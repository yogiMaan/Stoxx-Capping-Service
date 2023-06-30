from decimal import Context
from operator import concat
from grpc import ServicerContext, StatusCode
import pytest
import stoxx_capping_service
from stoxx_capping_service import capping_pb2
from stoxx_capping_service.capping_pb2 import *
import pandas as pd


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

    ci.methodology = capping_pb2.Methodology_Fixed

    ci.methodologyDatas.append(capping_pb2.MethodologyData(limitInfos=[capping_pb2.LimitInfo(limit=0.1)],
                                                           notEnoughComponentsBehaviour=capping_pb2.NotEnoughComponentsBehaviour_Error))  # basic
    data = [
        {'mcap': 0.12, 'components': ['1']},
        {'mcap': 0.11, 'components': ['2']},
        {'mcap': 0.1, 'components': ['3']},
        {'mcap': 0.09, 'components': ['4']},
        {'mcap': 0.07, 'components': ['5']},
        {'mcap': 0.05, 'components': ['6']},
        {'mcap': 0.05, 'components': ['7']},
        {'mcap': 0.05, 'components': ['8']},
        {'mcap': 0.05, 'components': ['9']},
        {'mcap': 0.04, 'components': ['10']},
        {'mcap': 0.04, 'components': ['11']},
        {'mcap': 0.04, 'components': ['12']},
        {'mcap': 0.04, 'components': ['13']},
        {'mcap': 0.03, 'components': ['14']},
        {'mcap': 0.03, 'components': ['15']},
        {'mcap': 0.03, 'components': ['16']},
        {'mcap': 0.03, 'components': ['17']},
        {'mcap': 0.03, 'components': ['18']}
    ]
    # Create a DataFrame using pandas
    df = pd.DataFrame(data)

    # Convert the DataFrame to a list of dictionaries
    mcaps = df.to_dict('records')

    # Append the mcaps to the CapInput object
    ci.mcaps.extend([Mcap(mcap=row['mcap'], components=row['components']) for row in mcaps])

    cpResult = grpc_stub.Cap(ci)
    Expected = [0.833333333333333, 0.909090909090909, 1.0, 1.044776119402985, 1.044776119402985, 1.044776119402985,
                1.044776119402985, 1.044776119402985, 1.044776119402985, 1.044776119402985, 1.044776119402985,
                1.044776119402985, 1.044776119402985, 1.044776119402985, 1.044776119402985, 1.044776119402985,
                1.044776119402985, 1.044776119402985]
    Result = cpResult.CappingFactor

    assert Expected == Result
