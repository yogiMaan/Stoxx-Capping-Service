import logging
import sys
from collections import namedtuple
import copy

logger = logging.getLogger(__name__)


def __after_nth_largest_components(componentPcts, n):
    logger.info("Function %s: starting", sys._getframe().f_code.co_name)
    excludes = set()
    if n <= 1:
        return excludes
    componentPctsSortedDesc = sorted(componentPcts.items(), key=lambda item: item[1], reverse=True)
    i = 0
    while (i < (n - 1) and i < len(componentPctsSortedDesc)):
        excludes.add(componentPctsSortedDesc[i][0])  # just get the key, not the key/value pair
        i += 1
        logger.info("excludes: %s", excludes)
        logger.info("Function %s: Finished", sys._getframe().f_code.co_name)
    return excludes


def __cap_component(limit, componentPcts, excludes, isFirstIteration, origSumTruncatedWeightsUnderLimit,
                    origSumResiduals):
    logger.info("Function %s:excludes: %s", sys._getframe().f_code.co_name, excludes)
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
    logger.info("Function %s: Finished", sys._getframe().f_code.co_name)
    return componentWghts


def __further_iterations_required(componentWghts, limit, excludes):
    logger.info("Function %s: starting", sys._getframe().f_code.co_name)
    for key in componentWghts:
        if key not in excludes and componentWghts[key].weightPlusResidual > limit:
            logger.info("Further iterations required")
            return True
    logger.info("Function %s: Finished", sys._getframe().f_code.co_name)
    return False


def __mcaps_pcts_to_pcts_next_component(mcaps, weightsPlusResiduals, componentIndex):
    logger.info("Function %s: starting", sys._getframe().f_code.co_name)
    componentPcts = {}
    for mcap in mcaps:
        prevKey = mcap.components[componentIndex - 1]
        key = mcap.components[componentIndex]
        if key in componentPcts:
            componentPcts[key] += weightsPlusResiduals[prevKey]
        else:
            componentPcts[key] = weightsPlusResiduals[prevKey]
    logger.info("componentPcts: %s", componentPcts)
    logger.info("Function %s: Finished", sys._getframe().f_code.co_name)
    return componentPcts


def __convert_to_mcap_decreasing(cpResults):
    logger.info("Function %s: starting", sys._getframe().f_code.co_name)
    maxF = 0.0
    for f in cpResults.CappingFactor:
        if f > maxF:
            maxF = f

    i = 0
    while i < len(cpResults.CappingFactor):
        cpResults.CappingFactor[i] = round(cpResults.CappingFactor[i] / maxF, 15)
        i += 1
    logger.info("CappingFactor: %s", cpResults.CappingFactor)
    logger.info("Function %s: Finished", sys._getframe().f_code.co_name)
    return cpResults


def __sumTruncatedWeightsUnderlimit(componentWghts, limit):
    logger.info("Function %s: starting", sys._getframe().f_code.co_name)
    sum = 0.0
    for key in componentWghts:
        if componentWghts[key].truncatedWeight < limit:
            sum += componentWghts[key].truncatedWeight
    logger.info("sumTruncatedWeightsUnderlimit: %s", sum)
    logger.info("Function %s: Finished", sys._getframe().f_code.co_name)
    return sum


def __cap_nth_level(limit, componentPcts, applyLimitToNthLargestAndBelow):
    logger.info("Function %s: starting", sys._getframe().f_code.co_name)
    isFirstIteration = True
    further_iterations_required = False
    sumTruncatedWeightsUnderLimit = 0.0
    sumResiduals = 0.0

    if (limit == 0):  # equal weighted
        limit = 1 / len(componentPcts)

    excludes = __after_nth_largest_components(componentPcts=componentPcts,
                                              n=applyLimitToNthLargestAndBelow)

    originalComponentPcts = copy.copy(componentPcts)

    wasMultiIteration = False

    while isFirstIteration or further_iterations_required:

        if not isFirstIteration:
            wasMultiIteration = True
            componentPcts = {}
            for key in componentWghts:
                componentPcts[key] = componentWghts[key].weightPlusResidual

        componentWghts = __cap_component(limit=limit, componentPcts=componentPcts, excludes=excludes,
                                         isFirstIteration=isFirstIteration,
                                         origSumTruncatedWeightsUnderLimit=sumTruncatedWeightsUnderLimit,
                                         origSumResiduals=sumResiduals)

        further_iterations_required = __further_iterations_required(componentWghts=componentWghts, limit=limit,
                                                                    excludes=excludes)

        if isFirstIteration and further_iterations_required:
            sumTruncatedWeightsUnderLimit = __sumTruncatedWeightsUnderlimit(
                componentWghts=componentWghts,
                limit=limit)
            for key in componentWghts:
                sumResiduals += componentWghts[key].residual

        isFirstIteration = False

    if wasMultiIteration:
        for key in componentWghts:
            componentWghts[key] = componentWghts[key]._replace(pctMcap=originalComponentPcts[key])

    logger.info("componentWghts: %s", componentWghts)
    logger.info("Function %s: Finished", sys._getframe().f_code.co_name)
    return componentWghts;
