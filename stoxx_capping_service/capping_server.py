"""Python implementation of the index capping"""
import logging
import os
from concurrent import futures
import grpc
from capping_Core import __cap_nth_level as cap_nth, __mcaps_pcts_to_pcts_next_component as mcap_nxt_cmpt, \
    __convert_to_mcap_decreasing as mcap_decreasing
from capping_pb2 import CapResult, Methodology_Ladder
from capping_pb2_grpc import CappingServicer, add_CappingServicer_to_server
import pandas as pd

DEFAULT_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - line %(lineno)s - %(message)s"
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "DEBUG"), format=os.environ.get("LOG_FORMAT", DEFAULT_FORMAT))
logger = logging.getLogger(__name__)


class CappingServicer(CappingServicer):
    """Provides methods that implement functionality of capping server."""

    @staticmethod
    def __mcaps_to_component_pcts(mcaps, componentIndex):
        # Function to convert a list of MCaps to a dictionary of component percentages
        # The dictionary key is the component name and the value is the percentage
        #df = pd.DataFrame(mcaps, columns=['components', 'mcap'])
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
        logger.info("__mcaps_to_component_pcts: componentPcts: %s", componentPcts)
        return componentPcts

    def Cap(self, request, context):

        logger.info("Cap Function called")
        # logger.info("methodology is: " + Methodology.Name(request.methodology))
        lstComponentWghts = []

        componentPcts = self.__mcaps_to_component_pcts(
            mcaps=request.mcaps, componentIndex=0)

        componentIndex = 0
        for md in request.methodologyDatas:
            if len(md.limitInfos) == 0:
                limit = 0
            else:
                limitInfo = md.limitInfos[0]
                limit = limitInfo.limit
                # limitName = limitInfo.limitName

            componentWghts = cap_nth(limit=limit, componentPcts=componentPcts,
                                     applyLimitToNthLargestAndBelow=md.applyLimitToNthLargestAndBelow)
            if (componentIndex + 1) < len(request.methodologyDatas):
                for componentWght in componentWghts:
                    componentPcts[componentWght] = componentWghts[componentWght].weightPlusResidual

                if request.methodology != Methodology_Ladder:
                    componentPcts = mcap_nxt_cmpt(mcaps=request.mcaps,
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
                f = lstComponentWghts[iMd][key].weightPlusResidual / lstComponentWghts[iMd][key].pctMcap
                factor *= f
                iMd += 1
            """cpResults.CappingFactor.append(round(factor, 15))
            cpResults.Id.append(key)
            """
            cpResults.capfactors.update({request.mcaps[i].ConstituentId: round(factor, 15)})
            i += 1

        if request.mcapDecreasingFactors:
            return mcap_decreasing(cpResults)

        return cpResults


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_CappingServicer_to_server(
        CappingServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    serve()
