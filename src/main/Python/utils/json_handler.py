"""
JSON handler utility for reading and writing JSON files
"""

import json
import os
from datetime import datetime


def ensure_json_file(path):
    """Create JSON file with empty list if it does not exist."""
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, "w") as file:
            json.dump([], file)


def load_json_data(path):
    """Load data from JSON file."""
    try:
        with open(path, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        return []


def append_json_row(path, timestamp, data):
    """Append a timestamped data row to JSON file."""
    existing_data = load_json_data(path)
    existing_data.append({
        "timestamp": timestamp,
        "data": data
    })
    with open(path, "w") as file:
        json.dump(existing_data, file, indent=2)

