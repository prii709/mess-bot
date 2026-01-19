import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from typing import List, Dict, Any
from app.config import settings
import os


class GoogleSheetsService:
    """Service for interacting with Google Sheets API"""
    
    def __init__(self):
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Google Sheets client with service account credentials"""
        try:
            if os.path.exists(settings.google_sheets_credentials_path):
                scopes = [
                    'https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive'
                ]
                creds = Credentials.from_service_account_file(
                    settings.google_sheets_credentials_path,
                    scopes=scopes
                )
                self.client = gspread.authorize(creds)
            else:
                print(f"Warning: Credentials file not found at {settings.google_sheets_credentials_path}")
        except Exception as e:
            print(f"Error initializing Google Sheets client: {e}")
    
    def get_sheet_data(self, sheet_id: str, worksheet_name: str = None) -> pd.DataFrame:
        """
        Get data from a Google Sheet as a pandas DataFrame
        
        Args:
            sheet_id: ID of the Google Sheet
            worksheet_name: Name of the worksheet (default: first worksheet)
        
        Returns:
            pandas DataFrame with the sheet data
        """
        if not self.client:
            return pd.DataFrame()
        
        try:
            spreadsheet = self.client.open_by_key(sheet_id)
            worksheet = spreadsheet.get_worksheet(0) if not worksheet_name else spreadsheet.worksheet(worksheet_name)
            data = worksheet.get_all_records()
            return pd.DataFrame(data)
        except Exception as e:
            print(f"Error fetching sheet data: {e}")
            return pd.DataFrame()
    
    def update_sheet_data(self, sheet_id: str, data: List[List[Any]], worksheet_name: str = None):
        """
        Update data in a Google Sheet
        
        Args:
            sheet_id: ID of the Google Sheet
            data: List of lists containing data to update
            worksheet_name: Name of the worksheet (default: first worksheet)
        """
        if not self.client:
            return
        
        try:
            spreadsheet = self.client.open_by_key(sheet_id)
            worksheet = spreadsheet.get_worksheet(0) if not worksheet_name else spreadsheet.worksheet(worksheet_name)
            worksheet.clear()
            worksheet.update('A1', data)
        except Exception as e:
            print(f"Error updating sheet data: {e}")
    
    def append_sheet_row(self, sheet_id: str, row: List[Any], worksheet_name: str = None):
        """
        Append a row to a Google Sheet
        
        Args:
            sheet_id: ID of the Google Sheet
            row: List containing row data
            worksheet_name: Name of the worksheet (default: first worksheet)
        """
        if not self.client:
            return
        
        try:
            spreadsheet = self.client.open_by_key(sheet_id)
            worksheet = spreadsheet.get_worksheet(0) if not worksheet_name else spreadsheet.worksheet(worksheet_name)
            worksheet.append_row(row)
        except Exception as e:
            print(f"Error appending row: {e}")


# Singleton instance
sheets_service = GoogleSheetsService()
