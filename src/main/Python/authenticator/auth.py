"""
Main authentication script for Fyers API
This script handles the OAuth2 authentication flow with Fyers
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from authenticator.fyers_authenticator import FyersAuthenticator


def main():
    """Main authentication flow"""
    print("=" * 80)
    print("Fyers API Authentication")
    print("=" * 80)
    
    # Initialize authenticator
    auth = FyersAuthenticator()
    
    # Step 1: Generate authorization URL
    print("\n[Step 1] Generating authorization URL...")
    auth.generate_auth_url()
    
    # Step 2: Get auth code from user
    print("\n[Step 2] Please visit the URL above and authorize the application.")
    auth_code = input("\nEnter the Authorization Code: ").strip()
    
    # Step 3: Set auth code
    print("\n[Step 3] Setting authorization code...")
    auth.set_auth_code(auth_code)
    
    # Step 4: Generate access token
    print("\n[Step 4] Generating access token...")
    auth.generate_access_token()
    
    # Step 5: Save tokens
    print("\n[Step 5] Saving tokens...")
    auth.save_tokens()
    
    print("\n" + "=" * 80)
    print("Authentication completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    main()



