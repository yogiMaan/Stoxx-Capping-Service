import pytest
from stoxx_capping_service import capping_pb2
import os
import logging

DEFAULT_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - line %(lineno)s - %(message)s"
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "DEBUG"), format=os.environ.get("LOG_FORMAT", DEFAULT_FORMAT))


@pytest.fixture(scope='module')
def grpc_add_to_server():
    from stoxx_capping_service.capping_pb2_grpc import add_CappingServicer_to_server
    return add_CappingServicer_to_server


@pytest.fixture(scope='module')
def grpc_servicer():
    from stoxx_capping_service.capping_server import CappingServicer
    return CappingServicer()


@pytest.fixture(scope='module')
def grpc_stub_cls(grpc_channel):
    from stoxx_capping_service.capping_pb2_grpc import CappingStub
    return CappingStub


def test_basic_capping(grpc_stub):
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
    cpResult = grpc_stub.Cap(ci)
    dictresult = {}
    for i in cpResult.capfactors:
        dictresult[i.ConstituentID] = i.factor

    Expected = {'18': 1.044776119402985, '15': 1.044776119402985, '16': 1.044776119402985, '6': 1.044776119402985,
                '5': 1.044776119402985, '10': 1.044776119402985, '17': 1.044776119402985, '11': 1.044776119402985,
                '13': 1.044776119402985, '7': 1.044776119402985, '9': 1.044776119402985, '1': 0.833333333333333,
                '2': 0.909090909090909, '14': 1.044776119402985, '12': 1.044776119402985, '4': 1.044776119402985,
                '3': 1.0, '8': 1.044776119402985}
    assert dictresult == Expected
