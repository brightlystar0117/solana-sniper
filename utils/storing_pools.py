import sys,os,json
from utils.webhook import sendWebhook
def getPool_info(desired_token_address):
    try:
        file_path = os.path.join(sys.path[0], 'data', 'bought_tokens_info.json')
        
        # Load the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Retrieve the settings for the desired_token_address
        settings = data.get(desired_token_address)["pool"]

        if settings is not None:
            return settings

        else:
            return None
    except:
        return None



def storePool_info(desired_token_address, pool_info):
    try:
        file_path = os.path.join(sys.path[0], 'data', 'bought_tokens_info.json')

        # Load the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Append the settings to the JSON object
        data[desired_token_address]["pool"] = pool_info



        # Write the updated data back to the file
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        print("Pool saved in 'bought_tokens_info.json'.")
        sendWebhook(f"a|Token INFO SAVE {desired_token_address}", f"Pool 'bought_tokens_info.json'.")

    except:
        print("Error [storePool_info]")
