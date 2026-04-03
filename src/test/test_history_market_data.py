"""
Test cases for history market data collector
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from datetime import datetime, timezone

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'main', 'Python'))

from collector.history_market_data import parse_candles, main


class TestParseCandles(unittest.TestCase):
    """Test cases for parse_candles function"""

    def setUp(self):
        """Set up test fixtures"""
        self.symbol = "NSE:NIFTY50-INDEX"
        self.resolution = "5"

    def test_parse_candles_with_valid_response(self):
        """Test parsing valid API response with candles"""
        response = {
            "s": "ok",
            "message": "success",
            "candles": [
                [1704067500, 22000, 22100, 21900, 22050, 1000],
                [1704067800, 22050, 22200, 21950, 22100, 1100],
            ]
        }

        rows = parse_candles(response, self.symbol, self.resolution)

        self.assertEqual(len(rows), 2)
        # Check first row
        self.assertEqual(rows[0][1], self.symbol)  # symbol
        self.assertEqual(rows[0][2], self.resolution)  # resolution
        self.assertEqual(rows[0][3], 1704067500)  # epoch
        self.assertEqual(rows[0][5], 22000)  # open
        self.assertEqual(rows[0][6], 22100)  # high
        self.assertEqual(rows[0][7], 21900)  # low
        self.assertEqual(rows[0][8], 22050)  # close
        self.assertEqual(rows[0][9], 1000)  # volume

    def test_parse_candles_with_empty_candles(self):
        """Test parsing response with empty candles list"""
        response = {
            "s": "error",
            "message": "No data available",
            "candles": []
        }

        rows = parse_candles(response, self.symbol, self.resolution)

        self.assertEqual(len(rows), 1)
        # Should create one row with empty values for candle data
        self.assertEqual(rows[0][1], self.symbol)
        self.assertEqual(rows[0][3], "")  # empty epoch
        self.assertEqual(rows[0][10], "error")  # status at index 10
        self.assertEqual(rows[0][11], "No data available")  # message at index 11

    def test_parse_candles_with_no_candles_key(self):
        """Test parsing response without candles key"""
        response = {
            "s": "error",
            "message": "Invalid symbol"
        }

        rows = parse_candles(response, self.symbol, self.resolution)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], self.symbol)
        self.assertEqual(rows[0][10], "error")  # status at index 10
        self.assertEqual(rows[0][11], "Invalid symbol")  # message at index 11

    def test_parse_candles_with_invalid_response_type(self):
        """Test parsing non-dict response"""
        response = None

        rows = parse_candles(response, self.symbol, self.resolution)

        self.assertEqual(len(rows), 0)

    def test_parse_candles_with_malformed_candles(self):
        """Test parsing response with malformed candle data"""
        response = {
            "s": "ok",
            "message": "success",
            "candles": [
                [1704067500, 22000, 22100, 21900, 22050, 1000],  # Valid
                [1704067800, 22050],  # Too few fields - should skip
                (1704068100, 22200, 22300, 22000, 22250, 1200),  # Valid tuple
            ]
        }

        rows = parse_candles(response, self.symbol, self.resolution)

        # Should have 2 valid rows (skip the malformed one)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][3], 1704067500)
        self.assertEqual(rows[1][3], 1704068100)

    def test_parse_candles_epoch_to_utc_conversion(self):
        """Test epoch timestamp conversion to UTC ISO format"""
        response = {
            "s": "ok",
            "message": "success",
            "candles": [
                [1704067500, 22000, 22100, 21900, 22050, 1000]
            ]
        }

        rows = parse_candles(response, self.symbol, self.resolution)

        # Check that UTC ISO timestamp is generated
        utc_timestamp = rows[0][4]
        self.assertIsNotNone(utc_timestamp)
        self.assertIn("T", utc_timestamp)  # ISO format has T
        # UTC timezone indicator - can be Z or +00:00
        self.assertTrue("Z" in utc_timestamp or "+00:00" in utc_timestamp)

    def test_parse_candles_multiple_symbols(self):
        """Test parsing for different symbols"""
        response = {
            "s": "ok",
            "message": "success",
            "candles": [
                [1704067500, 22000, 22100, 21900, 22050, 1000]
            ]
        }

        symbols = ["NSE:NIFTY50-INDEX", "BSE:SENSEX-INDEX", "NSE:NIFTYBANK-INDEX"]

        for symbol in symbols:
            rows = parse_candles(response, symbol, self.resolution)
            self.assertEqual(rows[0][1], symbol)


class TestHistoryMarketDataMain(unittest.TestCase):
    """Test cases for main function"""

    @patch('collector.history_market_data.HISTORY_CSV_COLUMNS', new=['col1', 'col2'])
    @patch('collector.history_market_data.HISTORY_MARKET_DATA_FILE', new='test_history.csv')
    @patch('collector.history_market_data.HISTORY_DATA_TEMPLATE', new={'resolution': '5'})
    @patch('collector.history_market_data.MARKET_SYMBOLS_LIST', new=['NSE:NIFTY50-INDEX'])
    @patch('collector.history_market_data.ensure_csv_file')
    @patch('collector.history_market_data.initialize_fyers_client')
    @patch('collector.history_market_data.logger')
    def test_main_success(
        self,
        mock_logger,
        mock_init_client,
        mock_ensure_csv
    ):
        """Test successful main execution"""
        # Mock client
        mock_fyers = MagicMock()
        mock_fyers.history.return_value = {
            "s": "ok",
            "message": "success",
            "candles": [
                [1704067500, 22000, 22100, 21900, 22050, 1000]
            ]
        }
        mock_init_client.return_value = (mock_fyers, '/path/to/resources')

        # Mock csv operations
        with patch('collector.history_market_data.get_history_data') as mock_get_data, \
             patch('collector.history_market_data.parse_candles') as mock_parse, \
             patch('collector.history_market_data.append_csv_rows') as mock_append, \
             patch('os.path.join', side_effect=lambda *args: '/'.join(args)):

            mock_get_data.return_value = {'symbol': 'NSE:NIFTY50-INDEX', 'resolution': '5'}
            mock_parse.return_value = [(datetime.now(timezone.utc).isoformat(), 'NSE:NIFTY50-INDEX', '5', '1704067500', '2024-01-01T00:00:00Z', 22000, 22100, 21900, 22050, 1000, 'ok', 'success')]

            # Run main
            main()

            # Verify client was initialized
            mock_init_client.assert_called_once()

            # Verify CSV file was created
            mock_ensure_csv.assert_called_once()

            # Verify history was fetched for symbol
            mock_fyers.history.assert_called_once()

            # Verify data was parsed and appended
            mock_parse.assert_called_once()
            mock_append.assert_called_once()

            # Verify logging
            self.assertTrue(mock_logger.info.called)

    @patch('collector.history_market_data.logger')
    @patch('collector.history_market_data.initialize_fyers_client')
    def test_main_api_initialization_error(self, mock_init_client, mock_logger):
        """Test main when API client initialization fails"""
        mock_init_client.side_effect = Exception("API initialization failed")

        with self.assertRaises(Exception):
            main()

        # Verify error was logged
        self.assertTrue(mock_logger.critical.called)

    @patch('collector.history_market_data.HISTORY_CSV_COLUMNS', new=['col1'])
    @patch('collector.history_market_data.HISTORY_MARKET_DATA_FILE', new='test_history.csv')
    @patch('collector.history_market_data.HISTORY_DATA_TEMPLATE', new={'resolution': '5'})
    @patch('collector.history_market_data.MARKET_SYMBOLS_LIST', new=['NSE:NIFTY50-INDEX', 'BSE:SENSEX-INDEX'])
    @patch('collector.history_market_data.ensure_csv_file')
    @patch('collector.history_market_data.initialize_fyers_client')
    @patch('collector.history_market_data.logger')
    def test_main_with_multiple_symbols(
        self,
        mock_logger,
        mock_init_client,
        mock_ensure_csv
    ):
        """Test main with multiple enabled symbols"""
        mock_fyers = MagicMock()
        mock_fyers.history.return_value = {
            "s": "ok",
            "message": "success",
            "candles": [[1704067500, 22000, 22100, 21900, 22050, 1000]]
        }
        mock_init_client.return_value = (mock_fyers, '/path/to/resources')

        with patch('collector.history_market_data.get_history_data') as mock_get_data, \
             patch('collector.history_market_data.parse_candles') as mock_parse, \
             patch('collector.history_market_data.append_csv_rows') as mock_append, \
             patch('os.path.join', side_effect=lambda *args: '/'.join(args)):

            mock_get_data.return_value = {'symbol': 'test', 'resolution': '5'}
            mock_parse.return_value = [('2024-01-01T00:00:00Z', 'test', '5', '1704067500', '2024-01-01T00:00:00Z', 22000, 22100, 21900, 22050, 1000, 'ok', 'success')]

            main()

            # Should have called API twice (once per symbol)
            self.assertEqual(mock_fyers.history.call_count, 2)

            # Should have appended data twice
            self.assertEqual(mock_append.call_count, 2)

    @patch('collector.history_market_data.HISTORY_CSV_COLUMNS', new=['col1'])
    @patch('collector.history_market_data.HISTORY_MARKET_DATA_FILE', new='test_history.csv')
    @patch('collector.history_market_data.HISTORY_DATA_TEMPLATE', new={'resolution': '5'})
    @patch('collector.history_market_data.MARKET_SYMBOLS_LIST', new=['NSE:NIFTY50-INDEX'])
    @patch('collector.history_market_data.ensure_csv_file')
    @patch('collector.history_market_data.initialize_fyers_client')
    @patch('collector.history_market_data.logger')
    def test_main_with_symbol_fetch_error(
        self,
        mock_logger,
        mock_init_client,
        mock_ensure_csv
    ):
        """Test main when fetching data for a symbol fails"""
        mock_fyers = MagicMock()
        mock_fyers.history.side_effect = Exception("API error")
        mock_init_client.return_value = (mock_fyers, '/path/to/resources')

        with patch('collector.history_market_data.get_history_data') as mock_get_data, \
             patch('os.path.join', side_effect=lambda *args: '/'.join(args)):

            mock_get_data.return_value = {'symbol': 'NSE:NIFTY50-INDEX', 'resolution': '5'}

            # Should not raise exception, should handle and log error
            main()

            # Verify error was logged
            self.assertTrue(mock_logger.error.called)

            # Verify info messages for start and completion
            self.assertTrue(mock_logger.info.called)

    @patch('collector.history_market_data.HISTORY_CSV_COLUMNS', new=['col1'])
    @patch('collector.history_market_data.HISTORY_MARKET_DATA_FILE', new='test_history.csv')
    @patch('collector.history_market_data.HISTORY_DATA_TEMPLATE', new={'resolution': '5'})
    @patch('collector.history_market_data.MARKET_SYMBOLS_LIST', new=[])
    @patch('collector.history_market_data.ensure_csv_file')
    @patch('collector.history_market_data.initialize_fyers_client')
    @patch('collector.history_market_data.logger')
    def test_main_with_empty_symbols_list(
        self,
        mock_logger,
        mock_init_client,
        mock_ensure_csv
    ):
        """Test main when no symbols are enabled"""
        mock_fyers = MagicMock()
        mock_init_client.return_value = (mock_fyers, '/path/to/resources')

        with patch('os.path.join', side_effect=lambda *args: '/'.join(args)):
            main()

            # Should not call API when no symbols
            mock_fyers.history.assert_not_called()

            # Should log info about 0 symbols
            self.assertTrue(mock_logger.info.called)


class TestHistoryDataIntegration(unittest.TestCase):
    """Integration tests for history data collector"""

    @patch('collector.history_market_data.HISTORY_CSV_COLUMNS', new=['col1'])
    @patch('collector.history_market_data.HISTORY_MARKET_DATA_FILE', new='history.csv')
    @patch('collector.history_market_data.HISTORY_DATA_TEMPLATE', new={'resolution': '5'})
    @patch('collector.history_market_data.MARKET_SYMBOLS_LIST', new=['NSE:NIFTY50-INDEX'])
    @patch('collector.history_market_data.append_csv_rows')
    @patch('collector.history_market_data.ensure_csv_file')
    @patch('collector.history_market_data.initialize_fyers_client')
    @patch('collector.history_market_data.logger')
    def test_full_flow_with_real_like_data(
        self,
        mock_logger,
        mock_init_client,
        mock_ensure_csv,
        mock_append
    ):
        """Test full flow with realistic API response"""
        mock_fyers = MagicMock()
        mock_fyers.history.return_value = {
            "s": "ok",
            "message": "success",
            "candles": [
                [1704067500, 22000, 22150, 21950, 22100, 5000],
                [1704067800, 22100, 22200, 22050, 22150, 4500],
                [1704068100, 22150, 22300, 22100, 22250, 6000],
            ]
        }
        mock_init_client.return_value = (mock_fyers, '/resources')

        with patch('collector.history_market_data.get_history_data') as mock_get_data, \
             patch('os.path.join', side_effect=lambda *args: '/'.join(args)):

            mock_get_data.return_value = {'symbol': 'NSE:NIFTY50-INDEX', 'resolution': '5'}

            main()

            # Verify append was called with 3 rows
            self.assertTrue(mock_append.called)
            call_args = mock_append.call_args
            rows = call_args[0][1]  # Get rows argument
            self.assertEqual(len(rows), 3)


if __name__ == '__main__':
    unittest.main()

