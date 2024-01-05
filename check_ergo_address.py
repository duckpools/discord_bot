import requests

def check_ergo_address(address):
    try:
        # Fetching the transaction history for the address
        response = requests.get(f"https://api.ergoplatform.com/api/v1/addresses/{address}/transactions?limit=5")
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
    address_list = [
    "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'
    ]
    # Check if the address of the first input (index 1) is in the address list
    if len(tx["inputs"]) > 1:  # Ensure there is at least two inputs to avoid index error
        return tx["inputs"][1]["address"] in address_list
    else:
        return False

def is_repayment_tx(tx):
    address_list = [
    "YFWk9RGcvBZWrfRvAHd9uRQWrdW42fTb1TNhJDAoVCQgASqQmhdVB287nhHKGY5toAFQWUVuYGe5G7CAeqpNNAsDvEKeZLXTK6WAS7SBDp51Gt7LGubSe7KvK6X3hi6WwN6SSJ4DXpZ85gnmSPH9heL9TxW1GPjtNtijMGmeh87ozqQ3QERx1o7QAYKf3UiJWth8jbCq7qt5pkEQNZzihkTf1KFXKLFP5xbGXWBLwzJMvAF7Ubpna2oPoXN4phAyyRXQQDtN",
    "r5zW3yf5B6ZghtHxnav9bFnQrebMKQKZQnvbkMwnTuoPp8wyvH9zoykUxkLquJkBUUsZie2Gc3Fs2rUQ2vV9ghvCfYx78bN2f2qcb9pFZoysqfuRfQs8w9rVMyDoWQ7qSWajedPzHbXpQaLTWNdJuTsuYN824KaFrrdqauhk7GQoegTmhq9tXDjTnMXXnRUxzxdcBjZfJM36XYu2kLf8ZsK3q5A7Mz9N6oa7Gg21qYpSmS4EJcagqDk8kinGmu9i6RYeXDnT6cxyd2w2eBmGy5Nd3JKzvPcy2DVRk9Th1yXhgztKu5dqkN7MW9oxA94eUgR3P2drbn4arGQiYc7",
    "r5zW3yf5BQiSNLp7zap6YGx4YVNY3wezAaUWTVkwNhK5228SgvZ3oUJ3iEQqi5D6Gn9Kc9Stfji1gkdXovyCzWyd6cn9AiVfz6mzuLU3D8qTwQp83GUJNtvpBdsizYjugY8ZWVWWNAhN4wEhgPKoo1PXi9JV4WnGu4cuMRWdpG7qzh7cHM2qdUvXZjJ7B66yirMUFZEdwHDqpWZsSTe2pxRWm7Kc71cUCo8bjG2JNuiFutBameVTTbKBUDH33XwNn1aDhzQj7gNQbVXuVvygdjGyk1PFfm3oP5W97RkFH9riGiQz9Tinxq75yogf6SY7db34xC4oqXPoZ3qCqtB",
    'r5zW3yf5Cp6PAiK1cgDEj9k4tExPLMR9jAFGR1QXD3NtVvAhRDLgyGCGn82JJwzgV7v41zaN3NmoWDrk2nH5SiQGE4pafSc9aWBWDn256v2iZWrU6rPGbxbs3arTMHL4rxq3DW5qQ31TUU9MGcRaq2dt2nUdWLoQNp1LLDrtsNM57ToLd3VV3WnBEPzHjq64xvb1MoyME2QaCNGUH6vsQw2a51YZAUajC2T7M38RQ3mNsD9nfp7WgikTuJrK9WRqRNXBXPy8mrSWGSthCo5cyQKjs9NVtBcaFMsuiCTqYGJRT1SySxcKF1fPAYjoCf7uTHE5WKkTZkz39jPmZK6',
    'r5zW3yf589G7zj8Yfw45X8TkWiJnUV1SHvhWaUwPpC4Um4WrF26DBNNYqkoSStYVjju3DX9u1GaaUVKnAPE6hFVxX2Xkt6bcygdPaEsAimCoYZrALq8LbrX8WXHnM5CChUvBXsjKZyPqqZThb5efbuSwgn8GeR2RkHGkT9CUtQrd6RN4Wn2buX55zNmaoUDVrdi5c8t3rJbERYy4S2pwn4i8xbAnCquNS65jk6J26EP3Lzs7yxqfiXBXJW37LDDwANwKchUJmzXfx2kkSB5XLSycYMRZZ2rSyyw4esZdUrtQZdiRBsyKP37rbmsU4Qjs6zkbRXijBbTAks2YmWA'
    ]
    # Check if the address of the first input (index 1) is in the address list
    if len(tx["inputs"]) > 1:  # Ensure there is at least two inputs to avoid index error
        return tx["inputs"][1]["address"] in address_list
    else:
        return False



def get_ergo_network_height():
    """
    This function calls the Ergo platform API to get the current network state
    and returns the height of the blockchain.
    """
    url = "https://api.ergoplatform.com/api/v1/networkState"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            height = data.get("height")
            return height
        else:
            return f"Error: Unable to access the API. Status code {response.status_code}"
    except Exception as e:
        return f"Error: {e}"
