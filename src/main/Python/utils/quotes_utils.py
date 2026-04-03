"""
Quotes market data collector utilities
"""

from datetime import datetime


def parse_quotes_response(response):
    """
    Parse Fyers quotes API response and return formatted data with timestamp.

    Args:
        response: API response dictionary from fyers.quotes()

    Returns:
        Dictionary with timestamp and response data, or None if invalid
    """
    if not isinstance(response, dict):
        print("Error: Unexpected quotes response format. Expected dictionary.")
        return None

    return {
        "timestamp": datetime.now().isoformat(),
        "data": response
    }

