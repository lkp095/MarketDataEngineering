import os
from config.fyers_config import (
    FYERS_CLIENT_ID, FYERS_SECRET_KEY, FYERS_REDIRECT_URI,
    FYERS_RESPONSE_TYPE, FYERS_GRANT_TYPE
)
from utils.path_utils import get_resources_path, ensure_resources_dir_exists

def save_tokens(client_id, access_token):
    """Save client_id and access_token to resources folder"""
    resources_path = ensure_resources_dir_exists()
    
    client_id_path = os.path.join(resources_path, "client_id.txt")
    access_token_path = os.path.join(resources_path, "access_token.txt")
    
    with open(client_id_path, "w") as f:
        f.write(client_id)
    
    with open(access_token_path, "w") as f:
        f.write(access_token)
    
    print(f"Tokens saved to {resources_path}")

def load_tokens():
    """Load client_id and access_token from resources folder"""
    resources_path = get_resources_path()
    
    client_id_path = os.path.join(resources_path, "client_id.txt")
    access_token_path = os.path.join(resources_path, "access_token.txt")
    
    if not os.path.exists(client_id_path) or not os.path.exists(access_token_path):
        raise FileNotFoundError("Token files not found in resources folder")
    
    with open(client_id_path, "r") as f:
        client_id = f.read().strip()
    
    with open(access_token_path, "r") as f:
        access_token = f.read().strip()
    
    return client_id, access_token

