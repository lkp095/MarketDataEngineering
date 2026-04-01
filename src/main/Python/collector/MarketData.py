import sys
import os
import time
import json
from datetime import datetime
from fyers_apiv3 import fyersModel

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.path_utils import get_resources_path
from utils.token_utils import load_tokens
from config.collector_config import QUOTES_DATA, POLLING_INTERVAL, MARKET_DATA_FILE

# Load tokens from resources
client_id, access_token = load_tokens()
resources_path = get_resources_path()

# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, is_async=False, log_path=resources_path)


market_data_path = os.path.join(resources_path, MARKET_DATA_FILE)

# Ensure file exists
if not os.path.exists(market_data_path):
    with open(market_data_path, "w") as f:
        json.dump([], f)

while True:
    response = fyers.quotes(data=QUOTES_DATA)
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

    time.sleep(POLLING_INTERVAL)
