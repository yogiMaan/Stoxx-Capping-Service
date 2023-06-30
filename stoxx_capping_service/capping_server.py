"""Python implementation of the index capping"""

from collections import namedtuple
from concurrent import futures
import copy
import logging
import grpc

from capping_pb2 import CapResult, Methodology_Ladder
from stoxx_capping_service.capping_pb2_grpc import CappingServicer, add_CappingServicer_to_server


class CappingServicer(CappingServicer):
    """Provides methods that implement functionality of capping server."""

    @staticmethod
    def __cap_component(self, limit, componentPcts, excludes, isFirstIteration, origSumTruncatedWeightsUnderLimit,
                        origSumResiduals):

        # https://docs.python.org/3/library/collections.html#collections.namedtuple
        ComponentWeight = namedtuple('CappingRecord',
                                     'pctMcap, applyCap, residual, truncatedWeight, underweightPct, spreadResidual, weightPlusResidual')

        componentWghts = {}
        sumTruncatedWeightsUnderLimit = 0.0 if isFirstIteration else origSumTruncatedWeightsUnderLimit
        sumResiduals = 0.0 if isFirstIteration else origSumResiduals

        for key in componentPcts:
            if componentPcts[key] >= limit:
                residual = 0 if key in excludes else componentPcts[key] - limit
                truncatedWeight = componentPcts[key] - residual
                componentWghts[key] = ComponentWeight(pctMcap=componentPcts[key], applyCap=0 if key in excludes else 1,
                                                      residual=residual, truncatedWeight=truncatedWeight,
                                                      underweightPct=0, spreadResidual=0,
                                                      weightPlusResidual=truncatedWeight)
                if isFirstIteration:
                    sumResiduals += residual
            elif isFirstIteration:
                sumTruncatedWeightsUnderLimit += componentPcts[key]

        for key in componentPcts:
            if componentPcts[key] < limit:
                underweightPct = componentPcts[key] / sumTruncatedWeightsUnderLimit
                spreadResidual = underweightPct * sumResiduals
                weightPlusResidual = componentPcts[key] + spreadResidual
                componentWghts[key] = ComponentWeight(pctMcap=componentPcts[key], applyCap=0 if key in excludes else 1,
                                                      residual=0, truncatedWeight=componentPcts[key],
                                                      underweightPct=underweightPct, spreadResidual=spreadResidual,
                                                      weightPlusResidual=weightPlusResidual)

        return componentWghts

    @staticmethod
    def __after_nth_largest_components(self, componentPcts, n):
        excludes = set()
        if n <= 1:
            return excludes
        componentPctsSortedDesc = sorted(componentPcts.items(), key=lambda item: item[1], reverse=True)
        i = 0
        while (i < (n - 1) and i < len(componentPctsSortedDesc)):
            excludes.add(componentPctsSortedDesc[i][0])  # just get the key, not the key/value pair
            i += 1
        return excludes

    @staticmethod
    def __mcaps_to_component_pcts(mcaps, componentIndex):
        sumMcaps = 0.0
        for mcap in mcaps:
            sumMcaps += mcap.mcap

        # this line stops a testcase where sum = 1.0000000000000002 from failing
        sumMcaps = round(sumMcaps, 15)

        componentPcts = {}
        for mcap in mcaps:
            key = mcap.components[componentIndex]
            if key in componentPcts:
                pctMcap = mcap.mcap / sumMcaps
                componentPcts[key] += pctMcap
            else:
                componentPcts[key] = mcap.mcap / sumMcaps

        return componentPcts

    @staticmethod
    def __mcaps_pcts_to_pcts_next_component(mcaps, weightsPlusResiduals, componentIndex):

        componentPcts = {}
        for mcap in mcaps:
            prevKey = mcap.components[componentIndex - 1]
            key = mcap.components[componentIndex]
            if key in componentPcts:
                componentPcts[key] += weightsPlusResiduals[prevKey]
            else:
                componentPcts[key] = weightsPlusResiduals[prevKey]

        return componentPcts

    @staticmethod
    def __convert_to_mcap_decreasing(cpResults):
        maxF = 0.0
        for f in cpResults.CappingFactor:
            if f > maxF:
                maxF = f

        i = 0
        while i < len(cpResults.CappingFactor):
            cpResults.CappingFactor[i] = round(cpResults.CappingFactor[i] / maxF, 15)
            i += 1

        return cpResults

    @staticmethod
    def __further_iterations_required(componentWghts, limit, excludes):
        for key in componentWghts:
            if key not in excludes and componentWghts[key].weightPlusResidual > limit:
                return True
        return False

    @staticmethod
    def __sumTruncatedWeightsUnderlimit(self, componentWghts, limit):
        sum = 0.0
        for key in componentWghts:
            if componentWghts[key].truncatedWeight < limit:
                sum += componentWghts[key].truncatedWeight
        return sum

    @staticmethod
    def __cap_nth_level(self, limit, componentPcts, applyLimitToNthLargestAndBelow):

        isFirstIteration = True
        further_iterations_required = False
        sumTruncatedWeightsUnderLimit = 0.0
        sumResiduals = 0.0

        if (limit == 0):  # equal weighted
            limit = 1 / len(componentPcts)

        excludes = self.__after_nth_largest_components(self, componentPcts=componentPcts,
                                                       n=applyLimitToNthLargestAndBelow)

        originalComponentPcts = copy.copy(componentPcts)

        wasMultiIteration = False

        while isFirstIteration or further_iterations_required:

            if not isFirstIteration:
                wasMultiIteration = True
                componentPcts = {}
                for key in componentWghts:
                    componentPcts[key] = componentWghts[key].weightPlusResidual

            componentWghts = self.__cap_component(self, limit=limit, componentPcts=componentPcts, excludes=excludes,
                                                  isFirstIteration=isFirstIteration,
                                                  origSumTruncatedWeightsUnderLimit=sumTruncatedWeightsUnderLimit,
                                                  origSumResiduals=sumResiduals)

            further_iterations_required = self.__further_iterations_required(componentWghts=componentWghts, limit=limit,
                                                                             excludes=excludes)

            if isFirstIteration and further_iterations_required:
                sumTruncatedWeightsUnderLimit = self.__sumTruncatedWeightsUnderlimit(self,
                                                                                     componentWghts=componentWghts,
                                                                                     limit=limit)
                for key in componentWghts:
                    sumResiduals += componentWghts[key].residual

            isFirstIteration = False

        if wasMultiIteration:
            for key in componentWghts:
                componentWghts[key] = componentWghts[key]._replace(pctMcap=originalComponentPcts[key])

        return componentWghts;

    def Cap(self, request, context):
        # print("methodology is: " + Methodology.Name(request.methodology))
        lstComponentWghts = []

        componentPcts = self.__mcaps_to_component_pcts(mcaps=request.mcaps, componentIndex=0)

        componentIndex = 0
        for md in request.methodologyDatas:
            if (len(md.limitInfos) == 0):
                limit = 0
            else:
                limitInfo = md.limitInfos[0]
                limit = limitInfo.limit
                # limitName = limitInfo.limitName

            componentWghts = self.__cap_nth_level(self=self, limit=limit, componentPcts=componentPcts,
                                                  applyLimitToNthLargestAndBelow=md.applyLimitToNthLargestAndBelow)
            if (componentIndex + 1) < len(request.methodologyDatas):
                for componentWght in componentWghts:
                    componentPcts[componentWght] = componentWghts[componentWght].weightPlusResidual

                if request.methodology != Methodology_Ladder:
                    componentPcts = self.__mcaps_pcts_to_pcts_next_component(mcaps=request.mcaps,
                                                                             weightsPlusResiduals=componentPcts,
                                                                             componentIndex=componentIndex + 1)
            lstComponentWghts.append(componentWghts)
            componentIndex += 1

        cpResults = CapResult()
        i = 0
        while i < len(request.mcaps):
            factor = 1
            iMd = 0
            while iMd < len(request.methodologyDatas):
                iComponentIndex = 0 if request.methodology == Methodology_Ladder else iMd
                key = request.mcaps[i].components[iComponentIndex]
                f = lstComponentWghts[iMd][key].weightPlusResidual / (lstComponentWghts[iMd][key].pctMcap)
                factor *= f
                iMd += 1
            """cpResults.CappingFactor.append(round(factor, 15))
            cpResults.Id.append(key)
            """
            cpResults.capfactors.update({request.mcaps[i].ConstituentId: round(factor, 15)})
            i += 1

        if request.mcapDecreasingFactors:
            return self.__convert_to_mcap_decreasing(cpResults)

        return cpResults


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_CappingServicer_to_server(
        CappingServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
