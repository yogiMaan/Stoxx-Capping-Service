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
            methodology=capping_pb2.Methodology_Ladder,
            limitInfos=[
                capping_pb2.LimitInfo(limit=0.1),
                capping_pb2.LimitInfo(limit=0.09),
                capping_pb2.LimitInfo(limit=0.08),
            ],
            notEnoughComponentsBehaviour=capping_pb2.NotEnoughComponentsBehaviour_Error,
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

    # Append the mcaps to the CapInput object
    cpResult = grpc_stub.Cap(ci)
    dict = {}
    for i in cpResult.capfactors:
        dict[i.ConstituentID] = i.factor
    Expected = {'18': 1.120689655172414, '15': 1.120689655172414, '16': 1.120689655172414, '6': 1.120689655172415, '5': 1.120689655172414, '10': 1.120689655172414, '17': 1.120689655172414, '11': 1.120689655172414, '13': 1.120689655172414, '7': 1.120689655172415, '9': 1.120689655172415, '1': 0.833333333333333, '2': 0.818181818181818, '14': 1.120689655172414, '12': 1.120689655172414, '4': 0.888888888888889, '3': 0.8, '8': 1.120689655172415
                }

    assert dict == Expected
