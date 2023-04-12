import requests
import pytest

login_url = 'http://localhost:5000/api/auth/login'
trade_url = 'http://localhost:5000/api/user/trades'

def test_valid_request():
    user = {
        'email': 'smith65@gmail.com',
        'password': '123456'
    }

    try:
        res = requests.post(url=login_url, json=user)

        assert res.status_code == 200

        data = res.json()

        assert data['token'] != None

        res = requests.get(url=trade_url, headers={'Authorization': data['token']})

        assert res.status_code == 200

        data = res.json()

        assert data['trades'] != None

        trades = data['trades']

        assert len(trades) >= 0
    except:
        assert 'Exception Thrown' == 'Exception Caught'
