import json
import requests
import pytest

login_url = 'http://localhost:8080/api/auth/login'
get_profilePic = 'http://localhost:8080/api/user/getProfilePic/'
update_profilePic = 'http://localhost:8080/api/user/updateProfilePic/'


class TestTradeClass:

    def test_get_profilePic(self):
        user = {
            'email': 'jdoe@gmail.com',
            'username': 'johndoe',
            'password': '123456',
            'id': '63f904e97833f3231394df49'
        }

        res = requests.post(url=login_url, json=user)
        assert res.status_code == 200
        data = res.json()
        assert data['token'] != None
        token = data['token']

        url = get_profilePic
        res = requests.get(url=url, headers={'Authorization': "Bearer "+token})
        assert res.status_code == 200
        data = res.json()
        assert data['data'] >= 1 and data['data'] <= 5

    def test_update_profilePic(self):
        user = {
            'email': 'jdoe@gmail.com',
            'username': 'johndoe',
            'password': '123456',
            'id': '63f904e97833f3231394df49'
        }

        new_profilePic = 3

        res = requests.post(url=login_url, json=user)
        assert res.status_code == 200
        data = res.json()
        assert data['token'] != None
        token = data['token']

        url = update_profilePic + str(new_profilePic)
        res = requests.post(url=url, headers={'Authorization': "Bearer "+token})
        assert res.status_code == 200
        data = res.json()

        url = get_profilePic
        res = requests.get(url=url, headers={'Authorization': "Bearer "+token})
        assert res.status_code == 200
        data = res.json()
        assert data['data'] == new_profilePic

    def test_update_profilePic_valid(self):

        user = {
            'email': 'jdoe@gmail.com',
            'username': 'johndoe',
            'password': '123456',
            'id': '63f904e97833f3231394df49'
        }

        res = requests.post(url=login_url, json=user)
        assert res.status_code == 200
        data = res.json()
        assert data['token'] != None
        token = data['token']

        url = get_profilePic
        res = requests.get(url=url, headers={'Authorization': "Bearer "+token})
        assert res.status_code == 200
        data = res.json()
        assert data['data'] >= 1 and data['data'] <= 5

    def test_update_profilePic_invalid(self):
        user = {
            'email': 'jdoe@gmail.com',
            'username': 'johndoe',
            'password': '123456',
            'id': '63f904e97833f3231394df49'
        }

        new_profilePic = 10 # Invalid profilePic

        res = requests.post(url=login_url, json=user)
        assert res.status_code == 200
        data = res.json()
        assert data['token'] != None
        token = data['token']

        url = get_profilePic
        res = requests.get(url=url, headers={'Authorization': "Bearer "+token})
        assert res.status_code == 200
        data = res.json()
        prev_profilePic = data['data']

        url = update_profilePic + str(new_profilePic)
        res = requests.post(url=url, headers={'Authorization': "Bearer "+token})
        assert res.status_code == 500
        data = res.json()

        url = get_profilePic
        res = requests.get(url=url, headers={'Authorization': "Bearer "+token})
        assert res.status_code == 200
        data = res.json()
        assert data['data'] == prev_profilePic