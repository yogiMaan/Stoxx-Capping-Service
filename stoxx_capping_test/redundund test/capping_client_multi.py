"""The Python implementation of the gRPC capping client."""

from __future__ import print_function

import logging
import grpc
import capping_pb2
from stoxx_capping_service import capping_pb2_grpc


def cap(stub):
    #https://protobuf.dev/reference/python/python-generated/#repeated-fields 
    
    ci = capping_pb2.CapInput()    

    ci.methodology = capping_pb2.Methodology_Fixed
    
    ci.methodologyDatas.append(capping_pb2.MethodologyData(limitInfos= [capping_pb2.LimitInfo(limit=0.1)], notEnoughComponentsBehaviour= capping_pb2.NotEnoughComponentsBehaviour_Error)) #basic
    ci.methodologyDatas.append(capping_pb2.MethodologyData(limitInfos= [capping_pb2.LimitInfo(limit=0.3)], notEnoughComponentsBehaviour= capping_pb2.NotEnoughComponentsBehaviour_Error)) #basic

    # ci.mcapDecreasingFactors = True

    ci.mcaps.append(capping_pb2.Mcap(mcap=12.0, components= ['1', 'a']))
    ci.mcaps.append(capping_pb2.Mcap(mcap=11.0, components= ['2', 'a']))
    ci.mcaps.append(capping_pb2.Mcap(mcap=10.0, components= ['3', 'a']))
    ci.mcaps.append(capping_pb2.Mcap(mcap=9.0,  components= ['4', 'a']))

    ci.mcaps.append(capping_pb2.Mcap(mcap=7.0, components= ['5', 'b']))
    ci.mcaps.append(capping_pb2.Mcap(mcap=5.0, components= ['6', 'b']))
    ci.mcaps.append(capping_pb2.Mcap(mcap=5.0, components= ['7', 'b']))

    ci.mcaps.append(capping_pb2.Mcap(mcap=5.0, components= ['8', 'c']))
    ci.mcaps.append(capping_pb2.Mcap(mcap=5.0, components= ['9', 'c']))

    ci.mcaps.append(capping_pb2.Mcap(mcap=4.0, components= ['10', 'd']))

    ci.mcaps.append(capping_pb2.Mcap(mcap=4.0, components= ['11', 'e']))
    ci.mcaps.append(capping_pb2.Mcap(mcap=4.0, components= ['12', 'e']))

    ci.mcaps.append(capping_pb2.Mcap(mcap=4.0, components= ['13', 'f']))
    ci.mcaps.append(capping_pb2.Mcap(mcap=3.0, components= ['14', 'f']))

    ci.mcaps.append(capping_pb2.Mcap(mcap=3.0, components= ['15', 'g']))
    ci.mcaps.append(capping_pb2.Mcap(mcap=3.0, components= ['16', 'g']))

    ci.mcaps.append(capping_pb2.Mcap(mcap=3.0, components= ['17', 'h']))
    ci.mcaps.append(capping_pb2.Mcap(mcap=3.0, components= ['18', 'h']))

    cpResult = stub.Cap(ci)    
    print ("got results")
    print(cpResult)

    

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
