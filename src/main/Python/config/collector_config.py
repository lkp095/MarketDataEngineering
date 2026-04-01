# Market Data Collector Configuration

from config.market_symbols import MARKET_SYMBOLS_STRING

# Data structure for Fyers API quotes request
QUOTES_DATA = {
    "symbols": MARKET_SYMBOLS_STRING
}

# Polling interval in seconds
POLLING_INTERVAL = 1

# Market data file name
MARKET_DATA_FILE = "market_data.json"

