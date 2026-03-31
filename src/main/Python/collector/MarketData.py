from fyers_apiv3 import fyersModel
import os
import time
import json
from datetime import datetime

base_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(base_dir, "../../../"))
client_id_path = os.path.join(project_root, "resources/client_id.txt")
access_token_path = os.path.join(project_root, "resources/access_token.txt")

client_id = open(client_id_path, "r").read()
access_token = open(access_token_path, "r").read()


# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,is_async=False, log_path=(str(project_root) + "/resources/" ))

data = {
    "symbols":"NSE:NIFTY50-INDEX, BSE:SENSEX-INDEX"
}

market_data_path = os.path.join(project_root, "resources/market_data.json")

# Ensure file exists
if not os.path.exists(market_data_path):
    with open(market_data_path, "w") as f:
        json.dump([], f)

while True:
    response = fyers.quotes(data=data)
    print(response)


    # Read existing data
    with open(market_data_path, "r") as f:
        existing_data = json.load(f)

    # Append new response with timestamp
    existing_data.append({
        "timestamp": datetime.now().isoformat(),
        "data": response
    })

    # Write back to file
    with open(market_data_path, "w") as f:
        json.dump(existing_data, f, indent=2)

    time.sleep(1)

