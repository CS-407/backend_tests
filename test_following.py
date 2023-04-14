import requests
import pytest

login_url = 'http://localhost:5000/api/auth/login'
signup_url = 'http://localhost:5000/api/auth/signup'
follow_request_url = 'http://localhost:5000/api/user/follow'
accept_request_url = 'http://localhost:5000/api/user/follow/accept'
reject_request_url = 'http://localhost:5000/api/user/follow/reject'

userToAccept = {
    'email': 'userToAccept@gmail.com',
    'username': 'userToAccept',
    'password': '123456',
    'password2': '123456'
}

userToReject = {
    'email': 'userToReject@gmail.com',
    'username': 'userToReject',
    'password': '123456',
    'password2': '123456'
}

userToFollow = {
    'email': 'userToFollow@gmail.com',
    'username': 'userToFollow',
    'password': '123456',
    'password2': '123456'
}

@pytest.fixture(scope='module', autouse=True)
def run_before_tests():
    try:
        requests.post(url=signup_url, json=userToAccept)
        requests.post(url=signup_url, json=userToReject)
        requests.post(url=signup_url, json=userToFollow)

        yield
    except Exception as e:
        print(e)

def test_send_follow_request():
        
    try:
        res = requests.post(url=login_url, json=userToFollow)
        data = res.json()

        follow_id = data['user']['_id']

        res = requests.post(url=login_url, json=userToAccept)
        data = res.json()

        res = requests.post(url=f'{follow_request_url}/{follow_id}', headers={'Authorization': 'Bearer ' + data['token']})
        assert res.status_code == 200

        data = res.json()
        assert data['msg'] == 'Follow Request Sent'

        res = requests.post(url=login_url, json=userToReject)
        data = res.json()

        res = requests.post(url=f'{follow_request_url}/{follow_id}', headers={'Authorization': 'Bearer ' + data['token']})
        assert res.status_code == 200

        data = res.json()
        assert data['msg'] == 'Follow Request Sent'
    except Exception as e:
        print(e)
        assert 'Exception Thrown' == 'Exception Caught'

def test_accept_follow_request():
    try:
        res = requests.post(url=login_url, json=userToAccept)
        data = res.json()

        accept_id = data['user']['_id']

        res = requests.post(url=login_url, json=userToFollow)
        data = res.json()

        res = requests.post(url=f'{accept_request_url}/{accept_id}', headers={'Authorization': 'Bearer ' + data['token']})
        assert res.status_code == 200

        data = res.json()
        assert data['msg'] == 'Success'
    except Exception as e:
        print(e)
        assert 'Exception Thrown' == 'Exception Caught'

def test_reject_follow_request():
    try:
        res = requests.post(url=login_url, json=userToReject)
        data = res.json()

        reject_id = data['user']['_id']

        res = requests.post(url=login_url, json=userToFollow)
        data = res.json()

        res = requests.post(url=f'{reject_request_url}/{reject_id}', headers={'Authorization': 'Bearer ' + data['token']})
        assert res.status_code == 200

        data = res.json()
        assert data['msg'] == 'Success'
    except Exception as e:
        print(e)
        assert 'Exception Thrown' == 'Exception Caught'