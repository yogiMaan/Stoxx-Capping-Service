"""The Python implementation of the gRPC capping client."""

from __future__ import print_function

import logging
import grpc
import capping_pb2
import capping_pb2_grpc


def cap(stub):
    # https://protobuf.dev/reference/python/python-generated/#repeated-fields

    ci = capping_pb2.CapInput()

    ci.methodologyDatas.append(
        capping_pb2.MethodologyData(
            methodology=capping_pb2.Methodology_Exposure,
            # limitInfos=[capping_pb2.LimitInfo(limit=0.1)],
            notEnoughComponentsBehaviour=capping_pb2.NotEnoughComponentsBehaviour_NotApplicable,
        )
    )  # basic
    # ci.methodologyDatas.append(
    #     capping_pb2.MethodologyData(
    #         limitInfos=[capping_pb2.LimitInfo(limit=0.3)],
    #         notEnoughComponentsBehaviour=capping_pb2.NotEnoughComponentsBehaviour_Error,
    #     )
    # )  # basic

    # ci.mcapDecreasingFactors = True
    ci.parent_mcaps.append(capping_pb2.Mcap(mcap=20.0, components=["a"]))
    ci.parent_mcaps.append(capping_pb2.Mcap(mcap=15.0, components=["a"]))
    ci.parent_mcaps.append(capping_pb2.Mcap(mcap=30.0, components=["b"]))
    ci.parent_mcaps.append(capping_pb2.Mcap(mcap=20.0, components=["c"]))
    ci.parent_mcaps.append(capping_pb2.Mcap(mcap=10.0, components=["d"]))
    ci.parent_mcaps.append(capping_pb2.Mcap(mcap=5.0, components=["e"]))

    ci.mcaps.append(capping_pb2.Mcap(mcap=15.0, components=["a"]))
    ci.mcaps.append(capping_pb2.Mcap(mcap=15.0, components=["a"]))
    ci.mcaps.append(capping_pb2.Mcap(mcap=30.0, components=["b"]))
    ci.mcaps.append(capping_pb2.Mcap(mcap=19.0, components=["c"]))
    ci.mcaps.append(capping_pb2.Mcap(mcap=20.0, components=["d"]))
    ci.mcaps.append(capping_pb2.Mcap(mcap=1.0, components=["e"]))

    cap_result = stub.Cap(ci)
    print("got results")
    print(cap_result)


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = capping_pb2_grpc.CappingStub(channel)
        cap(stub)


if __name__ == "__main__":
    logging.basicConfig()
    run()
