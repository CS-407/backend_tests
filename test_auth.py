import requests
import pytest

login_url = 'http://localhost:5000/api/auth/login'
signup_url = 'http://localhost:5000/api/auth/signup'

class TestSignupClass:
    def test_valid_signup(self):
        user = {
            'email': 'jdoe@gmail.com',
            'username': 'johndoe',
            'password': '123456',
            'password2': '123456'
        }

        try:
            res = requests.post(url=signup_url, json=user)
            data = res.json()

            if (res.status_code == 200):
                assert data['token'] != None
                assert data['user'] != None
            else:
                assert data['msg'] == 'User already exists'
        except:
            assert pytest.raises(Exception)
    
    def test_existing_user(self):
        user = {
            'email': 'jdoe@gmail.com',
            'username': 'johndoe',
            'password': '123456',
            'password2': '123456',
        }

        try:
            res = requests.post(url=signup_url, json=user)

            assert res.status_code == 401
        
            data = res.json()

            assert data['msg'] == 'User already exists'
        except:
            assert pytest.raises(Exception)

    def test_invalid_email(self):
        user = {
            'email': 'jdoe@gmail',
            'username': 'johndoe',
            'password': '123456',
            'password2': '123456'
        }

        try:
            res = requests.post(url=signup_url, json=user)

            assert res.status_code == 400

            data = res.json()

            assert len(data) == 1

            assert data[0]['param'] == 'email'
            assert data[0]['msg'] == 'Invalid value'
        except:
            assert pytest.raises(Exception)

    def test_invalid_password(self):
        user = {
            'email': 'jdoe@gmail.com',
            'username': 'johndoe',
            'password': '1234',
            'password2': '1234'
        }

        try:
            res = requests.post(url=signup_url, json=user)

            assert res.status_code == 400

            data = res.json()
            
            assert len(data) == 1

            assert data[0]['param'] == 'password'
            assert data[0]['msg'] == 'Invalid value'
        except:
            assert pytest.raises(Exception)

    def test_mismatching_passwords(self):
        user = {
            'email': 'jdoe@gmail.com',
            'username': 'johndoe',
            'password': '1234567',
            'password2': '1234568'
        }

        try:
            res = requests.post(url=signup_url, json=user)

            assert res.status_code == 401

            data = res.json()

            assert data['msg'] == 'Passwords do not match'
        except:
            assert pytest.raises(Exception)

class TestLoginClass:
    def test_valid_login(self):
        user = {
            'email': 'jdoe@gmail.com',
            'password': '123456'
        }

        try:
            res = requests.post(url=login_url, json=user)

            assert res.status_code == 200

            data = res.json()

            assert data['token'] != None
            assert data['user'] != None
        except:
            assert pytest.raises(Exception)

    def test_non_existing_user(self):
        user = {
            'email': 'nonexistentuser@gmail.com',
            'password': '123456'
        }

        try:
            res = requests.post(url=login_url, json=user)

            assert res.status_code == 404

            data = res.json()

            assert data['msg'] == 'User not found'
        except:
            assert pytest.raises(Exception)

    def test_invalid_email(self):
        user = {
            'email': 'invalid@emailformat',
            'password': '123456'
        }

        try:
            res = requests.post(url=login_url, json=user)

            assert res.status_code == 400

            data = res.json()

            assert len(data) == 1

            assert data[0]['param'] == 'email'
            assert data[0]['msg'] == 'Invalid value'
        except:
            assert pytest.raises(Exception)

    def test_invalid_password(self):
        user = {
            'email': 'validemail@gmail.com',
            'password': '1234'
        }

        try:
            res = requests.post(url=login_url, json=user)

            assert res.status_code == 400

            data = res.json()

            assert len(data) == 1

            assert data[0]['param'] == 'password'
            assert data[0]['msg'] == 'Invalid value'
        except:
            assert pytest.raises(Exception)

    def test_incorrect_password(self):
        user = {
            'email': 'jdoe@gmail.com',
            'password': '1234756'
        }

        try:
            res = requests.post(url=login_url, json=user)

            assert res.status_code == 401

            data = res.json()

            assert data['msg'] == 'Password incorrect'
        except:
            assert pytest.raises(Exception)