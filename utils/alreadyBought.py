import os, sys, json

from utils.webhook import sendWebhook
from utils.birdeye import getSymbol


"""
check if token exists in the file
"""
# def check_if_already_bought(token_address):
def check_token_existence(token_to_check):
    
    if getSettings(token_to_check) != None:
        return True
    return False


"""
Store token data from the file
"""
def storeSettings(amm,
                  desired_token_address,
                  txB,
                  execution_time,
                  limit_order_sell_Bool,
                  take_profit_ratio,
                  trailing_stop_Bool,
                  trailing_stop_ratio,
                  Limit_and_Trailing_Stop_Bool,
                  bought_token_price,
                  invest_amount_sol):
    
    token_symbol, _ = getSymbol(desired_token_address)

    file_path = os.path.join(sys.path[0], 'data', 'bought_tokens_info.json')

    # Define the settings
    settings = {
         'amm': amm,
            'txB': str(txB),
            'invest_amount_sol' : invest_amount_sol,
            'execution_time': execution_time,
            'limit_order_sell_Bool': limit_order_sell_Bool,
            'take_profit_ratio': take_profit_ratio,
            'trailing_stop_Bool': trailing_stop_Bool,
            'trailing_stop_ratio': trailing_stop_ratio,
            'Limit_and_Trailing_Stop_Bool': Limit_and_Trailing_Stop_Bool,
            'NEW_POOL': bought_token_price
    }


    # Load the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Append the settings to the JSON object
    data[desired_token_address] = settings

    # Write the updated data back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    print("Settings saved in 'bought_tokens_info.json'.")
    sendWebhook(f"a|Token INFO SAVE {token_symbol}", f"Settings saved in 'bought_tokens_info.json'.")



"""
Delete token data from the file
"""
def soldToken(desired_token_address):
    print("Deleting saved token from bought_tokens_info...")
    file_path = os.path.join(sys.path[0], 'data', 'bought_tokens_info.json')
    # Load the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Check if the 'desired_token_address' key exists in the JSON object
    if desired_token_address in data:
        # If it exists, delete it
        del data[desired_token_address]

    # Write the updated data back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)





"""
get token data from the file
"""
def getSettings(token):
    file_path = os.path.join(sys.path[0], 'data', 'bought_tokens_info.json')
    
    # Load the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Retrieve the settings for the desired_token_address
    settings = data.get(token)

    if settings is not None:
        print(f"Settings Retrieved for {token}")
        return settings

    else:
        return None

