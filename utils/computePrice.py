from utils.checkBalance import getBalance
import re
from ast import literal_eval
from solana.transaction import Transaction
from solders.pubkey import Pubkey
from raydium.create_close_account import fetch_pool_keys, make_simulate_pool_info_instruction
import requests
import json
import os, time
from solana.rpc.core import RPCException
from solana.rpc.types import TokenAccountOpts
from utils.new_pools_list import check


import sys
from configparser import ConfigParser
from utils.logger_store import print_message


LIQUIDITY_FEES_NUMERATOR = 25
LIQUIDITY_FEES_DENOMINATOR = 10000


def calculateAmountOut(amount, pool_info):
    status = pool_info['status']
    SWAP_decimals = pool_info['coin_decimals']  # swap coin
    SOL_decimals = pool_info['pc_decimals']  # SOL
    COIN_lp_decimals = pool_info['lp_decimals']  # swap coin
    pool_SOL_amount = pool_info['pool_pc_amount']  # sol
    pool_SWAP_amount = pool_info['pool_coin_amount']  # coin
    Coin_pool_lp_supply = pool_info['pool_lp_supply']  # coin

    reserve_in = pool_SOL_amount
    reserve_out = pool_SWAP_amount

    current_price = reserve_out / reserve_in
    # print(f"Current Price in SOL: {current_price:.12f}")

    amount_in = amount * 10 ** SOL_decimals
    Fees = (amount_in * LIQUIDITY_FEES_NUMERATOR)/LIQUIDITY_FEES_DENOMINATOR
    amount_in_with_fee = amount_in - Fees
    amountOutRaw = (reserve_out * amount_in_with_fee) / \
        (reserve_in + amount_in_with_fee)
    # Slippage = 1 + slippage
    # minimumAmountOut = amountOutRaw / slippage
    return amountOutRaw / 10 ** SWAP_decimals


def calculateAmountIn(amount, pool_info):
    SWAP_decimals = pool_info['coin_decimals']  # swap coin
    SOL_decimals = pool_info['pc_decimals']  # SOL
    COIN_lp_decimals = pool_info['lp_decimals']  # swap coin
    pool_SOL_amount = pool_info['pool_pc_amount']  # sol
    pool_SWAP_amount = pool_info['pool_coin_amount']  # coin
    Coin_pool_lp_supply = pool_info['pool_lp_supply']  # coin

    reserve_in = pool_SWAP_amount
    reserve_out = pool_SOL_amount

    current_price = reserve_out / reserve_in
    # print(f"Current Price in SOL: {current_price:.12f}")

    amount_in = amount * 10 ** SWAP_decimals
    Fees = (amount_in * LIQUIDITY_FEES_NUMERATOR)/LIQUIDITY_FEES_DENOMINATOR
    amount_in_with_fee = amount_in - Fees
    amountOutRaw = (reserve_out * amount_in_with_fee) / \
        (reserve_in + amount_in_with_fee)
    # Slippage = 1 + slippage
    # minimumAmountOut = amountOutRaw / slippage
    return amountOutRaw / 10 ** SOL_decimals


def getQuoteToken(TOKEN_TO_SWAP_SELL, tokenBalanceLamports):
        config = ConfigParser()
        config.read(os.path.join(sys.path[0], 'data', 'config.ini'))
        slippageBps = int(config.get("INVESTMENT", "slippage"))

        
        while True:
            quote_response1 = requests.get('https://quote-api.jup.ag/v6/quote', params={
                'inputMint': TOKEN_TO_SWAP_SELL,
                'outputMint': 'So11111111111111111111111111111111111111112',
                'amount': tokenBalanceLamports,
                'slippageBps': slippageBps
            })
            try:
                quote_response = quote_response1.json()
                break
            except Exception as e:
                text = ("getQuoteToken at ComputePrice error because too many requests...")
                alert_type = "e|[Ignore] Jupiter"
                print_message(text,alert_type)
                time.sleep(1)

        return int(quote_response['outAmount']) / 10**9

def getBaseToken(token_address):
    url = f"https://api.dexscreener.com/latest/dex/pairs/solana/{token_address}"
    response = requests.get(url).json()
    return response['pair']['baseToken']['address']


def get_price(token_address):
    url = f"https://api.dexscreener.com/latest/dex/tokens/{token_address}"
    exclude = ['EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',
               'Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB']
    response = requests.get(url).json()

    if token_address not in exclude:
        for pair in response['pairs']:
            if pair['quoteToken']['address'] == 'So11111111111111111111111111111111111111112':
                return float(pair['priceUsd'])
    else:
        return response['pairs'][0]['priceUsd']
    return None

def PoolInfo(mint, solana_client, payer):
    while True:
        quote = ""
        if mint == 'So11111111111111111111111111111111111111112':
            pool_keys = { 
                'amm_id': Pubkey.from_string("58oQChx4yWmvKdwLLZzBi4ChoCc2fqCUWBkwMihLYQo2"),
                'authority': Pubkey.from_string("5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1"),
                'base_mint': Pubkey.from_string("So11111111111111111111111111111111111111112"),
                'base_decimals': 9,
                'quote_mint': Pubkey.from_string("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"),
                'quote_decimals': 6,
                'lp_mint': Pubkey.from_string("8HoQnePLqPj4M7PUDzfw8e3Ymdwgc7NLGnaTUapubyvu"),
                'open_orders': Pubkey.from_string("HmiHHzq4Fym9e1D4qzLS6LDDM3tNsCTBPDWHTLZ763jY"),
                'target_orders': Pubkey.from_string("CZza3Ej4Mc58MnxWA385itCC9jCo3L1D7zc3LKy1bZMR"),
                'base_vault': Pubkey.from_string("DQyrAcCrDXQ7NeoqGgDCZwBvWDcYmFCjSb9JtteuvPpz"),
                'quote_vault': Pubkey.from_string("HLmqeL62xR1QoZ1HKKbXRrdN1p3phKpxRMb2VVopvBBz"),
                'market_id': Pubkey.from_string('8BnEgHoWFysVcuFFX7QztDmzuH8r5ZFvyP3sYwn1XTh6'),
                'market_base_vault': Pubkey.from_string('CKxTHwM9fPMRRvZmFnFoqKNd9pQR21c5Aq9bh5h9oghX'),
                'market_quote_vault': Pubkey.from_string('6A5NHCj1yF6urc9wZNe6Bcjj4LVszQNj5DwAWG97yzMu'),
                'market_authority': Pubkey.from_string('CTz5UMLQm2SRWHzQnU62Pi4yJqbNGjgRBHqqp6oDHfF7'),
                'bids': Pubkey.from_string('5jWUncPNBMZJ3sTHKmMLszypVkoRK6bfEQMQUHweeQnh'),
                'asks': Pubkey.from_string('EaXdHx7x3mdGA38j5RSmKYSXMzAFzzUXCLNBEDXDn1d5'),
                'event_queue': Pubkey.from_string('8CvwxZ9Db6XbLD46NZwwmVDZZRDy7eydFcAGkXKh9axa')
            }
        else:
            pool_keys = fetch_pool_keys(mint)
        if pool_keys == 'failed':
            pool_keys = fetch_pool_keys(mint)
            if pool_keys == 'failed':
                class CustomException(Exception):
                    pass
                # Raise the custom exception
                raise CustomException("Pool Keys Not found.")
        
        if str(pool_keys['quote_mint']) == "So11111111111111111111111111111111111111112":
            quote = "SOL"
        elif str(pool_keys['quote_mint']) == "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v":
            quote = "USDC"
        elif str(pool_keys['quote_mint']) == "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB":
            quote = "USDC"
        else:
            quote = "UNKOWN"


        while True:

            try:

                recent_block_hash = solana_client.get_latest_blockhash().value.blockhash

                tx = Transaction(recent_blockhash=recent_block_hash,
                                fee_payer=payer.pubkey())

                sim_inst = make_simulate_pool_info_instruction(
                    pool_keys, mint, solana_client)

                tx.add(sim_inst)

                signers = [payer]

                tx.sign(*signers)
                res = None
                response = solana_client.simulate_transaction(tx).value.logs
                for log in response:
                    if 'Program log: GetPoolData:' in log:
                        res = log
                        break
                if res != None:
                    return res, quote
            except RPCException as e:
                print(f"[PoolInfo] - RPC - error occurred: {e}")
            except Exception as e:
                print(f"[PoolInfo] error occurred: {e}")

def get_investment_worth(ctx, payer, token_address, tokenBalanceLamports):

    res, quote_type = PoolInfo(token_address, ctx, payer)
    pool_info = literal_eval(re.search('({.+})', res).group(0))

    SWAP_decimals = pool_info['coin_decimals']  # swap coin

    mintBalance = tokenBalanceLamports / 10**SWAP_decimals

    if quote_type == "SOL":
        sol = calculateAmountIn(mintBalance, pool_info)
        return sol
    else:
        # usdt = calculateAmountIn(mintBalance, pool_info)

        # res, quote_type = PoolInfo(
        #     "So11111111111111111111111111111111111111112", ctx, payer)
        # pool_info = literal_eval(re.search('({.+})', res).group(0))

        sol = calculateAmountOut(mintBalance, pool_info)

    return sol


def getSymbol(token):

    if check(token):
        return "IGNORE", "SOL"



    # usdc and usdt
    exclude = ['EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',
               'Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB']

    if token not in exclude:
        url = f"https://api.dexscreener.com/latest/dex/tokens/{token}"

        Token_Symbol = ""
        Sol_symbol = ""
        try:
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                resp = response.json()
                print("Response:", resp['pairs'][0]['baseToken']['symbol'])
                for pair in resp['pairs']:
                    quoteToken = pair['quoteToken']['symbol']

                    if quoteToken == 'SOL':
                        Token_Symbol = pair['baseToken']['symbol']
                        Sol_symbol = quoteToken
                        return Token_Symbol, Sol_symbol

            else:
                print(f"[getSymbol] Request failed with status code {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"[getSymbol] error occurred: {e}")
        except:
            a = 1

        return Token_Symbol, Sol_symbol
    else:
        if token == 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v':
            return "USDC", "SOL"
        elif token == 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v':
            return "USDT", "SOL"
