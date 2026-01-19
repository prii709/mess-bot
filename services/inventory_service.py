"""
Inventory Service Module

This module provides functionality for managing and querying mess inventory data.
"""

import pandas as pd
from typing import List, Dict, Optional
from services.sheets_client import SheetsClient


class InventoryService:
    """Service for managing mess inventory data."""
    
    def __init__(self, spreadsheet_id: str, worksheet_name: str = 'inventory_sheet'):
        """
        Initialize the Inventory Service.
        
        Args:
            spreadsheet_id (str): The ID of the Google Spreadsheet containing inventory data.
            worksheet_name (str): The name of the worksheet (default: 'inventory_sheet').
        """
        self.spreadsheet_id = spreadsheet_id
        self.worksheet_name = worksheet_name
        self.sheets_client = SheetsClient()
        self.inventory_df = None
        self._load_inventory()
    
    def _load_inventory(self):
        """
        Load inventory data from Google Sheets into a pandas DataFrame.
        
        Raises:
            ValueError: If the required columns are not present in the sheet.
        """
        records = self.sheets_client.get_all_records(
            self.spreadsheet_id, 
            self.worksheet_name
        )
        
        self.inventory_df = pd.DataFrame(records)
        
        # Validate required columns
        required_columns = ['item_name', 'quantity']
        if not all(col in self.inventory_df.columns for col in required_columns):
            raise ValueError(
                f"Inventory sheet must contain columns: {required_columns}. "
                f"Found columns: {list(self.inventory_df.columns)}"
            )
        
        # Ensure quantity is numeric
        self.inventory_df['quantity'] = pd.to_numeric(
            self.inventory_df['quantity'], 
            errors='coerce'
        ).fillna(0)
    
    def reload_inventory(self):
        """Reload inventory data from Google Sheets."""
        self._load_inventory()
    
    def get_item_stock(self, item_name: str) -> Optional[float]:
        """
        Get the current stock quantity for a specific item.
        
        Args:
            item_name (str): The name of the item to look up.
        
        Returns:
            Optional[float]: The current quantity of the item, or None if item not found.
        """
        if self.inventory_df is None or self.inventory_df.empty:
            return None
        
        # Case-insensitive search
        item_row = self.inventory_df[
            self.inventory_df['item_name'].str.lower() == item_name.lower()
        ]
        
        if item_row.empty:
            return None
        
        return float(item_row.iloc[0]['quantity'])
    
    def get_low_stock_items(self, threshold: float) -> List[Dict[str, float]]:
        """
        Get all items with stock below the specified threshold.
        
        Args:
            threshold (float): The stock threshold to check against.
        
        Returns:
            List[Dict[str, float]]: List of dictionaries containing item_name and quantity
                                   for items below the threshold.
        """
        if self.inventory_df is None or self.inventory_df.empty:
            return []
        
        low_stock_df = self.inventory_df[
            self.inventory_df['quantity'] < threshold
        ][['item_name', 'quantity']].copy()
        
        # Convert quantity to float for JSON serialization
        low_stock_df['quantity'] = low_stock_df['quantity'].astype(float)
        
        return low_stock_df.to_dict('records')
    
    def get_all_items(self) -> List[Dict[str, float]]:
        """
        Get all items in the inventory.
        
        Returns:
            List[Dict[str, float]]: List of dictionaries containing all inventory items.
        """
        if self.inventory_df is None or self.inventory_df.empty:
            return []
        
        result_df = self.inventory_df[['item_name', 'quantity']].copy()
        
        # Convert quantity to float for JSON serialization
        result_df['quantity'] = result_df['quantity'].astype(float)
        
        return result_df.to_dict('records')
