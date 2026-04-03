"""
Common API client initialization utilities
"""

from fyers_apiv3 import fyersModel

from utils.path_utils import get_resources_path
from utils.token_utils import load_tokens


def initialize_fyers_client():
    """
    Initialize and return Fyers API client and resources path.

    Returns:
        Tuple of (FyersModel instance, resources_path string)
    """
    client_id, access_token = load_tokens()
    resources_path = get_resources_path()

    fyers = fyersModel.FyersModel(
        client_id=client_id,
        token=access_token,
        is_async=False,
        log_path=resources_path,
    )

    return fyers, resources_path

