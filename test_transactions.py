import requests
import pytest

login_url = 'http://localhost:8080/api/auth/login'
trade_url = 'http://localhost:8080/api/user/trades/63f904e97833f3231394df49'
buy_url = 'http://localhost:8080/api/stock/buy'
sell_url = 'http://localhost:8080/api/stock/sell'
balance_url = 'http://localhost:8080/api/user/getBalance'

class TestTradeClass:
    def test_valid_request(self):
        user = {
            'email': 'jdoe@gmail.com',
            'username': 'johndoe',
            'password': '123456',
        }
        res = requests.post(url=login_url, json=user)
        assert res.status_code == 200
        data = res.json()
        assert data['token'] != None
        res = requests.get(url=trade_url, headers={'Authorization': "Bearer "+data['token']})
        assert res.status_code == 200
        data = res.json()
        assert data['trades'] != None
        trades = data['trades']
        assert len(trades) >= 0

    def test_valid_buy(self):
        user = {
            'email': 'jdoe@gmail.com',
            'username': 'johndoe',
            'password': '123456',
            'id': '63f904e97833f3231394df49'
        }

        requestInfo = {
            'stock_id': '6426185d45f9c2ebc03f9421',
            'stock_price_id': '6435ad4f157882350ce5c609',
            'no_of_shares': 1,
            'amount_usd': 165.630005,
            'buy': 'true',
        }

        res = requests.post(url=login_url, json=user)
        assert res.status_code == 200
        data = res.json()
        assert data['token'] != None
        token = data['token']

        res = requests.get(url=trade_url, headers={'Authorization': "Bearer "+token})
        assert res.status_code == 200
        data = res.json()
        prev_trades = data['trades']
        prev_trades_count = len(prev_trades)

        res = requests.post(url=buy_url, headers={'Authorization': "Bearer "+token}, data=requestInfo)
        assert res.status_code == 200
        
        new_res = requests.get(url=trade_url, headers={'Authorization': "Bearer "+token})
        assert res.status_code == 200
        new_data = new_res.json()
        new_trades = new_data['trades']
        new_trades_count = len(new_trades)

        assert new_trades_count == prev_trades_count + 1
    
    def test_valid_sell(self):
        user = {
            'email': 'jdoe@gmail.com',
            'username': 'johndoe',
            'password': '123456',
            'id': '63f904e97833f3231394df49'
        }

        requestInfo = {
            'stock_id': '6426185d45f9c2ebc03f9421',
            'stock_price_id': '6435ad4f157882350ce5c609',
            'no_of_shares': 1,
            'amount_usd': 165.630005,
            'buy': 'false',
        }

        res = requests.post(url=login_url, json=user)
        assert res.status_code == 200
        data = res.json()
        assert data['token'] != None
        token = data['token']

        res = requests.get(url=trade_url, headers={'Authorization': "Bearer "+token})
        assert res.status_code == 200
        data = res.json()
        prev_trades = data['trades']
        prev_trades_count = len(prev_trades)

        res = requests.post(url=buy_url, headers={'Authorization': "Bearer "+token}, data=requestInfo)
        assert res.status_code == 200
        
        new_res = requests.get(url=trade_url, headers={'Authorization': "Bearer "+token})
        assert res.status_code == 200
        new_data = new_res.json()
        new_trades = new_data['trades']
        new_trades_count = len(new_trades)

        assert new_trades_count == prev_trades_count + 1

    def test_buy_balance_update(self):
        user = {
            'email': 'jdoe@gmail.com',
            'username': 'johndoe',
            'password': '123456',
            'id': '63f904e97833f3231394df49'
        }

        requestInfo = {
            'stock_id': '6426185d45f9c2ebc03f9421',
            'stock_price_id': '6435ad4f157882350ce5c609',
            'no_of_shares': 1,
            'amount_usd': 165.630005,
            'buy': 'true',
        }

        res = requests.post(url=login_url, json=user)
        assert res.status_code == 200
        data = res.json()
        assert data['token'] != None
        token = data['token']

        res = requests.get(url=balance_url, headers={'Authorization': "Bearer "+token})
        assert res.status_code == 200
        data = res.json()
        prev_balance = data['balance']

        res = requests.post(url=buy_url, headers={'Authorization': "Bearer "+token}, data=requestInfo)
        assert res.status_code == 200

        res = requests.get(url=balance_url, headers={'Authorization': "Bearer "+token})
        assert res.status_code == 200
        data = res.json()
        new_balance = data['balance']

        assert new_balance == prev_balance - requestInfo['amount_usd']

    def test_sell_balance_update(self):
        user = {
            'email': 'jdoe@gmail.com',
            'username': 'johndoe',
            'password': '123456',
            'id': '63f904e97833f3231394df49'
        }

        requestInfo = {
            'stock_id': '6426185d45f9c2ebc03f9421',
            'stock_price_id': '6435ad4f157882350ce5c609',
            'no_of_shares': 1,
            'amount_usd': 165.630005,
            'buy': 'false',
        }

        res = requests.post(url=login_url, json=user)
        assert res.status_code == 200
        data = res.json()
        assert data['token'] != None
        token = data['token']

        res = requests.get(url=balance_url, headers={'Authorization': "Bearer "+token})
        assert res.status_code == 200
        data = res.json()
        prev_balance = data['balance']

        res = requests.post(url=sell_url, headers={'Authorization': "Bearer "+token}, data=requestInfo)
        assert res.status_code == 200

        res = requests.get(url=balance_url, headers={'Authorization': "Bearer "+token})
        assert res.status_code == 200
        data = res.json()
        new_balance = data['balance']

        assert new_balance == prev_balance + requestInfo['amount_usd']
    
    def test_buy_sell_combined(self):
        user = {
            'email': 'jdoe@gmail.com',
            'username': 'johndoe',
            'password': '123456',
            'id': '63f904e97833f3231394df49'
        }

        requestInfo = {
            'stock_id': '6426185d45f9c2ebc03f9421',
            'stock_price_id': '6435ad4f157882350ce5c609',
            'no_of_shares': 1,
            'amount_usd': 165.630005,
            'buy': 'true',
        }

        res = requests.post(url=login_url, json=user)
        assert res.status_code == 200
        data = res.json()
        assert data['token'] != None
        token = data['token']

        res = requests.get(url=balance_url, headers={'Authorization': "Bearer "+token})
        assert res.status_code == 200
        data = res.json()
        prev_balance = data['balance']

        res = requests.get(url=trade_url, headers={'Authorization': "Bearer "+token})
        assert res.status_code == 200
        data = res.json()
        prev_trades = data['trades']
        prev_trades_count = len(prev_trades)

        res = requests.post(url=buy_url, headers={'Authorization': "Bearer "+token}, data=requestInfo)
        assert res.status_code == 200

        requestInfo['buy'] = 'false'
        res = requests.post(url=sell_url, headers={'Authorization': "Bearer "+token}, data=requestInfo)
        assert res.status_code == 200

        res = requests.get(url=balance_url, headers={'Authorization': "Bearer "+token})
        assert res.status_code == 200
        data = res.json()
        new_balance = data['balance']

        new_res = requests.get(url=trade_url, headers={'Authorization': "Bearer "+token})
        assert res.status_code == 200
        new_data = new_res.json()
        new_trades = new_data['trades']
        new_trades_count = len(new_trades)

        assert new_balance == prev_balance
        assert new_trades_count == prev_trades_count + 2

    def test_larger_than_balance(self):
        user = {
            'email': 'jdoe@gmail.com',
            'username': 'johndoe',
            'password': '123456',
            'id': '63f904e97833f3231394df49'
        }

        amount = 165.630005 * 1000000

        requestInfo = {
            'stock_id': '6426185d45f9c2ebc03f9421',
            'stock_price_id': '6435ad4f157882350ce5c609',
            'no_of_shares': 1000000, # much larger than balance
            'amount_usd': amount,
            'buy': 'true',
        }

        res = requests.post(url=login_url, json=user)
        assert res.status_code == 200
        data = res.json()
        assert data['token'] != None
        token = data['token']

        res = requests.get(url=balance_url, headers={'Authorization': "Bearer "+token})
        assert res.status_code == 200
        data = res.json()
        prev_balance = data['balance']

        res = requests.get(url=trade_url, headers={'Authorization': "Bearer "+token})
        assert res.status_code == 200
        data = res.json()
        prev_trades = data['trades']
        prev_trades_count = len(prev_trades)

        res = requests.post(url=buy_url, headers={'Authorization': "Bearer "+token}, data=requestInfo)
        assert res.status_code == 400 # Request should fail

        res = requests.get(url=balance_url, headers={'Authorization': "Bearer "+token})
        assert res.status_code == 200
        data = res.json()
        new_balance = data['balance']

        new_res = requests.get(url=trade_url, headers={'Authorization': "Bearer "+token})
        assert res.status_code == 200
        new_data = new_res.json()
        new_trades = new_data['trades']
        new_trades_count = len(new_trades)

        assert new_balance == prev_balance
        assert new_trades_count == prev_trades_count
