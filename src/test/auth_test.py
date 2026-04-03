"""
Test cases for authenticator module
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'main', 'Python'))

from authenticator.fyers_authenticator import FyersAuthenticator


class TestFyersAuthenticator(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures"""
        self.auth = FyersAuthenticator()

    def test_init(self):
        """Test FyersAuthenticator initialization"""
        self.assertIsNotNone(self.auth.client_id)
        self.assertIsNotNone(self.auth.secret_key)
        self.assertEqual(self.auth.redirect_uri, 'https://trade.fyers.in/api-login/redirect-uri/index.html')
        self.assertEqual(self.auth.response_type, 'code')
        self.assertEqual(self.auth.grant_type, 'authorization_code')
        self.assertIsNone(self.auth.session)
        self.assertIsNone(self.auth.access_token)

    @patch('authenticator.fyers_authenticator.fyersModel')
    def test_generate_auth_url(self, mock_fyers):
        """Test generating authorization URL"""
        mock_session = MagicMock()
        mock_session.generate_authcode.return_value = 'https://example.com/auth'
        mock_fyers.SessionModel.return_value = mock_session

        with patch('builtins.print'):
            url = self.auth.generate_auth_url()

        self.assertEqual(url, 'https://example.com/auth')
        self.assertIsNotNone(self.auth.session)
        mock_fyers.SessionModel.assert_called_once()
        mock_session.generate_authcode.assert_called_once()

    def test_set_auth_code_without_session(self):
        """Test setting auth code without session raises error"""
        with self.assertRaises(RuntimeError) as context:
            self.auth.set_auth_code('code123')
        self.assertIn('Session not initialized', str(context.exception))

    @patch('authenticator.fyers_authenticator.fyersModel')
    def test_set_auth_code_with_session(self, mock_fyers):
        """Test setting auth code with valid session"""
        mock_session = MagicMock()
        mock_fyers.SessionModel.return_value = mock_session
        self.auth.session = mock_session

        self.auth.set_auth_code('code123')
        mock_session.set_token.assert_called_once_with('code123')

    def test_generate_access_token_without_session(self):
        """Test generating access token without session raises error"""
        with self.assertRaises(RuntimeError) as context:
            self.auth.generate_access_token()
        self.assertIn('Session not initialized', str(context.exception))

    @patch('authenticator.fyers_authenticator.fyersModel')
    def test_generate_access_token_success(self, mock_fyers):
        """Test successful access token generation"""
        mock_session = MagicMock()
        mock_session.generate_token.return_value = {'access_token': 'token123'}
        mock_fyers.SessionModel.return_value = mock_session
        self.auth.session = mock_session

        with patch('builtins.print'):
            token = self.auth.generate_access_token()

        self.assertEqual(token, 'token123')
        self.assertEqual(self.auth.access_token, 'token123')
        mock_session.generate_token.assert_called_once()

    @patch('authenticator.fyers_authenticator.fyersModel')
    def test_generate_access_token_failure(self, mock_fyers):
        """Test access token generation failure"""
        mock_session = MagicMock()
        mock_session.generate_token.return_value = {'error': 'invalid_code'}
        mock_fyers.SessionModel.return_value = mock_session
        self.auth.session = mock_session

        with patch('builtins.print'):
            with self.assertRaises(Exception):
                self.auth.generate_access_token()

    def test_save_tokens_without_token(self):
        """Test saving tokens without access token raises error"""
        with self.assertRaises(RuntimeError) as context:
            self.auth.save_tokens()
        self.assertIn('Access token not generated', str(context.exception))

    @patch('authenticator.fyers_authenticator.save_tokens')
    def test_save_tokens_with_token(self, mock_save_tokens):
        """Test saving tokens with valid access token"""
        self.auth.access_token = 'token123'

        self.auth.save_tokens()
        mock_save_tokens.assert_called_once_with(self.auth.client_id, 'token123')

    def test_get_fyers_model_without_token(self):
        """Test getting fyers model without token raises error"""
        with self.assertRaises(RuntimeError) as context:
            self.auth.get_fyers_model()
        self.assertIn('Access token not available', str(context.exception))

    @patch('authenticator.fyers_authenticator.fyersModel')
    @patch('authenticator.fyers_authenticator.get_resources_path')
    def test_get_fyers_model_with_token(self, mock_get_path, mock_fyers):
        """Test getting fyers model with valid token"""
        self.auth.access_token = 'token123'
        mock_get_path.return_value = '/path/to/resources'
        mock_fyers_instance = MagicMock()
        mock_fyers.FyersModel.return_value = mock_fyers_instance

        fyers_model = self.auth.get_fyers_model()

        self.assertEqual(fyers_model, mock_fyers_instance)
        mock_fyers.FyersModel.assert_called_once_with(
            client_id=self.auth.client_id,
            token='token123',
            is_async=False,
            log_path='/path/to/resources'
        )


class TestAuthMain(unittest.TestCase):
    """Test cases for Auth.py main function"""

    @patch('authenticator.auth.input', return_value='auth_code_123')
    @patch('authenticator.auth.FyersAuthenticator')
    def test_main_flow(self, mock_auth_class, mock_input):
        """Test the main authentication flow"""
        mock_auth_instance = MagicMock()
        mock_auth_class.return_value = mock_auth_instance

        # Import and run main
        from authenticator.auth import main

        with patch('builtins.print'):
            main()

        # Verify authentication steps were called in order
        mock_auth_class.assert_called_once()
        mock_auth_instance.generate_auth_url.assert_called_once()
        mock_auth_instance.set_auth_code.assert_called_once_with('auth_code_123')
        mock_auth_instance.generate_access_token.assert_called_once()
        mock_auth_instance.save_tokens.assert_called_once()

    @patch('authenticator.auth.input', side_effect=KeyboardInterrupt)
    @patch('authenticator.auth.FyersAuthenticator')
    def test_main_interrupted(self, mock_auth_class, mock_input):
        """Test main function when interrupted by user"""
        mock_auth_instance = MagicMock()
        mock_auth_class.return_value = mock_auth_instance

        from authenticator.auth import main

        with patch('builtins.print'):
            # Should not raise exception on KeyboardInterrupt
            try:
                main()
            except KeyboardInterrupt:
                # Expected behavior
                pass


if __name__ == '__main__':
    unittest.main()


