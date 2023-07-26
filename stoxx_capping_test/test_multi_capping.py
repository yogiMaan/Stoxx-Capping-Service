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
            methodology=capping_pb2.Methodology_Fixed,
            limitInfos=[capping_pb2.LimitInfo(limit=0.1)],
            notEnoughComponentsBehaviour=capping_pb2.NotEnoughComponentsBehaviour_Error,
        )
    )  # basic
    ci.methodologyDatas.append(
        capping_pb2.MethodologyData(
            limitInfos=[capping_pb2.LimitInfo(limit=0.3)],
            notEnoughComponentsBehaviour=capping_pb2.NotEnoughComponentsBehaviour_Error,
        )
    )  # basic

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

    cpResult = grpc_stub.Cap(ci)
    dict = {}
    for i in cpResult.capfactors:
        dict[i.ConstituentID] = i.factor
    Expected = {'1': 0.634469696969697,
                '10': 1.206896551724139,
                '11': 1.206896551724139,
                '12': 1.206896551724139,
                '13': 1.206896551724139,
                '14': 1.206896551724139,
                '15': 1.206896551724139,
                '16': 1.206896551724139,
                '17': 1.206896551724139,
                '18': 1.206896551724139,
                '2': 0.692148760330579,
                '3': 0.761363636363636,
                '4': 0.795454545454546,
                '5': 1.206896551724139,
                '6': 1.206896551724139,
                '7': 1.206896551724139,
                '8': 1.206896551724139,
                '9': 1.206896551724139}

    assert dict == Expected
