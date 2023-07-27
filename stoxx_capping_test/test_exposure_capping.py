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

    ci.methodologyDatas.append(
        capping_pb2.MethodologyData(
            methodology=capping_pb2.Methodology_Exposure,

            notEnoughComponentsBehaviour=capping_pb2.NotEnoughComponentsBehaviour_NotApplicable,
        )
    )

    ci.parent_mcaps.append(capping_pb2.Mcap(mcap=20.0, components=["a"], ConstituentId="1"))
    ci.parent_mcaps.append(capping_pb2.Mcap(mcap=15.0, components=["a"], ConstituentId="2"))
    ci.parent_mcaps.append(capping_pb2.Mcap(mcap=30.0, components=["b"], ConstituentId="3"))
    ci.parent_mcaps.append(capping_pb2.Mcap(mcap=20.0, components=["c"], ConstituentId="4"))
    ci.parent_mcaps.append(capping_pb2.Mcap(mcap=10.0, components=["d"], ConstituentId="5"))
    ci.parent_mcaps.append(capping_pb2.Mcap(mcap=5.0, components=["e"], ConstituentId="6"))

    ci.mcaps.append(capping_pb2.Mcap(mcap=15.0, components=["a"], ConstituentId="1"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=15.0, components=["a"], ConstituentId="2"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=30.0, components=["b"], ConstituentId="3"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=19.0, components=["c"], ConstituentId="4"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=20.0, components=["d"], ConstituentId="5"))
    ci.mcaps.append(capping_pb2.Mcap(mcap=1.0, components=["e"], ConstituentId="6"))

    cpResult = grpc_stub.Cap(ci)
    Resultdict = {}
    for i in cpResult.capfactors:
        Resultdict[i.ConstituentID] = i.factor
    Expected = {'1': 1.166666666666667,
                '2': 1.166666666666667,
                '3': 1.0,
                '4': 1.052631578947368,
                '5': 0.5,
                '6': 5.0}

    assert Resultdict == Expected
