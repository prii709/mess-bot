"""
Example usage of the Inventory Automation Service.

This script demonstrates how to use the inventory service to interact with
mess inventory data stored in Google Sheets.

Prerequisites:
1. Set up a Google Cloud project with Google Sheets API enabled
2. Create a service account and download credentials JSON
3. Set the GOOGLE_SHEETS_CREDENTIALS environment variable
4. Share your Google Sheet with the service account email address
"""

import os
import json
from services.inventory_service import InventoryService


def main():
    # Check if credentials are set
    if not os.environ.get('GOOGLE_SHEETS_CREDENTIALS'):
        print("Error: GOOGLE_SHEETS_CREDENTIALS environment variable not set.")
        print("\nTo set it, run:")
        print("export GOOGLE_SHEETS_CREDENTIALS='{\"type\": \"service_account\", ...}'")
        return
    
    # Replace with your actual spreadsheet ID
    # You can find this in the Google Sheets URL:
    # https://docs.google.com/spreadsheets/d/YOUR_SPREADSHEET_ID/edit
    SPREADSHEET_ID = 'your-spreadsheet-id-here'
    
    try:
        # Initialize the inventory service
        print("Initializing inventory service...")
        service = InventoryService(
            spreadsheet_id=SPREADSHEET_ID,
            worksheet_name='inventory_sheet'
        )
        
        print("✓ Successfully connected to Google Sheets\n")
        
        # Example 1: Get all items
        print("=" * 50)
        print("ALL INVENTORY ITEMS")
        print("=" * 50)
        all_items = service.get_all_items()
        for item in all_items:
            print(f"{item['item_name']}: {item['quantity']} units")
        print()
        
        # Example 2: Look up specific item
        print("=" * 50)
        print("SPECIFIC ITEM LOOKUP")
        print("=" * 50)
        item_to_check = 'Rice'
        stock = service.get_item_stock(item_to_check)
        if stock is not None:
            print(f"{item_to_check}: {stock} units in stock")
        else:
            print(f"{item_to_check}: Item not found")
        print()
        
        # Example 3: Case-insensitive lookup
        print("=" * 50)
        print("CASE-INSENSITIVE LOOKUP")
        print("=" * 50)
        variations = ['rice', 'RICE', 'RiCe']
        for variation in variations:
            stock = service.get_item_stock(variation)
            print(f"'{variation}' -> {stock} units")
        print()
        
        # Example 4: Get low stock items
        print("=" * 50)
        print("LOW STOCK ALERT (threshold: 10)")
        print("=" * 50)
        low_stock = service.get_low_stock_items(threshold=10)
        if low_stock:
            print(f"⚠️  Found {len(low_stock)} items with low stock:")
            for item in low_stock:
                print(f"  - {item['item_name']}: {item['quantity']} units")
        else:
            print("✓ All items are well-stocked!")
        print()
        
        # Example 5: Check for missing item
        print("=" * 50)
        print("MISSING ITEM HANDLING")
        print("=" * 50)
        missing_item = 'Nonexistent Item'
        stock = service.get_item_stock(missing_item)
        if stock is None:
            print(f"'{missing_item}' is not in the inventory")
        print()
        
        # Example 6: Reload inventory (useful for getting fresh data)
        print("=" * 50)
        print("RELOAD INVENTORY")
        print("=" * 50)
        print("Reloading inventory data from Google Sheets...")
        service.reload_inventory()
        print("✓ Inventory data refreshed")
        print()
        
    except ValueError as e:
        print(f"Configuration Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure:")
        print("1. Your spreadsheet ID is correct")
        print("2. The worksheet name is 'inventory_sheet'")
        print("3. The sheet has 'item_name' and 'quantity' columns")
        print("4. The service account has access to the spreadsheet")


if __name__ == '__main__':
    main()
