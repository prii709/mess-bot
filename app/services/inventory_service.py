import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.services.sheets_service import sheets_service
from app.config import settings
from app.models.schemas import InventoryItem, Alert


class InventoryService:
    """Service for managing inventory data and operations"""
    
    def __init__(self):
        self.sheet_id = settings.inventory_sheet_id
        self.low_stock_threshold = settings.low_stock_threshold
    
    def get_all_items(self) -> List[Dict[str, Any]]:
        """
        Get all inventory items
        
        Returns:
            List of inventory items as dictionaries
        """
        df = sheets_service.get_sheet_data(self.sheet_id)
        if df.empty:
            return []
        
        # Convert to list of dictionaries
        return df.to_dict('records')
    
    def get_item_by_name(self, item_name: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific inventory item by name
        
        Args:
            item_name: Name of the item to find
        
        Returns:
            Dictionary with item details or None if not found
        """
        df = sheets_service.get_sheet_data(self.sheet_id)
        if df.empty:
            return None
        
        # Case-insensitive search
        df['item_name_lower'] = df.get('item_name', df.get('Item Name', df.get('name', ''))).astype(str).str.lower()
        item_name_lower = item_name.lower()
        
        matching_items = df[df['item_name_lower'].str.contains(item_name_lower, na=False)]
        
        if not matching_items.empty:
            item = matching_items.iloc[0].to_dict()
            item.pop('item_name_lower', None)
            return item
        
        return None
    
    def check_low_stock(self) -> List[Alert]:
        """
        Check for items with low stock
        
        Returns:
            List of low stock alerts
        """
        df = sheets_service.get_sheet_data(self.sheet_id)
        if df.empty:
            return []
        
        alerts = []
        
        # Try different possible column names
        quantity_col = None
        name_col = None
        
        for col in ['quantity', 'Quantity', 'qty', 'Qty', 'stock', 'Stock']:
            if col in df.columns:
                quantity_col = col
                break
        
        for col in ['item_name', 'Item Name', 'name', 'Name', 'item', 'Item']:
            if col in df.columns:
                name_col = col
                break
        
        if quantity_col and name_col:
            # Convert quantity to numeric, handling any non-numeric values
            df[quantity_col] = pd.to_numeric(df[quantity_col], errors='coerce')
            
            low_stock_items = df[df[quantity_col] < self.low_stock_threshold]
            
            for _, item in low_stock_items.iterrows():
                alerts.append(Alert(
                    type="low_stock",
                    message=f"Low stock alert: {item[name_col]} has only {item[quantity_col]} units remaining",
                    severity="warning",
                    timestamp=datetime.now().isoformat()
                ))
        
        return alerts
    
    def get_inventory_summary(self) -> Dict[str, Any]:
        """
        Get a summary of inventory statistics
        
        Returns:
            Dictionary with inventory summary
        """
        df = sheets_service.get_sheet_data(self.sheet_id)
        if df.empty:
            return {
                "total_items": 0,
                "low_stock_items": 0,
                "message": "No inventory data available"
            }
        
        # Try to find quantity column
        quantity_col = None
        for col in ['quantity', 'Quantity', 'qty', 'Qty', 'stock', 'Stock']:
            if col in df.columns:
                quantity_col = col
                break
        
        if quantity_col:
            df[quantity_col] = pd.to_numeric(df[quantity_col], errors='coerce')
            low_stock_count = len(df[df[quantity_col] < self.low_stock_threshold])
        else:
            low_stock_count = 0
        
        return {
            "total_items": len(df),
            "low_stock_items": low_stock_count,
            "low_stock_threshold": self.low_stock_threshold
        }


# Singleton instance
inventory_service = InventoryService()
