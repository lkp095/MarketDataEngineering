"""
CSV handler utility for reading and writing CSV files
"""

import csv
import os
from datetime import datetime, timezone


def ensure_csv_file(path, headers):
    """Create CSV file with headers if it does not exist or is empty."""
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)


def epoch_to_utc_iso(epoch_value):
    """Convert epoch value to UTC ISO timestamp string."""
    try:
        return datetime.fromtimestamp(
            float(epoch_value), tz=timezone.utc
        ).isoformat()
    except (TypeError, ValueError, OSError):
        return ""


def append_csv_row(path, row):
    """Append a single row to CSV file."""
    with open(path, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(row)


def append_csv_rows(path, rows):
    """Append multiple rows to CSV file."""
    with open(path, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

