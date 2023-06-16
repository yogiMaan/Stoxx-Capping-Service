"""The Python implementation of the gRPC capping client."""

from __future__ import print_function

import logging
import grpc
import capping_pb2
import capping_pb2_grpc

def cap(stub):   
    #https://protobuf.dev/reference/python/python-generated/#repeated-fields 
    
    ci = capping_pb2.CapInput()    

    ci.methodology = capping_pb2.Methodology_Fixed
    
    ci.methodologyDatas.append(capping_pb2.MethodologyData(limitInfos= [capping_pb2.LimitInfo(limit=0.1)], notEnoughComponentsBehaviour= capping_pb2.NotEnoughComponentsBehaviour_Error)) #basic    

    # ci.mcapDecreasingFactors = True

    # ci.mcaps.append(capping_pb2.Mcap(mcap=12.0, components= ['1']))
    # ci.mcaps.append(capping_pb2.Mcap(mcap=11.0, components= ['2']))
    # ci.mcaps.append(capping_pb2.Mcap(mcap=10.0, components= ['3']))
    # ci.mcaps.append(capping_pb2.Mcap(mcap=9.0, components= ['4']))
    # ci.mcaps.append(capping_pb2.Mcap(mcap=7.0, components= ['5']))

    # ci.mcaps.append(capping_pb2.Mcap(mcap=5.0, components= ['6']))
    # ci.mcaps.append(capping_pb2.Mcap(mcap=5.0, components= ['7']))
    # ci.mcaps.append(capping_pb2.Mcap(mcap=5.0, components= ['8']))
    # ci.mcaps.append(capping_pb2.Mcap(mcap=5.0, components= ['9']))

    # ci.mcaps.append(capping_pb2.Mcap(mcap=4.0, components= ['10']))
    # ci.mcaps.append(capping_pb2.Mcap(mcap=4.0, components= ['11']))
    # ci.mcaps.append(capping_pb2.Mcap(mcap=4.0, components= ['12']))
    # ci.mcaps.append(capping_pb2.Mcap(mcap=4.0, components= ['13']))

    # ci.mcaps.append(capping_pb2.Mcap(mcap=3.0, components= ['14']))
    # ci.mcaps.append(capping_pb2.Mcap(mcap=3.0, components= ['15']))
    # ci.mcaps.append(capping_pb2.Mcap(mcap=3.0, components= ['16']))
    # ci.mcaps.append(capping_pb2.Mcap(mcap=3.0, components= ['17']))
    # ci.mcaps.append(capping_pb2.Mcap(mcap=3.0, components= ['18']))

    ci.mcaps.append(capping_pb2.Mcap(mcap=0.12, components= ['1']))
    ci.mcaps.append(capping_pb2.Mcap(mcap=0.11, components= ['2']))
    ci.mcaps.append(capping_pb2.Mcap(mcap=0.1, components= ['3']))
    ci.mcaps.append(capping_pb2.Mcap(mcap=0.09, components= ['4']))
    ci.mcaps.append(capping_pb2.Mcap(mcap=0.07, components= ['5']))

    ci.mcaps.append(capping_pb2.Mcap(mcap=0.05, components= ['6']))
    ci.mcaps.append(capping_pb2.Mcap(mcap=0.05, components= ['7']))
    ci.mcaps.append(capping_pb2.Mcap(mcap=0.05, components= ['8']))
    ci.mcaps.append(capping_pb2.Mcap(mcap=0.05, components= ['9']))

    ci.mcaps.append(capping_pb2.Mcap(mcap=0.04, components= ['10']))
    ci.mcaps.append(capping_pb2.Mcap(mcap=0.04, components= ['11']))
    ci.mcaps.append(capping_pb2.Mcap(mcap=0.04, components= ['12']))
    ci.mcaps.append(capping_pb2.Mcap(mcap=0.04, components= ['13']))

    ci.mcaps.append(capping_pb2.Mcap(mcap=0.03, components= ['14']))
    ci.mcaps.append(capping_pb2.Mcap(mcap=0.03, components= ['15']))
    ci.mcaps.append(capping_pb2.Mcap(mcap=0.03, components= ['16']))
    ci.mcaps.append(capping_pb2.Mcap(mcap=0.03, components= ['17']))
    ci.mcaps.append(capping_pb2.Mcap(mcap=0.03, components= ['18']))

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
