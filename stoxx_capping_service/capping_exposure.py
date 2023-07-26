import logging
import sys
import pandas as pd
logger = logging.getLogger(__name__)

def cap_exposure(df_parent_mcaps: pd.DataFrame, df_mcaps: pd.DataFrame):
    df_parent_grouped = df_parent_mcaps.groupby("c1")["mcap"].sum().reset_index()
    df_parent_grouped_sum = round(df_parent_grouped["mcap"].sum(), 15)
    df_parent_grouped["pct"] = df_parent_grouped.apply(
        lambda x: x["mcap"] / df_parent_grouped_sum, axis=1
    )

    df_grouped = df_mcaps.groupby("c1")["mcap"].sum().reset_index()
    df_grouped_sum = round(df_grouped["mcap"].sum(), 15)
    df_grouped["pct"] = df_grouped.apply(
        lambda x: x["mcap"] / df_grouped_sum, axis=1
    )

    df_final = df_parent_grouped.merge(df_grouped, on="c1", how="left")[
        ["c1", "pct_x", "pct_y"]
    ]
    df_final.rename(
        columns={"pct_x": "pct_parent", "pct_y": "pct_child"}, inplace=True
    )
    df_final["factor"] = df_final.apply(
        lambda x: x["pct_parent"] / x["pct_child"], axis=1
    )

    has_missing_component = df_final["factor"].isna().any()
    if not has_missing_component:
        df_final = df_final.merge(df_mcaps, on="c1", how="inner")
        return df_final

    df_final["child_pct_capped_mcaps"] = df_final.apply(
        lambda x: x["pct_child"] * x["factor"], axis=1
    )

    sum_child_pct = round(df_final["child_pct_capped_mcaps"].sum(), 15)

    df_final["missing_weight"] = df_final.apply(
        lambda x: (1 - sum_child_pct)
                  * (x["child_pct_capped_mcaps"] / sum_child_pct),
        axis=1,
    )

    df_final["new_child_tw"] = df_final.apply(
        lambda x: x["child_pct_capped_mcaps"] + x["missing_weight"],
        axis=1,
    )

    df_final.rename(columns={"factor": "old_factor"}, inplace=True)

    df_final["factor"] = df_final.apply(
        lambda x: x["new_child_tw"] / x["pct_child"],
        axis=1,
    )
    df_final = df_final.merge(df_mcaps, on="c1", how="inner")
    return df_final
