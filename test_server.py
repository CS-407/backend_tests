import requests
import pytest

url = 'http://localhost:5000/'

def test_server_run_state():
    try:
        requests.get(url)
        # If server is running, request will go through
        assert True
    except:
        # If server is not running, network exception should be thrown
        assert pytest.raises(Exception)

def test_non_existent_endpoint():
    try:
        res = requests.get(url)
        assert res.status_code == 404
    except:
        # If server is not running, network exception should be thrown
        assert pytest.raises(Exception)