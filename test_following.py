import requests
import pytest

login_url = 'http://localhost:5000/api/auth/login'

def test_send_follow_request():
    send_request_url = 'http://localhost:5000/api/user/follow'

    try:
        user = {
            'email': 'jdoe@gmail.com',
            'password': '123456'
        }

        res = requests.post(url=login_url, json=user)
        data = res.json()

        follow_obj = {
            'userId': '63e8451d540fd8c730cb98b4'
        }

        res = requests.post(url=send_request_url, json=follow_obj, headers={'Authorization': 'Bearer ' + data['token']})

        assert res.status_code == 200

        data = res.json()

        assert data['msg'] == 'Follow Request Sent'
    except Exception as e:
        print(e)
        assert 'Exception Thrown' == 'Exception Caught'