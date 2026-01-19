"""
Unit tests for SheetsClient module.
"""

import os
import json
import pytest
from unittest.mock import Mock, patch
from services.sheets_client import SheetsClient


class TestSheetsClient:
    """Test cases for SheetsClient class."""
    
    @pytest.fixture
    def mock_credentials(self):
        """Fixture providing mock service account credentials."""
        return {
            "type": "service_account",
            "project_id": "test-project",
            "private_key_id": "test-key-id",
            "private_key": "-----BEGIN PRIVATE KEY-----\ntest-key\n-----END PRIVATE KEY-----\n",
            "client_email": "test@test-project.iam.gserviceaccount.com",
            "client_id": "123456789",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    
    def test_init_without_credentials_raises_error(self):
        """Test that initialization without credentials raises ValueError."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError) as exc_info:
                SheetsClient()
            assert "GOOGLE_SHEETS_CREDENTIALS" in str(exc_info.value)
    
    def test_init_with_invalid_json_raises_error(self, mock_credentials):
        """Test that initialization with invalid JSON raises ValueError."""
        with patch.dict(os.environ, {'GOOGLE_SHEETS_CREDENTIALS': 'invalid-json'}):
            with pytest.raises(ValueError) as exc_info:
                SheetsClient()
            assert "Invalid JSON" in str(exc_info.value)
    
    @patch('services.sheets_client.gspread.authorize')
    @patch('services.sheets_client.Credentials.from_service_account_info')
    def test_init_with_valid_credentials(self, mock_creds, mock_authorize, mock_credentials):
        """Test successful initialization with valid credentials."""
        creds_json = json.dumps(mock_credentials)
        
        with patch.dict(os.environ, {'GOOGLE_SHEETS_CREDENTIALS': creds_json}):
            client = SheetsClient()
            
            assert client is not None
            mock_creds.assert_called_once()
            mock_authorize.assert_called_once()
    
    @patch('services.sheets_client.gspread.authorize')
    @patch('services.sheets_client.Credentials.from_service_account_info')
    def test_get_worksheet(self, mock_creds, mock_authorize, mock_credentials):
        """Test get_worksheet method."""
        creds_json = json.dumps(mock_credentials)
        
        mock_worksheet = Mock()
        mock_spreadsheet = Mock()
        mock_spreadsheet.worksheet.return_value = mock_worksheet
        mock_client = Mock()
        mock_client.open_by_key.return_value = mock_spreadsheet
        mock_authorize.return_value = mock_client
        
        with patch.dict(os.environ, {'GOOGLE_SHEETS_CREDENTIALS': creds_json}):
            client = SheetsClient()
            result = client.get_worksheet('test-spreadsheet-id', 'test-sheet')
            
            assert result == mock_worksheet
            mock_client.open_by_key.assert_called_once_with('test-spreadsheet-id')
            mock_spreadsheet.worksheet.assert_called_once_with('test-sheet')
    
    @patch('services.sheets_client.gspread.authorize')
    @patch('services.sheets_client.Credentials.from_service_account_info')
    def test_get_all_records(self, mock_creds, mock_authorize, mock_credentials):
        """Test get_all_records method."""
        creds_json = json.dumps(mock_credentials)
        
        mock_records = [
            {'item_name': 'Rice', 'quantity': 100},
            {'item_name': 'Wheat', 'quantity': 50}
        ]
        mock_worksheet = Mock()
        mock_worksheet.get_all_records.return_value = mock_records
        mock_spreadsheet = Mock()
        mock_spreadsheet.worksheet.return_value = mock_worksheet
        mock_client = Mock()
        mock_client.open_by_key.return_value = mock_spreadsheet
        mock_authorize.return_value = mock_client
        
        with patch.dict(os.environ, {'GOOGLE_SHEETS_CREDENTIALS': creds_json}):
            client = SheetsClient()
            result = client.get_all_records('test-spreadsheet-id', 'test-sheet')
            
            assert result == mock_records
            mock_worksheet.get_all_records.assert_called_once()
    
    @patch('services.sheets_client.gspread.authorize')
    @patch('services.sheets_client.Credentials.from_service_account_info')
    def test_custom_env_var(self, mock_creds, mock_authorize, mock_credentials):
        """Test initialization with custom environment variable name."""
        creds_json = json.dumps(mock_credentials)
        custom_var = 'CUSTOM_CREDS_VAR'
        
        with patch.dict(os.environ, {custom_var: creds_json}):
            client = SheetsClient(credentials_env_var=custom_var)
            
            assert client.credentials_env_var == custom_var
            mock_authorize.assert_called_once()
