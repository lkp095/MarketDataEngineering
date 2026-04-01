"""
Fyers API Authenticator Module
Handles authentication and token generation for Fyers API
"""

from fyers_apiv3 import fyersModel
from config.fyers_config import (
    FYERS_CLIENT_ID, FYERS_SECRET_KEY, FYERS_REDIRECT_URI,
    FYERS_RESPONSE_TYPE, FYERS_GRANT_TYPE
)
from utils.path_utils import get_resources_path
from utils.token_utils import save_tokens


class FyersAuthenticator:
    """Handles Fyers API authentication"""
    
    def __init__(self):
        self.client_id = FYERS_CLIENT_ID
        self.secret_key = FYERS_SECRET_KEY
        self.redirect_uri = FYERS_REDIRECT_URI
        self.response_type = FYERS_RESPONSE_TYPE
        self.grant_type = FYERS_GRANT_TYPE
        self.session = None
        self.access_token = None
    
    def generate_auth_url(self):
        """Generate authentication URL"""
        self.session = fyersModel.SessionModel(
            client_id=self.client_id,
            secret_key=self.secret_key,
            redirect_uri=self.redirect_uri,
            response_type=self.response_type,
            grant_type=self.grant_type
        )
        auth_url = self.session.generate_authcode()
        print("=" * 80)
        print("Authorization URL:")
        print(auth_url)
        print("=" * 80)
        return auth_url
    
    def set_auth_code(self, auth_code):
        """Set the authorization code"""
        if self.session is None:
            raise RuntimeError("Session not initialized. Call generate_auth_url() first.")
        self.session.set_token(auth_code)
    
    def generate_access_token(self):
        """Generate access token using auth code"""
        if self.session is None:
            raise RuntimeError("Session not initialized. Call generate_auth_url() first.")
        
        response = self.session.generate_token()
        
        try:
            self.access_token = response["access_token"]
            print("Access Token generated successfully!")
            return self.access_token
        except Exception as e:
            print(f"Error generating access token: {e}")
            print(f"Response: {response}")
            raise
    
    def save_tokens(self):
        """Save tokens to resources folder"""
        if self.access_token is None:
            raise RuntimeError("Access token not generated. Call generate_access_token() first.")
        save_tokens(self.client_id, self.access_token)
    
    def get_fyers_model(self):
        """Get initialized FyersModel instance"""
        if self.access_token is None:
            raise RuntimeError("Access token not available.")
        
        resources_path = get_resources_path()
        fyers = fyersModel.FyersModel(
            client_id=self.client_id,
            token=self.access_token,
            is_async=False,
            log_path=resources_path
        )
        return fyers

