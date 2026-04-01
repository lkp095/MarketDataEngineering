import csv
import os

# Get the directory of this file
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(current_dir, "market_symbols.csv")

def load_market_symbols():
    """Load market symbols from CSV file"""
    symbols_list = []
    
    try:
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Only include symbols that are enabled
                if row['enabled'].lower() == 'true':
                    symbols_list.append(row['symbol'])
    except FileNotFoundError:
        raise FileNotFoundError(f"Market symbols CSV file not found at: {csv_file_path}")
    
    return symbols_list

# Load symbols from CSV
MARKET_SYMBOLS_LIST = load_market_symbols()

# Comma-separated string format for API requests
MARKET_SYMBOLS_STRING = ", ".join(MARKET_SYMBOLS_LIST)

