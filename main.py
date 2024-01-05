import discord
import asyncio
from check_ergo_address import check_ergo_address, get_transaction_details, is_borrow_tx, is_repayment_tx, get_ergo_network_height
import random

intents = discord.Intents.default()
intents.messages = True 

client = discord.Client(intents=intents)

async def monitor_ergo_address(channel, address, token_name, decimal):
    last_transactions = set(check_ergo_address(address))
    await asyncio.sleep(random.randint(0, 20))
    while True:
        try:
            current_transactions = set(check_ergo_address(address))
            new_transactions = current_transactions - last_transactions

            for tx_id in new_transactions:
                tx_details = get_transaction_details(tx_id)
                if tx_details:
                    height = int(get_ergo_network_height())
                    txHeight = int(tx_details["outputs"][0]["settlementHeight"]) 
                    if (txHeight > height - 10):
                        message = analyze_transaction(tx_details, token_name, decimal)
                        await channel.send(f'{message}')

            last_transactions = current_transactions
            await asyncio.sleep(random.randint(60, 100))  # Check every 60 seconds
        except Exception as e:
            print(f"An error occurred: {e}")
            await asyncio.sleep(5)  # Short delay before restarting the task


def analyze_transaction(tx_details, token_name, decimal):
    if (token_name == "ERG"):
        # Extract ERGs from the first input and output
        input_ergs = tx_details["inputs"][0]["value"]
        output_ergs = tx_details["outputs"][0]["value"]

        # Calculate the difference and convert from nanoErgs to Ergs
        ergs_difference = int((output_ergs - input_ergs) / 10**(decimal - 2))

        # Round the difference to 2 decimal places
        ergs_difference_rounded = abs(ergs_difference / 10**2)

        if (is_borrow_tx(tx_details)) :
            return f":pray: **Funds Borrowed from the {token_name} Pool** \n\n**Amount Borrowed:** {ergs_difference_rounded} {token_name} \n**Transaction Link:** (https://explorer.ergoplatform.com/en/transactions/{tx_details['id']})"
        elif (is_repayment_tx(tx_details)):
            borrowed = tx_details["inputs"][1]["assets"][0]["amount"]
            repayment = tx_details["inputs"][1]["value"]

            profit = int((repayment - borrowed) / 10**(decimal-2))
            profit_rounded = abs(profit / 10**2)
            return f":moneybag: **Repayment Made to the {token_name} POOL** \n\n**Amount Repaid: **{tokens_difference_rounded} {token_name} \n**Pool Profit: **{profit_rounded} {token_name} \n**Transaction Link:** (https://explorer.ergoplatform.com/en/transactions/{tx_details['id']})"
        else:
            if (ergs_difference > 0):
                return f":money_with_wings: **{token_name} Lent to the {token_name} Pool** \n\n **Amount Lent: **{ergs_difference_rounded} {token_name} \n **Transaction Link:** (https://explorer.ergoplatform.com/en/transactions/{tx_details['id']})"
            else:
                return f":shopping_bags: **{token_name} Withdrawn out of {token_name} ERG Pool** \n\n **Amount Withdrawn: **{ergs_difference_rounded} {token_name} \n **Transaction Link:** (https://explorer.ergoplatform.com/en/transactions/{tx_details['id']})"
    else:
        input_tokens = tx_details["inputs"][0]["assets"][3]["amount"]
        output_tokens = tx_details["outputs"][0]["assets"][3]["amount"]

        # Calculate the difference
        tokens_difference = int((output_tokens - input_tokens) / 10**(decimal - 2))

        # Round the difference to 2 decimal places
        tokens_difference_rounded = abs(tokens_difference / 10**2)

        if (is_borrow_tx(tx_details)) :
            return f":pray: **Funds Borrowed from the {token_name} Pool** \n\n**Amount Borrowed:** {tokens_difference_rounded} {token_name} \n**Transaction Link:** (https://explorer.ergoplatform.com/en/transactions/{tx_details['id']})"
        elif (is_repayment_tx(tx_details)):
            borrowed = tx_details["inputs"][1]["assets"][0]["amount"]
            repayment = tx_details["inputs"][1]["assets"][1]["amount"]

            profit = int((repayment - borrowed) / 10**(decimal-2))
            profit_rounded = abs(profit / 10**2)

            return f":moneybag: **Repayment Made to the {token_name} POOL** \n\n**Amount Repaid: **{tokens_difference_rounded} {token_name} \n**Pool Profit: **{profit_rounded} {token_name} \n**Transaction Link:** (https://explorer.ergoplatform.com/en/transactions/{tx_details['id']})"
        else:
            if (tokens_difference > 0):
                return f":money_with_wings: **{token_name} Lent to the {token_name} Pool** \n\n **Amount Lent: **{tokens_difference_rounded} {token_name} \n **Transaction Link:** (https://explorer.ergoplatform.com/en/transactions/{tx_details['id']})"
            else:
                return f":shopping_bags: **{token_name} Withdrawn out of {token_name} ERG Pool** \n\n **Amount Withdrawn: **{tokens_difference_rounded} {token_name} \n **Transaction Link:** (https://explorer.ergoplatform.com/en/transactions/{tx_details['id']})"


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    channel = client.get_channel(1172477858380251228)
    address = '6Q6fbqfbMAogw42DWDtKuKt9frSKdqW92cmiPbeF2SnuYCS9Ca43ZAiJvR7Kj4ZW8yyTnsEY4Np82vF4BDrStxi7PkyGhvppdoWVV2Th3ALS38sWtvYqhso3fx9Ehwbodv36y7ytNZfJitGgx586NsXgZhn3hCVZdUq694vdDRWCyAJygAsu2hHaieTm1F7ZgGufrccYezPtDv3WjGiRZsENiPCheAJ8uEZVN6rnatXhvDhuZgd2ghhzxi4WxmTMSW2C8eZJukqxcqD9D8Jd21b4PYcPBMtqsWACPpKproeRiVZynvDsCKMx1HnZiY8JXSk3qvwtZmxSn5nw2GtKnfXGV4pjHHSr7mpKysayFxKxdWuFJ47S29SRqw8pL2bk4Us9haR6BbDR6uintCUVZ7Q2LAsMmkWwmKFw3fEhBKeq1hWgDAASSuUWXm6ZbYi4XLXchXjYEmWsZ6mYWnBW3QPK5iezrZiefP11GCohrbEtMLTQ1UvX2UchTr3mDqy7zQdJJLSC8Wnc7dEGYF59VJG3iT5aCFyBR1qxVdmyjUaEYDLmxuVS87HbmXoSBpi4jSHPGt2sLtNTKBpa7q7A7qvyGGAaxoPuPrtkuA8aV32vDfsvDSBWCVGN9zVpVBi95UV8G4mVHMKCAngRzNK93obXoWdZUe2y7QfZTHNY935zthiA2eWUiz8eRvGrbVTo2veXN3g1iYtBtmUez5CPDuFt4MdJeYyPY54idD6qPHVw8Kqnxs1QVK92qZCAGjjDqcLJwTC6kDhT3e6mJdrdmoCGuufj9KsNyzXwtwVo6wVVw8ZxJdRCf8c6cjEmSSS7SJWgwmgGMiPiQeo486mnzW4Pb9q3tdBAw78pttaFdvwp4iVFdWjkdgz8AxW8LLnjqjVY6aTrpFbVMk4nLbjR7zj7AtUNP75M55R2QKVtxyLvmw648ZmtgUAaXFxDCZEevVs2x7KotXtcY9zM74cGbgcM1ukwDVnzrQuGi3T6QBiFbWPxYjVKXVHhni5F1j8qK13XPCkwNRxD65xjKNcMekPyXDqTBLrx6avkSCodPvDPzVJJcmvzPuhdaTzEKy1pDy8h9khMDAW49VnAbzFpHv7o6WwSTyqMmipDcj8fdpL2wNkxCtuVUt4CQnthC8nusoCnyCxXboHdpMe4ebhcigSYbYPr3D3kkYoqFrBRqGs4aLuMsdYQ2xB7CeAf5EiNYurAFCtuUCy7Y8bFbdzs6XbG7wAoCGFZEd4Z1xsNNpSyWzy8TqE69yySKzNJ7FdmTbdVdUrKMjrv8DZt9sSuVL6RxnoV4DYsTeJRf3C2Z3ppsYuSqPaJwPtTqEzW4nRtHQ7v9yXFUAmHdGTsf5vnDcBa6dLHkhiQwpp8hU43qVj6CpftjsyJuqpWNfZ9QmHafy5PvyD6PmbPHey3knKuCoFKje8HbtB6e4Lt8wigxyThiRjyex93K1a9SixyfsXAH2sva7J5RCduZiwcrUPEKSU8eroSizXqAjpGm621AKidzMqVCYdgM1yvD6PhpbyYGLDqEBoMz6Y9hgpuDpK5skh1r3agNz23j5eVFxXoQ2ooEbNsxHGLgmmQcPHTA6YWs44Pdw9wGEqhZKBW79nqtfY97NxaVF6MFDx9WRcxiRsg63AWKRJfjVFLrZDyDzLJHxDKdEzwQFbdnB4pyfF2w7YD4bMTKqQFuegEwcgBWcziTctEeyMjtd8YB2dG2e6D5oJa38mnw5QyLLSugbFbyFV8a'  # Replace with the Ergo address you want to monitor
    client.loop.create_task(monitor_ergo_address(channel, address, "SigUSD", 2))
    address = '3F9bBReNRNpy8HU2PNNRbCdHgzj6F5WgDmKSRAg7bkW3qaJ3VrjQkfqX5W8zDRuUTRJfpt56L1mpx1V7Pt5Bo9QtT7HVQBWqRoUvTVcTkTRsPHRR363M14WsjKXfqPLvauS7BvwtggxXA8S6TTW4gArraoqauhfvyCzjHPNmmfEDypY2wvvMsYNW3VRQYCK8eDNLmdsQwvtGbULeeMdKXCvyH68CpAayLhuVbALRkKCyvdQvAz3gr3yxqNcrScFPxYwE61521iVGwJjfNdXPnHmkespPtM9hhj2qh7HdsAmbQUAJenRpD6RCN2pSh7aQUUZiQENbTxVmiJkqENs99yTv8aHmGFWsw2WQcwVH394M1Sj5ue1CCJYHg6N6FyCXyptsVSqvBG1scmUPqbPneQDCvS2xHgBd1HCrUram8mgD9GewBehXJXa5TL8fe5G2XnGtLukkqfJfmRRmwvjCxEcYv65gAsGW6xxy6YgGm3VxzDUdTnHisGYf3qFnEKkiZf6stFRWPNRcJmRh5jKHqVHjEWMQgdqRjv44qT4zKG6ewUYjubGhHjVy7qedLUnDvM1X7P1CCankPJzDJuZJqnefRrbcuNcP5Fawx2E2NdihRbiAKbA6g3RuNuS2WEPEkQUs7rKGT1fgDw41hq8LaoSf35Xax6eopjzEGLRKYyXqWb7yQfPVNebnYVxbXbRg5aVqHLyiJ4h5sqAdSm2QUjD1oMKuYmbqbqCsYfp2oxJKcL5i7JLnvEKSP23YmsN9Va4SAmmWj4VwiqexH1DGR2pt78LPpWgK2EtHN2gLk9KFnGmK8ZVZG2yx2taH6JXoZXieXarGkBPJrHyB4ZzB1K2pftLwk6vyvSVmfqz2VSi2Lc6NPyLiJ7eKdpbMFaZYm39FkhgCy5Wc7Be7Yqvd7RRVDhx6K9jS4YwPN8aCn24jtKXMs8T6orwxS3tFQR2cCMwqkFuLthR9PUVwX6wiEZ7qNc2p9eCQ7hcqSSAEnqg4teua4GLWtqYFeG1uebJERSBbgjEptrKswnPhzvcdabrwsMopBvknjzjdawW96fqgraPBhbcKDo172x6rFtJnmYrLd9mfNww1twDy43Nz6xGyP31u15Vjqr17g7tdd8sKHPjHFZX37RXquKf5k1i2DdXtcjmAWmuACe1QtfBitqJNwRbMe4RxgLk5doDX1tNfQMQdS1i94RSRrmMaRZUSndJZGPXxVjX6YcjXmVFarb8S9EkkC4jSm6SsHu5aHYG351kTP2mv3fHohRwNrqKkKpvxw1qe9QgYHDufFMYZb88SmmsBLnLGy6rsdurvdqdqWJFbxYvxmRumeSY3H69C3R8pbdrWjSLwxJTy6F2yQ4SQTBuwGpRuD7hcnKt84ajhNsFc4Fmzp8Zn8j9Tg3FSXR4M68bf1ABwnkKPBLdHmEe1qD4qYhGWd73SJVnHarpfyK2Gc1rXTrwCw6kqJRoQesNWQrgxbdGmm1aawJ1Pasks2pBd5118zKPHi2Wi8mCRepWKzv6oJjbWBiZtzrC6kEPXS8S7g9XpiGSFCSfK8aiHHYdHn8iAyuZeA2Yne4DmHZdys85gAh5hjjaPPYuMTHmCr4WbrNfMegX7oDyh7yrhV2sPbgRq7d75eXwpNW9Q5fs4xBqDbeJA1o26yCx7fkQ6yKs8DaWcgv9cFoJB1GA4V3izUpejSw1wqRR3tpMHT1LfB5GpJGoSXGkFQ9Mybt'  # Replace with the Ergo address you want to monitor
    client.loop.create_task(monitor_ergo_address(channel, address, "ERG", 9))
    address = '4z9dZrkxdYok1tkUF56Emr1XAzzi7VY8rTzxZ4qtv7VACufMJDQmbBVsgAjVhJ16AmnaMHLwMFoPYKUG3zL1d5Z17AHK6oGL2vxjkLxoEACbfMBMCaaMSiiZeZ36dGLbX1PAL3Lv4u2A7XfuZzd73QRG65t3v32S1hjSeamo4JBkY5hE2tGEwR9DaFkMn32Vh4PYYHm4aMBw9kCSxmkBZDvVYgf8yMTqz8UGyRDYFMFovuZhY2KTvYNrbQyUtQkbJ2Crn7ZmXfWbGV2FNNEwEfVTeNLVBLNky8sreH9XKFv9iASZ1Avd6RNHuBuSBh9aHdvABZwuZhaDBjKwzvUKwV9GTdzgeLb36naha5AxNVXwB2HMtUpeuG8fQ8btcpyrSYoUJSFFvoqhf1EBAWas251Wng4QQ4TdmCJfZWzrTK1NbEWX1dMYCm1pR4mUqNiKDyE5Ec5ftcRxv2N8jA8dErpYdSdT9g1v1sYBYsBn35zsFaHryxkYLTsSpyrSRzvWJXBxZQdPvztTFSxuyH4WMttUPFNDW567wZfco9u51VV3TYAbxLdn9JfQwmAHCwsBeAyGPrRLhpsEabGcVQSNs8ZTiRq9g7SuVKFBHHuCUnGqWkvV4DVyKHkwG6qT5Un1UxT9WZpuz89fFFT4Htd5DptFUQw2MqrZTSTrv9BEqGCy1WF54KnP4HHjzHsh9b4N8Fwbt1BQc5oHMnXbiAWYWy6z1qqBPUnGXUwG1k5mpDo8GWjJQQnHT5M6zaQaCZLmbANKmPtNsX3u7niy2WV5d9yMphoS4vU73ii6P9FPURxarfJ2oN19Zj9YTHaMY3b9bgF5P1U8gUUjZQ5dv2DTs7qULbRSwYNVaBUiX22yxycZu9j8dXMnzz49M5sdjuM8RjHyUAYUGGmFNsUVJkd3rotRNQr7QWaSpdQsZoVhALmTeSenXXMiBvGZu5jBMCmuR6GNNEbsQyWyoYyvCVAvTaUcmbjMBykNxmxCU7qUiY7E41S7RraDcVwk9dHZn17QXbsFCoU2UDyXZ6oHNxW76fx9UqL8Xdh3YpiUemGuhwansbwroycsZcqfWhvEtDre3Xrbtav91tPdwsFTVqt9yBGEZPNygQ6EkutVM99L36Uuwxxx6r8wph9iNg5cWZpefegJttkwzFEy1MLSWjmnhbgxDpxPfDGCGCEqBwMa5iNePBsLS7fhFdcn9VBrccozBSnrbD44g1TzNkb5yGRHMUrJ5KEYu7QtgxpfCAbjwxadgF3iaHhzDLW9Y9DHpVQTTTFTToRGYF6JdeTJt1LQDHMxTy11DmS1m3Pvk4bWSrcirVgxtb7Q97dz9fz1UHFETEYVHiVTjQzBYPYKvuWp8EDfjpuEksAAUzJHkKTukLoQE7AKCc9K78UQPG8kf8pbUj2zpVMUgEDdTwfk8pVUdjYNxL4sj3QBibPGs7CkziwFPgrJU8HsaXMXdMUPwW2Z718YN3mxVHiu7qiRdqFrjcAbVUiQsrsXRoHQyXowUAQLyQsWDCLUKBu1WoTe76xh4GDHsVKrCa6DgLeZhrTFnMay81J6TGJL9awQFG1pbrM9hCPQY9rn8K4gXskzMGiEgb3wsFfGu4KbfKL1dHsFiRdBgur5H6ccKRezb2bscw3rZKhU36c3igZnEsAmtnYCNQBySgS11rFr4tQdq8sr3gcN43GjrAgiFMFEcEAQGnD5ksjVEdCcttXFgJFCWkqapQyvEt4vALU3xYM5BEaQmdEJpHv2gsCvfAjT'  # Replace with the Ergo address you want to monitor
    client.loop.create_task(monitor_ergo_address(channel, address, "SigRSV", 0))
    address = '6Q6fbqfbMAogw42DWDtKuKt9frSKdqW92cmiPbeF2SnuYCS9Ca43ZAiJvR7KjbKursffXBwTuRfRyvZv7D9fr288gd6ctQSU55V7jg4xeGy77VHcxUAqQqMqMy7v9FspKJ3wUv5sBDfqXaL7iX6JvvjwcRmRNtkk7Es7zmVKVvcrizZoher8GdkGkt5oWeF4pzeDcUk7dLiQUPEVhYe6Qi3o2eqdba1xH5pbX1TXssdHnQNwV4qUDfQjq2xzQkCizu7ByHfsp3E8jZiQXzpNDbar6kdVc6kYUmYuVsMNR7qCQ3tHKi8wcKkamWUq7upVBxfYBcej76SyWFr3AVwYDykf8tY7qf1KeCUHP7eRtEnpDy2StzMQXVr6XQSJKXA7n6L75Xqgc8H2fua7XkhEwgYiFTQArRyq41y7eQ6Ra7kjMjtSBxLoAGXPdKoQQTJqrmxRrFnei3vMPZfXpjcMtYgw83epZj8WdCGxWU3kcadLG627HM8U7rpyS5gvxUUoAakM2AwANvPJ2aRKAVPBrvfGTgEXMYgJ2LQvmNoF8924nFjXgJc8dwgPwVLrbZioSbacixWsdAT1arPzF3JyYJNimfJFRyAXEqmpP9iDF5WfvdjCuUxnJqAQTwTGDu1L2hxXxhHgVfzoqTgxcqwJ1Rt1wbrHo55J2ZaNxMbh6urtSXEU5rvxL6uAW49H51KJ8Dn6Jg98WAcdvv5oww1QevXuqSyqmQdwkKE96MzZXZYsv4dXoJWHVfFS2FknRxqFbDMk4tz8LH7eXrse7s2ggyfxwX5AQA9ynbwUrSn4PpzCjXezva5sA9Dkjy5bVRRLViTpAkKjKQD7Xn2KqJ1MjThf8xr4m7yeMHnYBaPWxPVhQsQpNU2EW6ZuFbmz8mLtaadVXphfwEgxeezopehtA8T2CnaJbFgWxv1NmcMDFi9oE6SEEBNzQi2bQwvprqAGQuPCBAAezUPWZ2pnesG5TW7Xu5btujKCN3RzmtzBm6gDEEkt2a4Rxk8GBMoB2TysAgiGgJJxkEPiRpZNzbmMwn6ah8Z1z5iiRPY5TSEjHbdA1qgyNTbR91JUajZCafnkjCQtkzKf36r7h9nRx6PTJCM51tziffqhLu3wqhwHbu6wz97PtkA3FeC5bmpWEoDeEE4dSbZ836aigMiATYZmgyj4LEyGpqoiRxPT9R6cStdNN8MwUpVTCne72zbGSfnVChGuKXH5oGpoZHPwD7MdQRY8FGyNKzBfrjvxEnXczTm8J2WEA882ExDZQdDDAmUmhAkTkRLBQFcPb3NEk6B7AJyshAHN5ThvjqJnbKEiNoCFr3nXBN4YcV3QymB9soR7N2b5rRWdgPCdHT731AW8mMP3Gjra93chsyRMMAGtquveWYWZ7ESXFLTkZTYtCskWDEZzezyFtgQ1tSnAsqetspa9NKxXSy8cb88YvwPeJk191AdPRTAZLNjYwdC5NzRyxsC897HKjXzkkvrC72SZQtJSyifb3R1Lzd92y3ic1JxAimDy92EQDiHY1hZ5yKRiJJZfkPfjDgxqnMCHRXXu7nxwFRRCeEkeUs7VafTYfYQurhoBnxg7Pzi6NAdohtmaEVo1DeKFBec1axcDLPGs9jzQEBYR3nkxJEuCGwDEJEKCm2142vA6uXvJ91Y22A6bkBEdmcAsotitHk6EMcq4YkUAmko9GnDXdTgTtu3bjRrEwiqQxb6d3pFE2jXMwoMR35bntspPQMMi7pCJYtqM6x2NT'  # Replace with the Ergo address you want to monitor
    client.loop.create_task(monitor_ergo_address(channel, address, "QUACKS", 6))
    address = 'uNSWCGrJoB8w8CD4eBFT28pcoDd3q9sGHYFrQXZc9GSeb8nP2TEGuDtMf17W4J9BogDHNYFYrXdskbbbhxMxYM3Yp4sK6b6qhqPS4DNb4vB73Jy8NCMcbaoUcFfQLcKm4nPkCpFdwdo9n7GzKEECFFXe6FiDFbnoEtqkTsseg88zDcZmVdanXvMa7fL6yJoYppQBBH1XPtjHzSqpg7m8iThpfjjp1Wi1yGbewpFsvZ5roq3TzU8Jk928fgUBWa8MnHConNXAai7FJTo5w9EXuEhXoLhmgoCbJSMrgR5diTNYHm17FGd6mU1dTnRpk1dvx7TjpCz9cadJQw6DHfGjprdiLjkkdjcjnpUrpMdBjBrCf5CgjdH7VkC3RtudksekKNGAHaV46nx4yChvPXJSDmRjY8zPrXruzPqfJgXnajRcKJ2PW6uA7bx8yXVEAwhCFhyAxfGkab2FycXhSi4hQWJoQRETDpj5SvNRxE86aL5GdXYzQs9zbd1rqWAr9sqQ7tGTwh9TLmSMsLDmU7z9RoqpYEacLJvPYdMRD2EJYJVGN9XFHcnUcAGQNxDx7bks4opAtFvTQpX5SUHog6WNMsbwP5sRJGMN4Tm4yszqVvQAiPATDBmtQLVwqG13aan5bp87noNVr9vBZraLoEtuEuLqD1foBgN5NF5yTUJgoA5RSQhiquCr98tpZWivCeFoFVLTYknBfejLULv4faTUTPAp4KztNdeMqkYcDhjqTRFko7Lbf2XsUxeaYDvotcLn3hmgeJsr45SwbrUyDtsFtVuwPjis1vJiWwyNwF4WJiP4XrgEVJpNNXGMZJjpYZ7cNZx5Eary3LCKegMwDus4j1WUhxEW7q5BowgGuFwsncWpFBXPpbJeuBu3tbsXfyrDxQFHYVoLyGRDb2bJjazAWVY3eVNMNsxLk4aBiNMstfAynGngbw8r7hw5vhMWLL7S2CaBrz5ELbVZRowvBgDXc7Xxx6XiMN1x6KZhSU8gFHjAuzggHNo5WEfg9bE4G5qUsdpbsF29iorGCxyKFNiWfVriELMGBo4vgmvEwoPft2yREQjay4U5se4GWT7SBmYN7cWmM9c5qQzzQtVP78Xht13wH93QmVh6NDXb8hCC8p3vgR34ejXuCuXiLd1h52EVxcn7zUUHLmvEo4JaivGuPZgWHeeu6r7kg5nhBrzWkmvVXpiTbdEvMFvsh6vgMamytw6EtJuDBpKuk3xHrdBEHaoWLDBqxNL7TeewnK4qipPiJsszNtbuwkHpkYSMzaC9Yjs6AoKEPL2cpg28dJkXmA7gsC8g8fxxZL3GkhraLGpKPKotbEQNWaNo7AuZyGYEwaFdfkrGXLY5BBTNaYpyEYk6qaUk3oemvaA9TPZnijqbcU5W1YenQkHsh1Qbw2V36SX3qLrzwNVqvurDysRs9MjymKG1SgWfdi5Ti9dFcCW7DU3xtkrKdzXnsJoDbAfcZkqn3iczDVx119Y8QVDMrubAJFPqTCvKYNsZtQTe5Qw33D7YYb6Q6CW6SuVCXS9VAV9LwmYdbdRzU2bVQ1yuxby6NAhN4WX2evNv4PLowM3DfURPKVDV6js7zJ2b1SDFg445mLkhDac4RWTmCtPmze5wAtV2y3hoS9mTQtiHHftmNhroSJZW4eKpFZvm2jzT5QCttvxnoxZGSNfy6dmQbprDNYZfGkEJoCASooctFH1MEr8gP8P1XnC8Q183XUveQsXyad7Pfbew1t5TseXWuDrb9gcusmVVaH'  # Replace with the Ergo address you want to monitor
    client.loop.create_task(monitor_ergo_address(channel, address, "RSN", 3))



client.run('')
