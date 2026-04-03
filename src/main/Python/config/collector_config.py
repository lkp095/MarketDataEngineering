# Market Data Collector Configuration

from config.market_symbols import MARKET_SYMBOLS_STRING

# Data structure for Fyers API quotes request
QUOTES_DATA = {
    "symbols": MARKET_SYMBOLS_STRING
}

# History data template - customize symbol and resolution as needed
HISTORY_DATA_TEMPLATE = {
    "resolution": "5",
    "date_format": "1",
    "range_from": "2026-01-01",
    "range_to": "2026-03-31",
    "cont_flag": "1"
}

# Polling interval in seconds
POLLING_INTERVAL = 1
RESOLUTION = 5

# Market data file names
QUOTES_MARKET_DATA_FILE = "quotes_market_data.json"
HISTORY_MARKET_DATA_FILE = "history_market_data.csv"

# CSV column definitions for history market data
HISTORY_CSV_COLUMNS = [
    "fetched_at",
    "symbol",
    "resolution",
    "candle_epoch",
    "candle_time_utc",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "status",
    "message",
]



