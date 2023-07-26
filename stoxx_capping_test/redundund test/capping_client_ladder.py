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
            methodology=capping_pb2.Methodology_Ladder,
            limitInfos=[
                capping_pb2.LimitInfo(limit=0.1),
                capping_pb2.LimitInfo(limit=0.09),
                capping_pb2.LimitInfo(limit=0.08),
            ],
            applyLimitToNthLargestAndBelow=1,
            notEnoughComponentsBehaviour=capping_pb2.NotEnoughComponentsBehaviour_Error,
        )
    )

    # ci.mcapDecreasingFactors = True

    ci.mcaps.append(capping_pb2.Mcap(mcap=12.0, components=["1"]))
    ci.mcaps.append(capping_pb2.Mcap(mcap=11.0, components=["2"]))
    ci.mcaps.append(capping_pb2.Mcap(mcap=10.0, components=["3"]))
    ci.mcaps.append(capping_pb2.Mcap(mcap=9.0, components=["4"]))
    ci.mcaps.append(capping_pb2.Mcap(mcap=7.0, components=["5"]))

    ci.mcaps.append(capping_pb2.Mcap(mcap=5.0, components=["6"]))
    ci.mcaps.append(capping_pb2.Mcap(mcap=5.0, components=["7"]))
    ci.mcaps.append(capping_pb2.Mcap(mcap=5.0, components=["8"]))
    ci.mcaps.append(capping_pb2.Mcap(mcap=5.0, components=["9"]))

    ci.mcaps.append(capping_pb2.Mcap(mcap=4.0, components=["10"]))
    ci.mcaps.append(capping_pb2.Mcap(mcap=4.0, components=["11"]))
    ci.mcaps.append(capping_pb2.Mcap(mcap=4.0, components=["12"]))
    ci.mcaps.append(capping_pb2.Mcap(mcap=4.0, components=["13"]))

    ci.mcaps.append(capping_pb2.Mcap(mcap=3.0, components=["14"]))
    ci.mcaps.append(capping_pb2.Mcap(mcap=3.0, components=["15"]))
    ci.mcaps.append(capping_pb2.Mcap(mcap=3.0, components=["16"]))
    ci.mcaps.append(capping_pb2.Mcap(mcap=3.0, components=["17"]))
    ci.mcaps.append(capping_pb2.Mcap(mcap=3.0, components=["18"]))

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
