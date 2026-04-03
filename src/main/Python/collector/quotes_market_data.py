"""
Quotes market data collector - fetches real-time quotes for all enabled symbols
and persists to JSON file. Runs continuously as a daemon.
"""

import sys
import os
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.logger import get_logger
from utils.api_client import initialize_fyers_client
from utils.json_handler import ensure_json_file, append_json_row
from utils.quotes_utils import parse_quotes_response
from config.collector_config import (
    QUOTES_DATA,
    POLLING_INTERVAL,
    QUOTES_MARKET_DATA_FILE,
)

logger = get_logger(__name__)

def main():
    """Main function to collect and persist quotes data continuously."""
    try:
        # Initialize Fyers API client
        fyers, resources_path = initialize_fyers_client()
        logger.info("Fyers API client initialized successfully")

        # Set up JSON file path
        market_data_path = os.path.join(resources_path, QUOTES_MARKET_DATA_FILE)
        ensure_json_file(market_data_path)
        logger.info(f"JSON file initialized: {market_data_path}")

        logger.info("Starting quotes data collection (continuous daemon)")
        logger.info(f"Polling interval: {POLLING_INTERVAL} second(s)")

        iteration = 0
        total_records = 0

        while True:
            iteration += 1
            logger.debug(f"Iteration {iteration}")

            try:
                # Fetch quotes data
                response = fyers.quotes(data=QUOTES_DATA)
                logger.debug(f"Response: {response}")

                # Parse and persist data
                if (parsed_data := parse_quotes_response(response)):
                    append_json_row(
                        market_data_path,
                        parsed_data["timestamp"],
                        parsed_data["data"],
                    )
                    total_records += 1
                    logger.info(f"Data appended (total: {total_records})")
                else:
                    logger.warning("Failed to parse quotes response")

            except Exception as e:
                logger.error(f"Error fetching quotes: {e}", exc_info=True)

            # Wait before next fetch
            logger.debug(f"Waiting {POLLING_INTERVAL} second(s) before next fetch...")
            time.sleep(POLLING_INTERVAL)

    except KeyboardInterrupt:
        logger.info("Shutdown signal received")
        logger.info(f"Total iterations: {iteration}")
        logger.info(f"Total records collected: {total_records}")
        logger.info(f"Data saved to: {market_data_path}")
    except Exception as e:
        logger.critical(f"Critical error in quotes data collector: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()

