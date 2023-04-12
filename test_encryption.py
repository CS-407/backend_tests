import requests
import pytest

def test_signup():
    signup_url = 'http://localhost:5000/api/auth/signup'
    user = {
        'email': 'smith65@gmail.com',
        'username': 'samsmith',
        'password': '123456',
        'password2': '123456'
    }

    try:
        res = requests.post(url=signup_url, json=user)

        assert res.status_code == 200

        data = res.json()

        assert data['token'] != None
        assert data['user']['password'] != user['password']
    except:
        assert 'Exception Thrown' == 'Exception Caught'

def test_valid_login():
    login_url = 'http://localhost:5000/api/auth/login'
    user = {
        'email': 'smith65@gmail.com',
        'password': '123456'
    }

    try:
        res = requests.post(url=login_url, json=user)

        assert res.status_code == 200

        data = res.json()

        assert data['token'] != None
        assert data['user'] != None
    except:
        assert 'Exception Thrown' == 'Exception Caught'

def test_invalid_login():
    login_url = 'http://localhost:5000/api/auth/login'
    user = {
        'email': 'smith65@gmail.com',
        'password': '1234576'
    }

    try:
        res = requests.post(url=login_url, json=user)

        assert res.status_code == 401

        data = res.json()
        assert data['msg'] == 'Password incorrect'
    except:
        assert 'Exception Thrown' == 'Exception Caught'