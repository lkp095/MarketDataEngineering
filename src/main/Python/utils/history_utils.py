"""
History data collector utilities
"""

from config.collector_config import HISTORY_DATA_TEMPLATE


def get_history_data(symbol):
    """
    Create history request data for a specific symbol.

    Args:
        symbol: Market symbol (e.g., 'NSE:NIFTY50-INDEX')

    Returns:
        Dictionary with history request parameters
    """
    data = HISTORY_DATA_TEMPLATE.copy()
    data["symbol"] = symbol
    return data

