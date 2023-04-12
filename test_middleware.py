import requests
import pytest

login_url = 'http://localhost:5000/api/auth/login'
trade_url = 'http://localhost:5000/api/user/trades'

def test_unauthorized_request():
    try:
        res = requests.get(url=trade_url)

        assert res.status_code == 401

        data = res.json()

        assert data['msg'] == 'Not authorized'
    except:
        assert 'Exception' == 'Exception Caught'

def test_authorized_request():
    user = {
        'email': 'jdoe@gmail.com',
        'password': '123456'
    }
    
    try:
        res = requests.post(url=login_url, json=user)

        assert res.status_code == 200
        data = res.json()
        assert data['token'] != None

        res = requests.get(url=trade_url, headers={'Authorization': 'Bearer' + data['token']})

        assert res.status_code == 200
        data = res.json()
        assert data['msg'] == 'Authorized'
    except:
        assert 'Exception' == 'Exception Caught'