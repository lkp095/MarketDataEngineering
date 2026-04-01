"""
Test cases for Auth.py and FyersAuthenticator
"""

import unittest
from unittest.mock import patch, MagicMock, mock_open
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
        """Test initialization"""
        self.assertEqual(self.auth.client_id, 'RX6ZEHRV6X-100')
        self.assertEqual(self.auth.secret_key, '5491XH3V0G')
        self.assertEqual(self.auth.redirect_uri, 'https://trade.fyers.in/api-login/redirect-uri/index.html')
        self.assertEqual(self.auth.response_type, 'code')
        self.assertEqual(self.auth.grant_type, 'authorization_code')
        self.assertIsNone(self.auth.session)
        self.assertIsNone(self.auth.access_token)
    
    @patch('authenticator.fyers_authenticator.fyersModel')
    def test_generate_auth_url(self, mock_fyers):
        """Test generating auth URL"""
        mock_session = MagicMock()
        mock_session.generate_authcode.return_value = 'https://example.com/auth'
        mock_fyers.SessionModel.return_value = mock_session
        
        with patch('builtins.print') as mock_print:
            url = self.auth.generate_auth_url()
        
        self.assertEqual(url, 'https://example.com/auth')
        mock_fyers.SessionModel.assert_called_once_with(
            client_id=self.auth.client_id,
            secret_key=self.auth.secret_key,
            redirect_uri=self.auth.redirect_uri,
            response_type=self.auth.response_type,
            grant_type=self.auth.grant_type
        )
        mock_session.generate_authcode.assert_called_once()
        # Check print calls
        self.assertIn('Authorization URL:', str(mock_print.call_args_list))
    
    def test_set_auth_code_without_session(self):
        """Test setting auth code without session"""
        with self.assertRaises(RuntimeError) as cm:
            self.auth.set_auth_code('code123')
        self.assertIn('Session not initialized', str(cm.exception))
    
    @patch('authenticator.fyers_authenticator.fyersModel')
    def test_set_auth_code(self, mock_fyers):
        """Test setting auth code"""
        mock_session = MagicMock()
        mock_fyers.SessionModel.return_value = mock_session
        self.auth.session = mock_session
        
        self.auth.set_auth_code('code123')
        mock_session.set_token.assert_called_once_with('code123')
    
    def test_generate_access_token_without_session(self):
        """Test generating access token without session"""
        with self.assertRaises(RuntimeError) as cm:
            self.auth.generate_access_token()
        self.assertIn('Session not initialized', str(cm.exception))
    
    @patch('authenticator.fyers_authenticator.fyersModel')
    def test_generate_access_token_success(self, mock_fyers):
        """Test generating access token successfully"""
        mock_session = MagicMock()
        mock_session.generate_token.return_value = {'access_token': 'token123'}
        mock_fyers.SessionModel.return_value = mock_session
        self.auth.session = mock_session
        
        with patch('builtins.print') as mock_print:
            token = self.auth.generate_access_token()
        
        self.assertEqual(token, 'token123')
        self.assertEqual(self.auth.access_token, 'token123')
        mock_session.generate_token.assert_called_once()
        self.assertIn('Access Token generated successfully!', str(mock_print.call_args_list))
    
    @patch('authenticator.fyers_authenticator.fyersModel')
    def test_generate_access_token_failure(self, mock_fyers):
        """Test generating access token failure"""
        mock_session = MagicMock()
        mock_session.generate_token.return_value = {'error': 'invalid_code'}
        mock_fyers.SessionModel.return_value = mock_session
        self.auth.session = mock_session
        
        with patch('builtins.print') as mock_print:
            with self.assertRaises(Exception):
                self.auth.generate_access_token()
        
        self.assertIn('Error generating access token', str(mock_print.call_args_list))
    
    def test_save_tokens_without_token(self):
        """Test saving tokens without access token"""
        with self.assertRaises(RuntimeError) as cm:
            self.auth.save_tokens()
        self.assertIn('Access token not generated', str(cm.exception))
    
    @patch('authenticator.fyers_authenticator.save_tokens')
    def test_save_tokens(self, mock_save):
        """Test saving tokens"""
        self.auth.access_token = 'token123'
        
        self.auth.save_tokens()
        mock_save.assert_called_once_with(self.auth.client_id, self.auth.access_token)
    
    def test_get_fyers_model_without_token(self):
        """Test getting fyers model without token"""
        with self.assertRaises(RuntimeError) as cm:
            self.auth.get_fyers_model()
        self.assertIn('Access token not available', str(cm.exception))
    
    @patch('authenticator.fyers_authenticator.fyersModel')
    @patch('authenticator.fyers_authenticator.get_resources_path')
    def test_get_fyers_model(self, mock_get_path, mock_fyers):
        """Test getting fyers model"""
        self.auth.access_token = 'token123'
        mock_get_path.return_value = '/path/to/resources'
        mock_fyers_model = MagicMock()
        mock_fyers.FyersModel.return_value = mock_fyers_model
        
        fyers = self.auth.get_fyers_model()
        
        self.assertEqual(fyers, mock_fyers_model)
        mock_fyers.FyersModel.assert_called_once_with(
            client_id=self.auth.client_id,
            token=self.auth.access_token,
            is_async=False,
            log_path='/path/to/resources'
        )


class TestAuthMain(unittest.TestCase):
    
    @patch('authenticator.Auth.input', return_value='auth_code_123')
    @patch('authenticator.Auth.FyersAuthenticator')
    @patch('builtins.print')
    def test_main_flow(self, mock_print, mock_auth_class, mock_input):
        """Test the main authentication flow"""
        mock_auth_instance = MagicMock()
        mock_auth_class.return_value = mock_auth_instance
        
        # Import and run main
        from authenticator.Auth import main
        main()
        
        # Check calls
        mock_auth_class.assert_called_once()
        mock_auth_instance.generate_auth_url.assert_called_once()
        mock_auth_instance.set_auth_code.assert_called_once_with('auth_code_123')
        mock_auth_instance.generate_access_token.assert_called_once()
        mock_auth_instance.save_tokens.assert_called_once()
        # Check prints
        self.assertGreater(len(mock_print.call_args_list), 5)  # Multiple prints


if __name__ == '__main__':
    unittest.main()
