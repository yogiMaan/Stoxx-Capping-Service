import pytest
from stoxx_capping_service import capping_pb2


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


def test_equal_capping(grpc_stub):
    ci = capping_pb2.CapInput()

    ci.methodology = capping_pb2.Methodology_Ladder
    ci.methodologyDatas.append(
        capping_pb2.MethodologyData(limitInfos=[capping_pb2.LimitInfo(limit=0.1)], applyLimitToNthLargestAndBelow=1,
                                    notEnoughComponentsBehaviour=capping_pb2.NotEnoughComponentsBehaviour_Error))
    ci.methodologyDatas.append(
        capping_pb2.MethodologyData(limitInfos=[capping_pb2.LimitInfo(limit=0.09)], applyLimitToNthLargestAndBelow=2,
                                    notEnoughComponentsBehaviour=capping_pb2.NotEnoughComponentsBehaviour_Error))
    ci.methodologyDatas.append(
        capping_pb2.MethodologyData(limitInfos=[capping_pb2.LimitInfo(limit=0.08)], applyLimitToNthLargestAndBelow=3,
                                    notEnoughComponentsBehaviour=capping_pb2.NotEnoughComponentsBehaviour_Error))

    ci.mcaps.append(capping_pb2.Mcap(mcap=12.0, components=['1', 'a'], ConstituentId="1"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=11.0, components=['2', 'a'], ConstituentId="2"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=10.0, components=['3', 'a'], ConstituentId="3"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=9.0, components=['4', 'a'], ConstituentId="4"))

    ci.mcaps.append(capping_pb2.Mcap(mcap=7.0, components=['5', 'b'], ConstituentId="5"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=5.0, components=['6', 'b'], ConstituentId="6"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=5.0, components=['7', 'b'], ConstituentId="7"))

    ci.mcaps.append(capping_pb2.Mcap(mcap=5.0, components=['8', 'c'], ConstituentId="8"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=5.0, components=['9', 'c'], ConstituentId="9"))

    ci.mcaps.append(capping_pb2.Mcap(mcap=4.0, components=['10', 'd'], ConstituentId="10"))

    ci.mcaps.append(capping_pb2.Mcap(mcap=4.0, components=['11', 'e'], ConstituentId="11"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=4.0, components=['12', 'e'], ConstituentId="12"))

    ci.mcaps.append(capping_pb2.Mcap(mcap=4.0, components=['13', 'f'], ConstituentId="13"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=3.0, components=['14', 'f'], ConstituentId="14"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=3.0, components=['15', 'g'], ConstituentId="15"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=3.0, components=['16', 'g'], ConstituentId="16"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=3.0, components=['17', 'h'], ConstituentId="17"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=3.0, components=['18', 'h'], ConstituentId="18"))

    # Append the mcaps to the CapInput object
    cpResult = grpc_stub.Cap(ci)
    for Id in cpResult.capfactors:
        print(Id, cpResult.capfactors[Id])
    Result = cpResult.capfactors
    print(Result)
    Expected = {'18': 1.120689655172414, '15': 1.120689655172414, '16': 1.120689655172414, '6': 1.120689655172413,
                '5': 1.120689655172413, '10': 1.120689655172413, '17': 1.120689655172414, '11': 1.120689655172413,
                '13': 1.120689655172413, '7': 1.120689655172413, '9': 1.120689655172413, '1': 0.833333333333333,
                '2': 0.818181818181818, '14': 1.120689655172414, '12': 1.120689655172413, '4': 0.888888888888889,
                '3': 0.8, '8': 1.120689655172413
                }

    assert Expected == Result
