import discord
import asyncio
from check_ergo_address import check_ergo_address, get_transaction_details, is_borrow_tx, is_repayment_tx

intents = discord.Intents.default()
intents.messages = True 

client = discord.Client(intents=intents)

async def monitor_ergo_address(channel, address):
    last_transactions = set()
    while True:
        current_transactions = set(check_ergo_address(address))
        new_transactions = current_transactions - last_transactions

        for tx_id in new_transactions:
            tx_details = get_transaction_details(tx_id)
            if tx_details:
                message = analyze_transaction(tx_details)
                await channel.send(f'{message}')

        last_transactions = current_transactions
        await asyncio.sleep(60)  # Check every 60 seconds

def analyze_transaction(tx_details):
    # Extract ERGs from the first input and output
    input_ergs = tx_details["inputs"][0]["value"]
    output_ergs = tx_details["outputs"][0]["value"]

    # Calculate the difference and convert from nanoErgs to Ergs
    ergs_difference = int((output_ergs - input_ergs) / 10000000)

    # Round the difference to 2 decimal places
    ergs_difference_rounded = abs(ergs_difference / 100)


    if (is_borrow_tx(tx_details)) :
        return f":pray: **Funds Borrowed from the ERG Pool** \n\n**Amount Borrowed:** {ergs_difference_rounded} ERG \n**Transaction Link:** (https://explorer.ergoplatform.com/en/transactions/{tx_details['id']})"
    elif (is_repayment_tx(tx_details)):
        return f":white_check_mark: **Repayment Made to the ERG POOL** \n\n**Amount Repaid: **{ergs_difference_rounded} ERG \n**Transaction Link:** (https://explorer.ergoplatform.com/en/transactions/{tx_details['id']})"
    else:
        if (ergs_difference > 0):
            return f":money_with_wings: **ERG Lent to the ERG Pool** \n\n **Amount Lent: **{ergs_difference_rounded} ERG \n **Transaction Link:** (https://explorer.ergoplatform.com/en/transactions/{tx_details['id']})"
        else:
            return f":shopping_bags: **ERG Withdrawn out of the ERG Pool** \n\n **Amount Withdrawn: **{ergs_difference_rounded} ERG \n **Transaction Link:** (https://explorer.ergoplatform.com/en/transactions/{tx_details['id']})"


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    channel = client.get_channel(1172439284666601572)
    address = '3F9bBReNRNpy8HU2PNNRbCdHgzj6F5WgDmKSRAg7bkW3qaJ3VrjQkfqX5W8zDRuUTRJfpt56L1mpx1V7Pt5Bo9QtT7HVQBWqRoUvTVcTkTRsPHRR363M14WsjKXfqPLvauS7BvwtggxXA8S6TTW4gArraoqauhfvyCzjHPNmmfEDypY2wvvMsYNW3VRQYCK8eDNLmdsQwvtGbULeeMdKXCvyH68CpAayLhuVbALRkKCyvdQvAz3gr3yxqNcrScFPxYwE61521iVGwJjfNdXPnHmkespPtM9hhj2qh7HdsAmbQUAJenRpD6RCN2pSh7aQUUZiQENbTxVmiJkqENs99yTv8aHmGFWsw2WQcwVH394M1Sj5ue1CCJYHg6N6FyCXyptsVSqvBG1scmUPqbPneQDCvS2xHgBd1HCrUram8mgD9GewBehXJXa5TL8fe5G2XnGtLukkqfJfmRRmwvjCxEcYv65gAsGW6xxy6YgGm3VxzDUdTnHisGYf3qFnEKkiZf6stFRWPNRcJmRh5jKHqVHjEWMQgdqRjv44qT4zKG6ewUYjubGhHjVy7qedLUnDvM1X7P1CCankPJzDJuZJqnefRrbcuNcP5Fawx2E2NdihRbiAKbA6g3RuNuS2WEPEkQUs7rKGT1fgDw41hq8LaoSf35Xax6eopjzEGLRKYyXqWb7yQfPVNebnYVxbXbRg5aVqHLyiJ4h5sqAdSm2QUjD1oMKuYmbqbqCsYfp2oxJKcL5i7JLnvEKSP23YmsN9Va4SAmmWj4VwiqexH1DGR2pt78LPpWgK2EtHN2gLk9KFnGmK8ZVZG2yx2taH6JXoZXieXarGkBPJrHyB4ZzB1K2pftLwk6vyvSVmfqz2VSi2Lc6NPyLiJ7eKdpbMFaZYm39FkhgCy5Wc7Be7Yqvd7RRVDhx6K9jS4YwPN8aCn24jtKXMs8T6orwxS3tFQR2cCMwqkFuLthR9PUVwX6wiEZ7qNc2p9eCQ7hcqSSAEnqg4teua4GLWtqYFeG1uebJERSBbgjEptrKswnPhzvcdabrwsMopBvknjzjdawW96fqgraPBhbcKDo172x6rFtJnmYrLd9mfNww1twDy43Nz6xGyP31u15Vjqr17g7tdd8sKHPjHFZX37RXquKf5k1i2DdXtcjmAWmuACe1QtfBitqJNwRbMe4RxgLk5doDX1tNfQMQdS1i94RSRrmMaRZUSndJZGPXxVjX6YcjXmVFarb8S9EkkC4jSm6SsHu5aHYG351kTP2mv3fHohRwNrqKkKpvxw1qe9QgYHDufFMYZb88SmmsBLnLGy6rsdurvdqdqWJFbxYvxmRumeSY3H69C3R8pbdrWjSLwxJTy6F2yQ4SQTBuwGpRuD7hcnKt84ajhNsFc4Fmzp8Zn8j9Tg3FSXR4M68bf1ABwnkKPBLdHmEe1qD4qYhGWd73SJVnHarpfyK2Gc1rXTrwCw6kqJRoQesNWQrgxbdGmm1aawJ1Pasks2pBd5118zKPHi2Wi8mCRepWKzv6oJjbWBiZtzrC6kEPXS8S7g9XpiGSFCSfK8aiHHYdHn8iAyuZeA2Yne4DmHZdys85gAh5hjjaPPYuMTHmCr4WbrNfMegX7oDyh7yrhV2sPbgRq7d75eXwpNW9Q5fs4xBqDbeJA1o26yCx7fkQ6yKs8DaWcgv9cFoJB1GA4V3izUpejSw1wqRR3tpMHT1LfB5GpJGoSXGkFQ9Mybt'  # Replace with the Ergo address you want to monitor
    client.loop.create_task(monitor_ergo_address(channel, address))



client.run('')
