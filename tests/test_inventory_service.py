"""
Unit tests for InventoryService module.
"""

import os
import json
import pytest
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
from services.inventory_service import InventoryService


class TestInventoryService:
    """Test cases for InventoryService class."""
    
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
        }
    
    @pytest.fixture
    def mock_inventory_data(self):
        """Fixture providing sample inventory data."""
        return [
            {'item_name': 'Rice', 'quantity': 100},
            {'item_name': 'Wheat', 'quantity': 50},
            {'item_name': 'Sugar', 'quantity': 5},
            {'item_name': 'Salt', 'quantity': 0},
            {'item_name': 'Oil', 'quantity': 25},
        ]
    
    @patch('services.inventory_service.SheetsClient')
    def test_init_loads_inventory(self, mock_sheets_client, mock_credentials, mock_inventory_data):
        """Test that initialization loads inventory data."""
        creds_json = json.dumps(mock_credentials)
        
        mock_client_instance = Mock()
        mock_client_instance.get_all_records.return_value = mock_inventory_data
        mock_sheets_client.return_value = mock_client_instance
        
        with patch.dict(os.environ, {'GOOGLE_SHEETS_CREDENTIALS': creds_json}):
            service = InventoryService('test-spreadsheet-id')
            
            assert service.inventory_df is not None
            assert len(service.inventory_df) == 5
            mock_client_instance.get_all_records.assert_called_once()
    
    @patch('services.inventory_service.SheetsClient')
    def test_get_item_stock_existing_item(self, mock_sheets_client, mock_credentials, mock_inventory_data):
        """Test getting stock for an existing item."""
        creds_json = json.dumps(mock_credentials)
        
        mock_client_instance = Mock()
        mock_client_instance.get_all_records.return_value = mock_inventory_data
        mock_sheets_client.return_value = mock_client_instance
        
        with patch.dict(os.environ, {'GOOGLE_SHEETS_CREDENTIALS': creds_json}):
            service = InventoryService('test-spreadsheet-id')
            stock = service.get_item_stock('Rice')
            
            assert stock == 100.0
    
    @patch('services.inventory_service.SheetsClient')
    def test_get_item_stock_case_insensitive(self, mock_sheets_client, mock_credentials, mock_inventory_data):
        """Test that item lookup is case-insensitive."""
        creds_json = json.dumps(mock_credentials)
        
        mock_client_instance = Mock()
        mock_client_instance.get_all_records.return_value = mock_inventory_data
        mock_sheets_client.return_value = mock_client_instance
        
        with patch.dict(os.environ, {'GOOGLE_SHEETS_CREDENTIALS': creds_json}):
            service = InventoryService('test-spreadsheet-id')
            
            assert service.get_item_stock('rice') == 100.0
            assert service.get_item_stock('RICE') == 100.0
            assert service.get_item_stock('RiCe') == 100.0
    
    @patch('services.inventory_service.SheetsClient')
    def test_get_item_stock_missing_item(self, mock_sheets_client, mock_credentials, mock_inventory_data):
        """Test getting stock for a missing item returns None."""
        creds_json = json.dumps(mock_credentials)
        
        mock_client_instance = Mock()
        mock_client_instance.get_all_records.return_value = mock_inventory_data
        mock_sheets_client.return_value = mock_client_instance
        
        with patch.dict(os.environ, {'GOOGLE_SHEETS_CREDENTIALS': creds_json}):
            service = InventoryService('test-spreadsheet-id')
            stock = service.get_item_stock('Nonexistent Item')
            
            assert stock is None
    
    @patch('services.inventory_service.SheetsClient')
    def test_get_item_stock_zero_quantity(self, mock_sheets_client, mock_credentials, mock_inventory_data):
        """Test getting stock for an item with zero quantity."""
        creds_json = json.dumps(mock_credentials)
        
        mock_client_instance = Mock()
        mock_client_instance.get_all_records.return_value = mock_inventory_data
        mock_sheets_client.return_value = mock_client_instance
        
        with patch.dict(os.environ, {'GOOGLE_SHEETS_CREDENTIALS': creds_json}):
            service = InventoryService('test-spreadsheet-id')
            stock = service.get_item_stock('Salt')
            
            assert stock == 0.0
    
    @patch('services.inventory_service.SheetsClient')
    def test_get_low_stock_items(self, mock_sheets_client, mock_credentials, mock_inventory_data):
        """Test getting items below a threshold."""
        creds_json = json.dumps(mock_credentials)
        
        mock_client_instance = Mock()
        mock_client_instance.get_all_records.return_value = mock_inventory_data
        mock_sheets_client.return_value = mock_client_instance
        
        with patch.dict(os.environ, {'GOOGLE_SHEETS_CREDENTIALS': creds_json}):
            service = InventoryService('test-spreadsheet-id')
            low_stock = service.get_low_stock_items(threshold=10)
            
            assert len(low_stock) == 2
            item_names = [item['item_name'] for item in low_stock]
            assert 'Sugar' in item_names
            assert 'Salt' in item_names
    
    @patch('services.inventory_service.SheetsClient')
    def test_get_low_stock_items_high_threshold(self, mock_sheets_client, mock_credentials, mock_inventory_data):
        """Test getting items with a high threshold."""
        creds_json = json.dumps(mock_credentials)
        
        mock_client_instance = Mock()
        mock_client_instance.get_all_records.return_value = mock_inventory_data
        mock_sheets_client.return_value = mock_client_instance
        
        with patch.dict(os.environ, {'GOOGLE_SHEETS_CREDENTIALS': creds_json}):
            service = InventoryService('test-spreadsheet-id')
            low_stock = service.get_low_stock_items(threshold=50)
            
            assert len(low_stock) == 3
            quantities = [item['quantity'] for item in low_stock]
            assert all(q < 50 for q in quantities)
    
    @patch('services.inventory_service.SheetsClient')
    def test_get_low_stock_items_no_results(self, mock_sheets_client, mock_credentials, mock_inventory_data):
        """Test getting low stock items when none exist below threshold."""
        creds_json = json.dumps(mock_credentials)
        
        mock_client_instance = Mock()
        mock_client_instance.get_all_records.return_value = mock_inventory_data
        mock_sheets_client.return_value = mock_client_instance
        
        with patch.dict(os.environ, {'GOOGLE_SHEETS_CREDENTIALS': creds_json}):
            service = InventoryService('test-spreadsheet-id')
            low_stock = service.get_low_stock_items(threshold=0)
            
            assert len(low_stock) == 0
    
    @patch('services.inventory_service.SheetsClient')
    def test_get_all_items(self, mock_sheets_client, mock_credentials, mock_inventory_data):
        """Test getting all inventory items."""
        creds_json = json.dumps(mock_credentials)
        
        mock_client_instance = Mock()
        mock_client_instance.get_all_records.return_value = mock_inventory_data
        mock_sheets_client.return_value = mock_client_instance
        
        with patch.dict(os.environ, {'GOOGLE_SHEETS_CREDENTIALS': creds_json}):
            service = InventoryService('test-spreadsheet-id')
            all_items = service.get_all_items()
            
            assert len(all_items) == 5
            assert all('item_name' in item and 'quantity' in item for item in all_items)
    
    @patch('services.inventory_service.SheetsClient')
    def test_reload_inventory(self, mock_sheets_client, mock_credentials, mock_inventory_data):
        """Test reloading inventory data."""
        creds_json = json.dumps(mock_credentials)
        
        mock_client_instance = Mock()
        mock_client_instance.get_all_records.return_value = mock_inventory_data
        mock_sheets_client.return_value = mock_client_instance
        
        with patch.dict(os.environ, {'GOOGLE_SHEETS_CREDENTIALS': creds_json}):
            service = InventoryService('test-spreadsheet-id')
            
            # Modify the inventory data for the second call
            new_data = [{'item_name': 'New Item', 'quantity': 999}]
            mock_client_instance.get_all_records.return_value = new_data
            
            service.reload_inventory()
            
            assert len(service.inventory_df) == 1
            assert service.get_item_stock('New Item') == 999.0
            assert mock_client_instance.get_all_records.call_count == 2
    
    @patch('services.inventory_service.SheetsClient')
    def test_missing_required_columns_raises_error(self, mock_sheets_client, mock_credentials):
        """Test that missing required columns raises ValueError."""
        creds_json = json.dumps(mock_credentials)
        
        invalid_data = [{'name': 'Rice', 'stock': 100}]  # Wrong column names
        
        mock_client_instance = Mock()
        mock_client_instance.get_all_records.return_value = invalid_data
        mock_sheets_client.return_value = mock_client_instance
        
        with patch.dict(os.environ, {'GOOGLE_SHEETS_CREDENTIALS': creds_json}):
            with pytest.raises(ValueError) as exc_info:
                InventoryService('test-spreadsheet-id')
            assert "must contain columns" in str(exc_info.value)
    
    @patch('services.inventory_service.SheetsClient')
    def test_custom_worksheet_name(self, mock_sheets_client, mock_credentials, mock_inventory_data):
        """Test using a custom worksheet name."""
        creds_json = json.dumps(mock_credentials)
        
        mock_client_instance = Mock()
        mock_client_instance.get_all_records.return_value = mock_inventory_data
        mock_sheets_client.return_value = mock_client_instance
        
        with patch.dict(os.environ, {'GOOGLE_SHEETS_CREDENTIALS': creds_json}):
            service = InventoryService('test-spreadsheet-id', 'custom_sheet')
            
            assert service.worksheet_name == 'custom_sheet'
            mock_client_instance.get_all_records.assert_called_with(
                'test-spreadsheet-id', 
                'custom_sheet'
            )
    
    @patch('services.inventory_service.SheetsClient')
    def test_handles_non_numeric_quantities(self, mock_sheets_client, mock_credentials):
        """Test that non-numeric quantities are handled gracefully."""
        creds_json = json.dumps(mock_credentials)
        
        data_with_invalid = [
            {'item_name': 'Rice', 'quantity': '100'},  # String number
            {'item_name': 'Wheat', 'quantity': 'N/A'},  # Non-numeric
            {'item_name': 'Sugar', 'quantity': 50},     # Valid number
        ]
        
        mock_client_instance = Mock()
        mock_client_instance.get_all_records.return_value = data_with_invalid
        mock_sheets_client.return_value = mock_client_instance
        
        with patch.dict(os.environ, {'GOOGLE_SHEETS_CREDENTIALS': creds_json}):
            service = InventoryService('test-spreadsheet-id')
            
            assert service.get_item_stock('Rice') == 100.0
            assert service.get_item_stock('Wheat') == 0.0  # N/A converted to 0
            assert service.get_item_stock('Sugar') == 50.0
