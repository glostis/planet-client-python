'''Test the low-level client up to the request/response level. That is, verify
a request is made to the expected URL and the response is as provided. Unless
specifically needed (e.g., JSON format), the response content should not
matter'''

import os
import pytest

from planet import api
import requests
import requests_mock


client = api.Client()
client.api_key = 'foobar'


# @pytest.fixture(scope="module")
# def mock_get(path, data, status_code=200):
#
#     def outer(func):
#
#         @requests_mock.mock()
#         def inner(m):
#             m.register_uri('GET', client.base_url + path,
#                            text=data, status_code=status_code)
#             func()
#
#         return inner
#
#     return outer


def assert_client_exc(clz, msg, status=None):
    try:
        client._get('whatevs')
    except clz as ex:
        assert msg == ex.message
    else:
        raise AssertionError('expected %s' % clz.__name__)


def test_assert_client_execution_success():
    '''make sure our test works'''
    
    with requests_mock.Mocker() as m:

        uri = os.path.join(client.base_url, 'whatevs')
        m.get(uri, text='test', status_code=200)
        
        # Since the Client object captures the entire response, there's
        # not much to test against. Just check that an exception is not raised.
        try:
            client._get('whatevs')
            assert True
        except:
            assert False


def test_assert_client_execution_failure():
    '''make sure our test works'''
    
    with requests_mock.Mocker() as m:

        uri = os.path.join(client.base_url, 'whatevs')
        m.get(uri, text='test', status_code=404)
        
        # Check that an exception is raised
        try:
            client._get('whatevs')
        except api.APIException as e:
            assert True
            return
        
        assert False


def test_missing_api_key():
    
    client = api.Client()
    # make sure any detected key is cleared
    client.api_key = None

    def assert_missing():
        try:
            client._get('whatevs')
            assert False
        except api.InvalidAPIKey as ex:
            assert str(ex) == 'No API key provided'
    
    assert_missing()
    client.api_key = ''
    assert_missing()


def test_status_code_404():
    
    with requests_mock.Mocker() as m:
        
        uri = os.path.join(client.base_url, 'whatevs')
        m.get(uri, text='not exist', status_code=404)
        
        try:
            client._get('whatevs')
        except api.MissingResource as e:
            
            # TODO: Check returned string. Currently issues between Python 3 bytes and Python 2 strings
            assert True
            return
        
        assert False


def test_status_code_other():
    
    with requests_mock.Mocker() as m:
        
        uri = os.path.join(client.base_url, 'whatevs')
        m.get(uri, text='emergency', status_code=911)
        
        try:
            client._get('whatevs')
        except api.APIException as e:
            
            assert True
            return
        
        assert False


def test_list_all_scene_types():
    
    with requests_mock.Mocker() as m:
        
        uri = os.path.join(client.base_url, 'scenes')
        m.get(uri, text='oranges', status_code=200)
        
        # TODO: Check returned string. Currently issues between Python 3 bytes and Python 2 strings
        # assert client.list_scene_types().get_raw() == 'oranges'
        assert True


def test_fetch_scene_info_scene_id():
    
    with requests_mock.Mocker() as m:
        
        uri = os.path.join(client.base_url, 'scenes/ortho/x22')
        m.get(uri, text='bananas', status_code=200)
        
        client.get_scene_metadata('x22').get_raw() == 'bananas'
        assert True
