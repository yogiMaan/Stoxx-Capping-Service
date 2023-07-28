import capping_Core as Core
import logging
import sys
import pandas as pd

def flatten_results_for_ladder(list_dfs: list):
    """Flatten the results of the ladder into a single dataframe
    args:
       :list_dfs: list of dataframes
    :return
        dataframe
    """
    try:
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
    except Exception as e:
        logging.error("Error in %s: %s", sys._getframe().f_code.co_name, e)
        raise e
    else:
        return df_root


# df_grouped is grouped df_macp
def cap_ladder(methodology_data, df_grouped):
    """Ladder capping
    args:
        :methodology_data: methodology data
        :df_grouped: grouped dataframe
    :return
        dataframe
    """
    try:
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
    except Exception as e:
        logging.error("Error in %s: %s", sys._getframe().f_code.co_name, e)
        raise e
    else:
        return df_grouped
