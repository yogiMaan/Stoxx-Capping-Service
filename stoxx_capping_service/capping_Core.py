import logging
import sys
from collections import namedtuple
import copy
import pandas as pd

from core_logger import get_logger

logger = get_logger(__name__, 'logs/debug.log', use_formatter=True)
df_logger = get_logger(str(__name__) + '_dfs', 'logs/debug.log', use_formatter=False)
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
