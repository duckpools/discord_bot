import requests

def check_ergo_address(address):
    try:
        # Fetching the transaction history for the address
        response = requests.get(f"https://api.ergoplatform.com/api/v1/addresses/{address}/transactions?limit=10")
        response.raise_for_status()

        data = response.json()
        transactions = data.get('items', [])

        # Extracting transaction IDs from the transaction history
        transaction_ids = [tx['id'] for tx in transactions]
        return transaction_ids

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def get_transaction_details(tx_id):
    try:
        response = requests.get(f"https://api.ergoplatform.com/api/v1/transactions/{tx_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching transaction details: {e}")
        return None


def is_borrow_tx(tx):
    return tx["inputs"][1]["address"] == "2Cw4JJbBRQxr8WQACzNu8k6kAKwpLGRxy5uAXndZYmQb1ktpNAxFi5B1gjQX4z5tgifqyZQiAuojorsZhpgCG9hDyAjTjtVzwPhnrydKGNS7ivz5tiuqWdmwRx1Uun2AUHSkKhRuCsJEKDfPBCjc7RzmfqaADbVniDPLePUs9y7mYFM9AxPUzhNnEoRaqjjWkWU7uAzWcihArG2bvk8Lhneqdoda537M7HsMfzuYw1FL6zX6jqgWzsZ2ZJ3g78sVmVAtd2YwPSeQE6j4s41md9FRto689WtVtLrbLc6Q6es5M9svvBqP8CUXetR9zYQ67HBpJJ73Rumg6JJxLr9MuDZUiEnioNYsyqpAAxr9p1uBqrUaTkfVLfBBDxJLEtTHhp2JthXweqXrixmwubyESLkGtrvv2uX2cVZGevNgRKVmdnoyP4WFScDdgoKogcGoPCPQZ6vNVxpqgJXEq3TJkP4DK7ndQWWKB8mQCBBor7yrJ6xnXg1oPvkT5HDZE3V94GzzUH5PY3MJ79pHZto3MB4v961KZ5B6iXGdeVHVQFedC3xMYDxBQQAbFzVTWWTen8yKbiP"

def is_repayment_tx(tx):
    return tx["inputs"][1]["address"] == "YFWk9RGcvBZWrfRvAHd9uRQWrdW42fTb1TNhJDAoVCQgASqQmhdVB287nhHKGY5toAFQWUVuYGe5G7CAeqpNNAsDvEKeZLXTK6WAS7SBDp51Gt7LGubSe7KvK6X3hi6WwN6SSJ4DXpZ85gnmSPH9heL9TxW1GPjtNtijMGmeh87ozqQ3QERx1o7QAYKf3UiJWth8jbCq7qt5pkEQNZzihkTf1KFXKLFP5xbGXWBLwzJMvAF7Ubpna2oPoXN4phAyyRXQQDtN"
