# Import the required module from the fyers_apiv3 package
from fyers_apiv3 import fyersModel
import os

# Define your Fyers API credentials
client_id = "RX6ZEHRV6X-100"  # Replace with your client ID
secret_key = "5491XH3V0G"  # Replace with your secret key
redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"  # Replace with your redirect URI
response_type = "code"
grant_type = "authorization_code"


# Create a session object to handle the Fyers API authentication and token generation
session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri,
    response_type=response_type,
    grant_type=grant_type
)

generateTokenUrl = session.generate_authcode()
print("generatedTokenUrl : ", generateTokenUrl)

auth_code = input("Enter Auth Code: ")
session.set_token(auth_code)
response = session.generate_token()


try:
    access_token = response["access_token"]
    print("Access Token:", access_token)
except Exception as e:
    print("Error generating access token:", e, "Response:", response)


with open("../../../resources/client_id.txt", "w") as f:
    f.write(client_id)
with open("../../../resources/access_token.txt", "w") as f:
    f.write(access_token)


fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,is_async=False, log_path="../../../resources/")


