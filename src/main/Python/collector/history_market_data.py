"""
History market data collector - fetches OHLCV candle data from Fyers API
for all enabled symbols and persists to CSV file.
"""

import sys
import os
from datetime import datetime, timezone

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.logger import get_logger
from utils.api_client import initialize_fyers_client
from utils.csv_handler import ensure_csv_file, epoch_to_utc_iso, append_csv_rows
from utils.history_utils import get_history_data
from config.collector_config import ( HISTORY_DATA_TEMPLATE, HISTORY_MARKET_DATA_FILE, HISTORY_CSV_COLUMNS,)
from config.market_symbols import MARKET_SYMBOLS_LIST

logger = get_logger(__name__)


def parse_candles(response, symbol, resolution):
    """
    Parse Fyers history API response and extract candle rows.

    Args:
        response: API response dictionary
        symbol: Market symbol string
        resolution: Candle resolution string

    Returns:
        List of row tuples ready for CSV writing
    """
    rows = []
    fetched_at = datetime.now(timezone.utc).isoformat()

    if not isinstance(response, dict):
        logger.error(f"Unexpected response for {symbol}. Expected dictionary.")
        return rows

    candles = response.get("candles", [])
    status = response.get("s", "")
    message = response.get("message", "")
    resolution_str = str(resolution)

    # If no candles, still log the response status
    if not isinstance(candles, list) or not candles:
        rows.append((
            fetched_at,
            symbol,
            resolution_str,
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            status,
            message,
        ))
        return rows

    # Parse each candle row
    for candle in candles:
        if not isinstance(candle, (list, tuple)) or len(candle) < 6:
            continue

        epoch, open_price, high, low, close, volume = candle[:6]
        rows.append((
            fetched_at,
            symbol,
            resolution_str,
            epoch,
            epoch_to_utc_iso(epoch),
            open_price,
            high,
            low,
            close,
            volume,
            status,
            message,
        ))

    return rows


def main():
    """Main function to collect and persist history data for all symbols."""
    try:
        # Initialize Fyers API client
        fyers, resources_path = initialize_fyers_client()
        logger.info("Fyers API client initialized successfully")

        # Set up CSV file path
        market_data_path = os.path.join(resources_path, HISTORY_MARKET_DATA_FILE)
        ensure_csv_file(market_data_path, HISTORY_CSV_COLUMNS)
        logger.info(f"CSV file initialized: {market_data_path}")

        resolution = HISTORY_DATA_TEMPLATE.get("resolution", "5")

        # Fetch history data for each enabled symbol
        logger.info(f"Fetching history for {len(MARKET_SYMBOLS_LIST)} enabled symbols...")
        total_rows = 0

        for symbol in MARKET_SYMBOLS_LIST:
            logger.info(f"Fetching {symbol}...")
            try:
                # Create request data for this symbol
                request_data = get_history_data(symbol)

                # Fetch history data
                response = fyers.history(data=request_data)
                logger.debug(f"Response for {symbol}: {response}")

                # Parse and persist rows
                rows = parse_candles(response, symbol, resolution)
                if rows:
                    append_csv_rows(market_data_path, rows)
                    total_rows += len(rows)
                    logger.info(f"Appended {len(rows)} rows for {symbol}")
                else:
                    logger.warning(f"No rows to append for {symbol}")
            except Exception as e:
                logger.error(f"Error fetching {symbol}: {e}", exc_info=True)

        logger.info(f"Total rows appended: {total_rows}")
        logger.info(f"Data saved to: {market_data_path}")

    except Exception as e:
        logger.critical(f"Critical error in history data collector: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()


