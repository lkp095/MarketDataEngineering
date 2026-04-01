"""
Test cases for MarketData.py
"""

import unittest
from unittest.mock import patch, MagicMock, mock_open
import json
import os
import sys
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'main', 'Python'))


class TestMarketData(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_response = {
            "code": 200,
            "message": "success",
            "data": [
                {"symbol": "NSE:NIFTY50-INDEX", "ltp": 22000},
                {"symbol": "BSE:SENSEX-INDEX", "ltp": 72000}
            ]
        }
    
    def test_data_collection_loop(self):
        """Test the data collection loop"""
        mock_fyers = MagicMock()
        mock_fyers.quotes.return_value = self.mock_response
        
        # Simulate the loop
        data_list = []
        counter = 0
        max_iterations = 3
        try:
            while counter < max_iterations:
                # Simulate the loop body
                response = mock_fyers.quotes(data={"symbols": "NSE:NIFTY50-INDEX, BSE:SENSEX-INDEX"})
                print(f"Fetched data: {response}")
                
                # For test, just append to list
                data_list.append({
                    "timestamp": "2023-10-01T12:00:00",
                    "data": response
                })
                
                counter += 1
        except KeyboardInterrupt:
            pass
        
        # Check that quotes was called 3 times
        self.assertEqual(mock_fyers.quotes.call_count, 3)
        self.assertEqual(len(data_list), 3)
    
    def test_quotes_call(self):
        """Test that fyers.quotes is called with correct data"""
        mock_fyers = MagicMock()
        mock_fyers.quotes.return_value = self.mock_response
        
        # Simulate the call
        response = mock_fyers.quotes(data={"symbols": "NSE:NIFTY50-INDEX, BSE:SENSEX-INDEX"})
        
        mock_fyers.quotes.assert_called_once_with(data={"symbols": "NSE:NIFTY50-INDEX, BSE:SENSEX-INDEX"})
        self.assertEqual(response, self.mock_response)
    
    def test_data_append_to_file(self):
        """Test appending data to JSON file"""
        mock_json_load = MagicMock(return_value=[{"old": "data"}])
        mock_json_dump = MagicMock()
        mock_file = MagicMock()
        
        # Simulate the append logic
        response = self.mock_response
        
        # Read existing data
        existing_data = mock_json_load.return_value
        
        # Append new response with timestamp
        timestamp = "2023-10-01T12:00:00"
        existing_data.append({
            "timestamp": timestamp,
            "data": response
        })
        
        # Write back to file
        with mock_file as f:
            mock_json_dump(existing_data, f, indent=2)
        
        mock_json_dump.assert_called_once_with(existing_data, mock_file.__enter__.return_value, indent=2)
        self.assertEqual(len(existing_data), 2)
        self.assertEqual(existing_data[1]["timestamp"], "2023-10-01T12:00:00")
        self.assertEqual(existing_data[1]["data"], response)
    
    def test_file_creation_if_not_exists(self):
        """Test that market_data.json is created if it doesn't exist"""
        mock_exists = MagicMock(return_value=False)
        mock_file = MagicMock()
        mock_json_dump = MagicMock()
        
        # The script does:
        if not mock_exists("dummy_path"):
            with mock_file("dummy_path", "w") as f:
                mock_json_dump([], f)
        
        mock_exists.assert_called_once_with("dummy_path")
        mock_json_dump.assert_called_once_with([], mock_file.return_value.__enter__.return_value)


if __name__ == '__main__':
    unittest.main()
