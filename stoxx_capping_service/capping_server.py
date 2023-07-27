"""Python implementation of the index capping"""

import capping_pb2
from stoxx_capping_service import capping_pb2_grpc
import capping_Core as Core
import capping_ladder as ladder
import capping_exposure as exposure
from concurrent import futures
from core_logger import get_logger
import pandas as pd
import grpc
import sys
import os

logger = get_logger(__name__, 'logs/debug.log', use_formatter=True)
df_logger = get_logger(str(__name__) + '_dfs', 'logs/debug.log', use_formatter=False)


class CappingServicer(capping_pb2_grpc.CappingServicer):
    """Provides methods that implement functionality of capping server."""

    @staticmethod
    def __mcaps_to_data_frame(mcaps):
        rows = list()
        for mcap in mcaps:
            d = {"mcap": mcap.mcap, "c1": mcap.components[0], "ConstituentId": mcap.ConstituentId}

            # if we are doing multi component capping, add the additional components
            for i in range(1, len(mcap.components)):
                d["c" + str(i + 1)] = mcap.components[i]
            rows.append(d)

        return pd.DataFrame(rows)

    @staticmethod
    def __multiply_factors(num_components: int, df_row: pd.Series):
        factor = df_row["c1_factor"] if "c1_factor" in df_row else df_row["factor"]

        if num_components == 1:
            return factor

        for i in range(2, (num_components + 1)):
            factor *= df_row["c" + str(i) + "_factor"]

        return factor

    def __cap(self, request):
        logger.info("Function %s:", sys._getframe().f_code.co_name)
        df_mcaps = self.__mcaps_to_data_frame(mcaps=request.mcaps)

        for i_component_index, methodology_data in enumerate(request.methodologyDatas):
            logger.info("methodology: %s", capping_pb2.Methodology.Name(methodology_data.methodology))
            logger.info("Running Iteration %s: ", str(i_component_index + 1))

            if methodology_data.methodology == capping_pb2.Methodology_Exposure:
                df_parent_mcaps = self.__mcaps_to_data_frame(mcaps=request.parent_mcaps)
                df_final = exposure.cap_exposure(
                    df_parent_mcaps=df_parent_mcaps, df_mcaps=df_mcaps
                )
                continue

            if i_component_index > 0:
                df_merged = df_mcaps.merge(df_grouped, on="c1", how="inner")[
                    ["c1", "c2", "weight_plus_residual", "ConstituentId"]
                ]
                df_merged.rename(columns={"weight_plus_residual": "mcap"}, inplace=True)
                df_merged.drop_duplicates(
                    subset="c" + str(i_component_index), inplace=True
                )
                df_grouped = (
                    df_merged.groupby("c" + str(i_component_index + 1))["mcap"]
                    .sum()
                    .reset_index()
                    .sort_values("mcap", ascending=False)
                )

            else:
                df_grouped = (
                    df_mcaps.groupby("c" + str(i_component_index + 1))["mcap"]
                    .sum()
                    .reset_index()
                    .sort_values("mcap", ascending=False)
                )
            logger.info("Iteration %s Grouped Mcaps : ", str(i_component_index + 1))
            df_logger.info("\n %s", df_mcaps.to_markdown(index=False))
            if len(methodology_data.limitInfos) == 0:
                cap_limit = 0
            else:
                limit_info = methodology_data.limitInfos[0]
                cap_limit = limit_info.limit
            logger.info("Iteration %s Limit %s: ",str(i_component_index + 1), cap_limit)
            if methodology_data.methodology == capping_pb2.Methodology_Ladder:
                df_grouped = ladder.cap_ladder(
                    methodology_data=methodology_data,
                    df_grouped=df_grouped
                )
            else:
                df_grouped = Core.cap_component(
                    df_grouped=df_grouped,
                    cap_limit=cap_limit,
                    is_first_iteration=True,
                )

            cols = list(
                df_mcaps.columns if i_component_index == 0 else df_final.columns
            )
            cols.append("factor")
            cols[0] = "mcap_x"

            if i_component_index == 0:
                df_final = df_mcaps.merge(
                    df_grouped, on="c" + str(i_component_index + 1), how="inner"
                )[cols]
            else:
                df_final = df_final.merge(
                    df_grouped, on="c" + str(i_component_index + 1), how="inner"
                )[cols]

            df_final.rename(
                columns={
                    "mcap_x": "mcap",
                    "factor": "c" + str(i_component_index + 1) + "_factor",
                },
                inplace=True,
            )

        df_final["factor"] = df_final.apply(
            lambda x: self.__multiply_factors(
                num_components=(i_component_index + 1), df_row=x
            ),
            axis=1,
        )
        logger.info("result after Iteration %s : ", str(i_component_index + 1))
        df_logger.info("\n %s", df_final.to_markdown(index=False))
        return df_final

    def Cap(self, request, context):

        logger.info("Function %s:", sys._getframe().f_code.co_name)
        df_factors = self.__cap(request=request)

        cap_result = capping_pb2.CapResult()
        factors = list(df_factors["factor"])
        max_factor = max(factors)

        for index, row in df_factors.iterrows():
            if request.mcapDecreasingFactors:
                factor = capping_pb2.Capfactor(ConstituentID=row["ConstituentId"],
                                               factor=round(row["factor"] / max_factor, 15))
                cap_result.capfactors.append(factor)

            else:
                factor = capping_pb2.Capfactor(ConstituentID=row["ConstituentId"], factor=round(row["factor"], 15))
                cap_result.capfactors.append(factor)

        return cap_result


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    capping_pb2_grpc.add_CappingServicer_to_server(CappingServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
