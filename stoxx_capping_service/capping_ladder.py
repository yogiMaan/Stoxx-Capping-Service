import capping_Core as Core
import logging
import sys
import pandas as pd
logger = logging.getLogger(__name__)



def flatten_results_for_ladder(list_dfs: list):
    df_root = list_dfs[0]
    for idx, df in enumerate(list_dfs):
        if idx > 0:
            df_root = df_root.merge(df, on="c1", how="inner")[
                ["c1", "mcap_x", "factor_x", "factor_y"]
            ]
            df_root["factor"] = df_root.apply(
                lambda x: x["factor_x"] * x["factor_y"], axis=1
            )
            df_root.drop(["factor_x", "factor_y"], axis=1, inplace=True)
        print("")
    return df_root


# df_grouped is grouped df_macp
def cap_ladder(methodology_data, df_grouped):
    df_group_list = list()
    for n, limit in enumerate(methodology_data.limitInfos):
        df_grouped = Core.cap_component(
            df_grouped=df_grouped,
            cap_limit=limit.limit,
            is_first_iteration=True,
            exclude_nth_rows_from_cap=None if n == 0 else n,
        )
        df_grouped["orig_pct"] = df_grouped["pct"]
        df_group_list.append(df_grouped.copy())
    df_grouped = flatten_results_for_ladder(df_group_list)
    return df_grouped