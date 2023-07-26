import logging
import sys
from collections import namedtuple
import copy
import pandas as pd

logger = logging.getLogger(__name__)


def cap_component(
        df_grouped: pd.DataFrame,
        cap_limit: float,
        is_first_iteration: bool,
        sum_residuals: float = None,
        sum_truncated_weight_under_cap_limit: float = None,
        exclude_nth_rows_from_cap: int = None,
):
    logger.info("Function %s:", sys._getframe().f_code.co_name)
    if is_first_iteration and exclude_nth_rows_from_cap is None:
        # the rounding line stops a testcase where sum = 1.0000000000000002 from failing
        component_sum = round(df_grouped["mcap"].sum(), 15)
        df_grouped["orig_pct"] = df_grouped.apply(
            lambda x: x["mcap"] / component_sum, axis=1
        )
        df_grouped["pct"] = df_grouped["orig_pct"]
    else:
        df_grouped.drop(
            columns=[
                "apply_cap",
                "residuals",
                "truncated_weight",
                "underweight_pct",
                "spread_residual",
                "weight_plus_residual",
                "factor",
            ],
            inplace=True,
        )

    df_grouped["apply_cap"] = True

    if exclude_nth_rows_from_cap is not None:
        # Update the column values for the first n rows
        df_grouped.loc[
            df_grouped.index[:exclude_nth_rows_from_cap], "apply_cap"
        ] = False

    df_grouped["residuals"] = df_grouped.apply(
        lambda x: x["pct"] - cap_limit
        if x["pct"] > cap_limit and x["apply_cap"] == True
        else 0,
        axis=1,
    )
    if sum_residuals is None:
        sum_residuals = round(df_grouped["residuals"].sum(), 15)

    df_grouped["truncated_weight"] = df_grouped.apply(
        lambda x: x["pct"] - x["residuals"], axis=1
    )

    if sum_truncated_weight_under_cap_limit is None:
        sum_truncated_weight_under_cap_limit = round(
            df_grouped[df_grouped["truncated_weight"] < cap_limit][
                "truncated_weight"
            ].sum(),
            15,
        )

    df_grouped["underweight_pct"] = df_grouped.apply(
        lambda x: x["truncated_weight"] / sum_truncated_weight_under_cap_limit
        if x["truncated_weight"] < cap_limit
        else 0,
        axis=1,
    )

    df_grouped["spread_residual"] = df_grouped.apply(
        lambda x: x["underweight_pct"] * sum_residuals, axis=1
    )

    df_grouped["weight_plus_residual"] = df_grouped.apply(
        lambda x: x["truncated_weight"] + x["spread_residual"], axis=1
    )

    df_grouped["weight_plus_residual"] = df_grouped.apply(
        lambda x: x["truncated_weight"] + x["spread_residual"], axis=1
    )
    df_grouped["factor"] = df_grouped.apply(
        lambda x: x["weight_plus_residual"] / x["orig_pct"],
        axis=1,
    )

    any_overweight_component = (
            (df_grouped["weight_plus_residual"] > cap_limit) & df_grouped["apply_cap"]
    ).any()

    df_grouped["pct"] = df_grouped["weight_plus_residual"]

    if any_overweight_component:
        return cap_component(
            df_grouped=df_grouped,
            cap_limit=cap_limit,
            is_first_iteration=False,
            sum_residuals=sum_residuals,
            sum_truncated_weight_under_cap_limit=sum_truncated_weight_under_cap_limit,
            exclude_nth_rows_from_cap=exclude_nth_rows_from_cap,
        )
    else:
        return df_grouped


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

"""
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
"""