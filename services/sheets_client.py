"""
Google Sheets Client Module

This module provides a client for interacting with Google Sheets using service account authentication.
"""

import os
import json
import gspread
from google.oauth2.service_account import Credentials


class SheetsClient:
    """Client for accessing Google Sheets with service account authentication."""
    
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets.readonly',
        'https://www.googleapis.com/auth/drive.readonly'
    ]
    
    def __init__(self, credentials_env_var='GOOGLE_SHEETS_CREDENTIALS'):
        """
        Initialize the Google Sheets client.
        
        Args:
            credentials_env_var (str): Name of the environment variable containing
                                      the service account credentials JSON.
        
        Raises:
            ValueError: If the credentials environment variable is not set.
            json.JSONDecodeError: If the credentials JSON is invalid.
        """
        self.credentials_env_var = credentials_env_var
        self._client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """
        Initialize the gspread client with service account credentials.
        
        Raises:
            ValueError: If credentials are not found or invalid.
        """
        credentials_json = os.environ.get(self.credentials_env_var)
        
        if not credentials_json:
            raise ValueError(
                f"Environment variable '{self.credentials_env_var}' not set. "
                "Please provide Google Sheets service account credentials."
            )
        
        try:
            credentials_dict = json.loads(credentials_json)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in credentials: {e}")
        
        credentials = Credentials.from_service_account_info(
            credentials_dict,
            scopes=self.SCOPES
        )
        
        self._client = gspread.authorize(credentials)
    
    def get_worksheet(self, spreadsheet_id, worksheet_name):
        """
        Get a specific worksheet from a spreadsheet.
        
        Args:
            spreadsheet_id (str): The ID of the Google Spreadsheet.
            worksheet_name (str): The name of the worksheet to retrieve.
        
        Returns:
            gspread.Worksheet: The requested worksheet.
        
        Raises:
            gspread.exceptions.SpreadsheetNotFound: If spreadsheet is not found.
            gspread.exceptions.WorksheetNotFound: If worksheet is not found.
        """
        spreadsheet = self._client.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.worksheet(worksheet_name)
        return worksheet
    
    def get_all_records(self, spreadsheet_id, worksheet_name):
        """
        Get all records from a worksheet as a list of dictionaries.
        
        Args:
            spreadsheet_id (str): The ID of the Google Spreadsheet.
            worksheet_name (str): The name of the worksheet to retrieve.
        
        Returns:
            list: List of dictionaries where keys are column headers.
        """
        worksheet = self.get_worksheet(spreadsheet_id, worksheet_name)
        return worksheet.get_all_records()
