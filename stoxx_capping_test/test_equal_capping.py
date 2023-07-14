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

    ci.methodology = capping_pb2.Methodology_Fixed
    ci.methodologyDatas.append(capping_pb2.MethodologyData())  # equal

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
    for Id in cpResult.capfactors:
        print(Id, cpResult.capfactors[Id])
    Result = cpResult.capfactors
    print(Result)
    Expected = {'18': 1.851851851851852, '15': 1.851851851851852, '16': 1.851851851851852, '6': 1.111111111111111,
                '5': 0.793650793650793, '10': 1.388888888888889, '17': 1.851851851851852, '11': 1.388888888888889,
                '13': 1.388888888888889, '7': 1.111111111111111, '9': 1.111111111111111, '1': 0.462962962962963,
                '2': 0.505050505050505, '14': 1.851851851851852, '12': 1.388888888888889, '4': 0.617283950617284,
                '3': 0.555555555555555, '8': 1.111111111111111
                }

    assert Expected == Result
