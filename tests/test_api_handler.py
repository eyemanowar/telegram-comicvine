from unittest.mock import MagicMock, patch
from api_handler import ApiHandler
import pytest
import requests



@patch('api_handler.requests.get')
def test_get_200(mock_get):
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = {"results": ['test1', 'test2', 'test3']}
    mock_get.return_value = fake_response

    handler = ApiHandler()
    response = handler.get_request(url='https://test.com', params={})

    assert response == {"results": ['test1', 'test2', 'test3']} , f'The resposne is not 200. The response is: {response}'


@patch('api_handler.requests.get')
def test_get_404(mock_get):
    fake_response = MagicMock()
    fake_response.status_code = 404
    fake_response.json.return_value = {"results": ['test1', 'test2', 'test3']}
    mock_get.return_value = fake_response
    handler = ApiHandler()
    with pytest.raises(AssertionError):
        response = handler.get_request(url='https://test.com', params={})

@patch('api_handler.requests.get')
def test_get_runtime_error(mock_get):
    mock_get.side_effect = requests.RequestException("connection failed")
    handler = ApiHandler()
    with pytest.raises(RuntimeError):
        response = handler.get_request(url='https://test.com', params={})
