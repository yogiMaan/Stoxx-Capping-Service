from decimal import Context
from operator import concat
from grpc import ServicerContext, StatusCode
import pytest
import stoxx_capping_service
from stoxx_capping_service import capping_pb2
from stoxx_capping_service.capping_pb2 import *
from stoxx_capping_service.capping_pb2_grpc import CappingStub
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


def test_equal_capping(grpc_stub):
    ci = capping_pb2.CapInput()    

    ci.methodology = capping_pb2.Methodology_Fixed    
    ci.methodologyDatas.append(capping_pb2.MethodologyData()) #equal


    data = [
        {'mcap': 12.0, 'components': ['1']},
        {'mcap': 11.0, 'components': ['2']},
        {'mcap': 10.0, 'components': ['3']},
        {'mcap': 9.0, 'components': ['4']},
        {'mcap': 7.0, 'components': ['5']},
        {'mcap': 5.0, 'components': ['6']},
        {'mcap': 5.0, 'components': ['7']},
        {'mcap': 5.0, 'components': ['8']},
        {'mcap': 5.0, 'components': ['9']},
        {'mcap': 4.0, 'components': ['10']},
        {'mcap': 4.0, 'components': ['11']},
        {'mcap': 4.0, 'components': ['12']},
        {'mcap': 4.0, 'components': ['13']},
        {'mcap': 3.0, 'components': ['14']},
        {'mcap': 3.0, 'components': ['15']},
        {'mcap': 3.0, 'components': ['16']},
        {'mcap': 3.0, 'components': ['17']},
        {'mcap': 3.0, 'components': ['18']}
    ]
    # Create a DataFrame using pandas
    df = pd.DataFrame(data)

    # Convert the DataFrame to a list of dictionaries
    mcaps = df.to_dict('records')

    # Append the mcaps to the CapInput object
    ci.mcaps.extend([Mcap(mcap=row['mcap'], components=row['components']) for row in mcaps])
    cpResult = grpc_stub.Cap(ci)    
    print ("got results")
    print(cpResult)

    #assert 1==2
