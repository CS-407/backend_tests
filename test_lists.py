import json
import requests
import pytest

login_url = 'http://localhost:8080/api/auth/login'
get_users_lists_url = 'http://localhost:8080/api/list/getLists/'
get_single_list_url = 'http://localhost:8080/api/list/get/'
update_list_url = 'http://localhost:8080/api/list/update/'

class TestTradeClass:

    def test_get_single_list_response(self):
        user = {
            'email': 'jdoe@gmail.com',
            'username': 'johndoe',
            'password': '123456',
            'id': '63f904e97833f3231394df49'
        }

        test_list = {
            "_id":"644b04266a4e316c71f3c76e",
            "list_owner": "63f904e97833f3231394df49",
            "stocksCount": 3,
            "list_name": "Testing List"
        }

        res = requests.post(url=login_url, json=user)
        assert res.status_code == 200
        data = res.json()
        assert data['token'] != None
        token = data['token']
        url = get_single_list_url + test_list['_id']
        res = requests.get(url=url, headers={'Authorization': "Bearer "+token})
        assert res.status_code == 200
        data = res.json()

        assert data['list_name'] == test_list['list_name']
        assert data['list_owner']['_id'] == test_list['list_owner']
        assert len(data['stocks']) == test_list['stocksCount']

    def test_get_users_lists_response(self):
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
        url = get_users_lists_url + user['id']
        res = requests.get(url=url, headers={'Authorization': "Bearer "+token})
        assert res.status_code == 200

    def test_update_list_response(self):
        user = {
            'email': 'jdoe@gmail.com',
            'username': 'johndoe',
            'password': '123456',
            'id': '63f904e97833f3231394df49'
        }

        test_list = {
            "_id": "644b04266a4e316c71f3c76e",
            "list_owner": {'_id':'63f904e97833f3231394df49'},
            "stocks": [ 
                {'_id': '6426185d45f9c2ebc03f9421'}, 
                {'_id': '6426185d45f9c2ebc03f9425'}, 
                {'_id': '6426186045f9c2ebc03f9435'} 
            ],
            "list_name": "Testing List"
        }

        res = requests.post(url=login_url, json=user)
        assert res.status_code == 200
        data = res.json()
        assert data['token'] != None
        token = data['token']

        url = update_list_url
        res = requests.post(url=url, headers={'Authorization': "Bearer "+token}, json=test_list)
        assert res.status_code == 200

        url = get_single_list_url + test_list['_id']
        res = requests.get(url=url, headers={'Authorization': "Bearer "+token})
        assert res.status_code == 200
        data = res.json()

        assert data['list_name'] == test_list['list_name']
        assert data['list_owner']['_id'] == test_list['list_owner']['_id']
        assert len(data['stocks']) == len(test_list['stocks'])
    
    
    