"""The Python implementation of the gRPC capping client."""

from __future__ import print_function

import logging
import grpc
from stoxx_capping_service import capping_pb2
from stoxx_capping_service import capping_pb2_grpc


def cap(stub):
    #https://protobuf.dev/reference/python/python-generated/#repeated-fields 
    
    ci = capping_pb2.CapInput()

    ci.methodologyDatas.append(
        capping_pb2.MethodologyData(
            methodology=capping_pb2.Methodology.Methodology_Fixed,
            limitInfos=[capping_pb2.LimitInfo(limit=0.1)],
            notEnoughComponentsBehaviour=capping_pb2.NotEnoughComponentsBehaviour_NotApplicable,
        )
    )

    ci.mcaps.append(capping_pb2.Mcap(mcap=12.0, components=['1'], ConstituentId="1"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=11.0, components=['2'], ConstituentId="2"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=10.0, components=['3'], ConstituentId="3"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=9.0, components=['4'], ConstituentId="4"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=7.0, components=['5'], ConstituentId="5"))

    ci.mcaps.append(capping_pb2.Mcap(mcap=5.0, components=['6'], ConstituentId="6"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=5.0, components=['7'], ConstituentId="7"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=5.0, components=['8'], ConstituentId="8"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=5.0, components=['9'], ConstituentId="9"))

    ci.mcaps.append(capping_pb2.Mcap(mcap=4.0, components=['10'], ConstituentId="10"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=4.0, components=['11'], ConstituentId="11"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=4.0, components=['12'], ConstituentId="12"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=4.0, components=['13'], ConstituentId="13"))

    ci.mcaps.append(capping_pb2.Mcap(mcap=3.0, components=['14'], ConstituentId="14"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=3.0, components=['15'], ConstituentId="15"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=3.0, components=['16'], ConstituentId="16"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=3.0, components=['17'], ConstituentId="17"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=3.0, components=['18'], ConstituentId="18"))

    cpResult = stub.Cap(ci)    
    print ("got results")
    dict = {}
    for i in cpResult.capfactors:
        dict[i.ConstituentID] = i.factor
    print(dict)
    

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = capping_pb2_grpc.CappingStub(channel)
        cap(stub)
        #print("-------------- GetFeature --------------")
        #guide_get_feature(stub)
        #print("-------------- ListFeatures --------------")
        #guide_list_features(stub)
        #print("-------------- RecordRoute --------------")
        #guide_record_route(stub)
        #print("-------------- RouteChat --------------")
        #guide_route_chat(stub)


if __name__ == '__main__':
    logging.basicConfig()
    run()
