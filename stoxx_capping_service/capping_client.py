"""The Python implementation of the gRPC capping client."""

from __future__ import print_function

import logging
import grpc
import capping_pb2
from stoxx_capping_service import capping_pb2_grpc


def cap(stub):
    #https://protobuf.dev/reference/python/python-generated/#repeated-fields 
    
    ci = capping_pb2.CapInput()    

    #ci.methodology = capping_pb2.Methodology_Fixed
    #ci.methodologyDatas.append(capping_pb2.MethodologyData(limit=0.1, notEnoughComponentsBehaviour= capping_pb2.NotEnoughComponentsBehaviour_Error)) #basic
    #ci.methodologyDatas.append(capping_pb2.MethodologyData(limit=0.08, notEnoughComponentsBehaviour= capping_pb2.NotEnoughComponentsBehaviour_Error)) #basic
    #ci.methodologyDatas.append(capping_pb2.MethodologyData()) #equal

    ci.methodology = capping_pb2.Methodology_Ladder
    ci.methodologyDatas.append(capping_pb2.MethodologyData(limit=0.1, applyLimitToNthLargestAndBelow=1, notEnoughComponentsBehaviour= capping_pb2.NotEnoughComponentsBehaviour_Error))
    ci.methodologyDatas.append(capping_pb2.MethodologyData(limit=0.09, applyLimitToNthLargestAndBelow=2, notEnoughComponentsBehaviour= capping_pb2.NotEnoughComponentsBehaviour_Error))
    ci.methodologyDatas.append(capping_pb2.MethodologyData(limit=0.08, applyLimitToNthLargestAndBelow=3, notEnoughComponentsBehaviour= capping_pb2.NotEnoughComponentsBehaviour_Error))

    # ci.methodologyDatas.append(capping_pb2.MethodologyData(limit=0.1, applyLimitToNthLargestAndBelow=1, notEnoughComponentsBehaviour= capping_pb2.NotEnoughComponentsBehaviour_Error))
    # ci.methodologyDatas.append(capping_pb2.MethodologyData(limit=0.09, applyLimitToNthLargestAndBelow=2, notEnoughComponentsBehaviour= capping_pb2.NotEnoughComponentsBehaviour_Error))
    # ci.methodologyDatas.append(capping_pb2.MethodologyData(limit=0.08, applyLimitToNthLargestAndBelow=3, notEnoughComponentsBehaviour= capping_pb2.NotEnoughComponentsBehaviour_Error))    
    # ci.mcapDecreasingFactors = True

    #ci.mcaps.append(capping_pb2.Mcap(instrId="1", mcap=12.0).components.extend("1"))
  

    ci.mcaps.append(capping_pb2.Mcap(mcap=12.0))
    ci.mcaps[len(ci.mcaps) -1].components.extend(["1"]) 

    ci.mcaps.append(capping_pb2.Mcap(mcap=11.0))
    ci.mcaps[len(ci.mcaps) -1].components.extend(["2"])
    ci.mcaps.append(capping_pb2.Mcap(mcap=10.0))
    ci.mcaps[len(ci.mcaps) -1].components.extend(["3"])    
    ci.mcaps.append(capping_pb2.Mcap(mcap=9.0))
    ci.mcaps[len(ci.mcaps) -1].components.extend(["4"])
    ci.mcaps.append(capping_pb2.Mcap(mcap=7.0))
    ci.mcaps[len(ci.mcaps) -1].components.extend(["5"])
    ci.mcaps.append(capping_pb2.Mcap(mcap=5.0))
    ci.mcaps[len(ci.mcaps) -1].components.extend(["7"])
    ci.mcaps.append(capping_pb2.Mcap(mcap=5.0))
    ci.mcaps[len(ci.mcaps) -1].components.extend(["8"])
    ci.mcaps.append(capping_pb2.Mcap(mcap=5.0))
    ci.mcaps[len(ci.mcaps) -1].components.extend(["9"])
    ci.mcaps.append(capping_pb2.Mcap(mcap=5.0))
    ci.mcaps[len(ci.mcaps) -1].components.extend(["10"])
    ci.mcaps.append(capping_pb2.Mcap(mcap=4.0))
    ci.mcaps[len(ci.mcaps) -1].components.extend(["11"])
    ci.mcaps.append(capping_pb2.Mcap(mcap=4.0))
    ci.mcaps[len(ci.mcaps) -1].components.extend(["12"])
    ci.mcaps.append(capping_pb2.Mcap(mcap=4.0))
    ci.mcaps[len(ci.mcaps) -1].components.extend(["13"])
    ci.mcaps.append(capping_pb2.Mcap(mcap=4.0))
    ci.mcaps[len(ci.mcaps) -1].components.extend(["14"])
    ci.mcaps.append(capping_pb2.Mcap(mcap=3.0))
    ci.mcaps[len(ci.mcaps) -1].components.extend(["15"])
    ci.mcaps.append(capping_pb2.Mcap(mcap=3.0))
    ci.mcaps[len(ci.mcaps) -1].components.extend(["16"])
    ci.mcaps.append(capping_pb2.Mcap(mcap=3.0))
    ci.mcaps[len(ci.mcaps) -1].components.extend(["17"])
    ci.mcaps.append(capping_pb2.Mcap(mcap=3.0))
    ci.mcaps[len(ci.mcaps) -1].components.extend(["18"])

    # ci.mcaps.append(capping_pb2.Mcap(mcap=6.0))
    # ci.mcaps[len(ci.mcaps) -1].components.extend(["1"]) 

    ci.mcaps.append(capping_pb2.Mcap(mcap=3.0))
    ci.mcaps[len(ci.mcaps) -1].components.extend(["19"])
    
    # ci.mcaps.append(capping_pb2.Mcap(mcap=6.0))
    # ci.mcaps[len(ci.mcaps) -1].components.extend(["1"])    


    #for x in ci.mcaps:
    #    print(x.instrId)

    #for x in ci.mcaps:
    #    print(x.mcap)

    #for x in ci.mcaps:
    #    print(x.components)

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
