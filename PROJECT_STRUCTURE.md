# Market Data Engineering - Modularized Project Structure

## Overview
This project has been modularized for better maintainability and code organization.

## Directory Structure

```
src/main/Python/
├── config/                    # Configuration files
│   ├── __init__.py
│   ├── fyers_config.py       # Fyers API credentials configuration
│   └── collector_config.py   # Market data collector configuration
│
├── utils/                     # Utility modules
│   ├── __init__.py
│   ├── path_utils.py         # Path management utilities
│   └── token_utils.py        # Token save/load utilities
│
├── authenticator/             # Authentication module
│   ├── __init__.py
│   ├── Auth.py               # Main authentication entry point
│   └── fyers_authenticator.py # FyersAuthenticator class
│
├── collector/                 # Data collection module
│   ├── __init__.py
│   └── MarketData.py         # Market data collection script
│
└── resources/                 # Runtime resources (created at runtime)
    ├── client_id.txt
    ├── access_token.txt
    ├── market_data.json
    ├── fyersApi.log
    └── fyersRequests.log
```

## Key Features

### 1. **Modularized Configuration** 
   
#### `config/fyers_config.py`
   - Centralized storage of Fyers API credentials
   - Easy to update credentials in one place
   
#### `config/collector_config.py`
   - Market data symbols configuration
   - Polling interval settings
   - File names for data storage
   - Add new configurations here as needed

### 2. **Utility Modules** (`utils/`)
   - **path_utils.py**: Dynamic path resolution for project files
   - **token_utils.py**: Token persistence (save/load)

### 3. **Authentication Module** (`authenticator/`)
   - **FyersAuthenticator**: Encapsulates the OAuth2 flow
   - Handles token generation and storage
   - Clean step-by-step authentication process
   - **Prints authorization URL** for manual auth code entry

### 4. **Data Collection** (`collector/`)
   - Uses modularized utilities for configuration and token management
   - Simplified code with dependencies handled by utilities

## Usage

### Authentication

Run the authentication script to generate access tokens:

```bash
cd src/main/Python
python authenticator/Auth.py
```

This will:
1. **Print the authorization URL** to the console
2. Prompt you to visit the URL and authorize the application
3. Wait for you to **manually enter the auth code**
4. Generate and save the access token to `src/resources/`

### Data Collection

Run the market data collector:

```bash
cd src/main/Python
python collector/MarketData.py
```

This will:
1. Load tokens from `src/resources/`
2. Connect to Fyers API
3. Collect market data and save to `market_data.json`

## Configuration

### Updating Fyers API Credentials

Edit `src/main/Python/config/fyers_config.py`:

```python
FYERS_CLIENT_ID = "YOUR_CLIENT_ID"
FYERS_SECRET_KEY = "YOUR_SECRET_KEY"
FYERS_REDIRECT_URI = "https://trade.fyers.in/api-login/redirect-uri/index.html"
```

### Updating Market Data Collector Configuration

Edit `src/main/Python/config/collector_config.py`:

```python
# Add or modify market symbols
MARKET_DATA_SYMBOLS = "NSE:NIFTY50-INDEX, BSE:SENSEX-INDEX"

# Change polling interval (in seconds)
POLLING_INTERVAL = 1

# Change output file name
MARKET_DATA_FILE = "market_data.json"
```

## Benefits

1. **No Hardcoded Paths**: All paths are computed dynamically
2. **Reusable Utilities**: Token and path utilities are easily reusable
3. **Centralized Config**: All credentials in one configuration file
4. **Clean Separation**: Authentication, collection, and utilities are separated
5. **Easy Maintenance**: Updates to paths or config only need to be made in one place
6. **Manual Auth Flow**: Authorization URL is printed; you provide auth code manually

