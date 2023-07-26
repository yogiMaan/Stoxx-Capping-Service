"""Python implementation of the index capping"""
from concurrent import futures
import logging
import pandas as pd
import grpc
import capping_pb2
from stoxx_capping_service import capping_pb2_grpc
import capping_Core as Core
import capping_ladder as ladder
import capping_exposure as exposure


class CappingServicer(capping_pb2_grpc.CappingServicer):
    """Provides methods that implement functionality of capping server."""

    def __mcaps_to_data_frame(self, mcaps):
        rows = list()
        for mcap in mcaps:
            d = {"mcap": mcap.mcap, "c1": mcap.components[0], "ConstituentId": mcap.ConstituentId}

            # if we are doing multi component capping, add the additional components
            for i in range(1, len(mcap.components)):
                d["c" + str(i + 1)] = mcap.components[i]
            rows.append(d)

        return pd.DataFrame(rows)

    def __cap(self, request):
        df_mcaps = self.__mcaps_to_data_frame(mcaps=request.mcaps)

        for i_component_index, methodology_data in enumerate(request.methodologyDatas):
            print(
                "methodology: "
                + capping_pb2.Methodology.Name(methodology_data.methodology)
            )
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

            if len(methodology_data.limitInfos) == 0:
                cap_limit = 0
            else:
                limit_info = methodology_data.limitInfos[0]
                cap_limit = limit_info.limit

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
        return df_final

    def __multiply_factors(self, num_components: int, df_row: pd.Series):
        factor = df_row["c1_factor"]

        if num_components == 1:
            return factor

        for i in range(2, (num_components + 1)):
            factor *= df_row["c" + str(i) + "_factor"]

        return factor

    def Cap(self, request, context):
        # print("methodology is: " + capping_pb2.Methodology.Name(request.methodology))

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
    logging.basicConfig()
    serve()
