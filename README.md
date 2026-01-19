# mess-bot

Backend service for mess inventory automation.

## Overview

This project provides a backend service that reads and analyzes mess inventory data from Google Sheets. It enables automated stock monitoring and provides an API for integration with automation bots.

## Features

- 📊 **Google Sheets Integration**: Seamless connection to inventory data via Google Sheets API
- 🔍 **Stock Lookup**: Query current stock levels for any item
- ⚠️ **Low Stock Alerts**: Identify items below configurable thresholds
- 🔐 **Secure Authentication**: Service account-based authentication with environment variable configuration
- ✅ **Well-Tested**: Comprehensive test suite with 19+ unit tests
- 📝 **Fully Documented**: Complete API documentation and usage examples

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/prii709/mess-bot.git
cd mess-bot

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. Create a Google Cloud service account with Google Sheets API access
2. Download the credentials JSON file
3. Set the credentials as an environment variable:

```bash
export GOOGLE_SHEETS_CREDENTIALS='{"type": "service_account", "project_id": "...", ...}'
```

### Usage

```python
from services.inventory_service import InventoryService

# Initialize the service
service = InventoryService(spreadsheet_id='your-spreadsheet-id')

# Get stock for an item
stock = service.get_item_stock('Rice')
print(f"Rice stock: {stock}")

# Get items with low stock
low_stock = service.get_low_stock_items(threshold=10)
for item in low_stock:
    print(f"{item['item_name']}: {item['quantity']}")
```

See `example_usage.py` for more comprehensive examples.

## Project Structure

```
mess-bot/
├── services/
│   ├── sheets_client.py      # Google Sheets API client
│   ├── inventory_service.py  # Inventory management service
│   └── README.md             # Detailed service documentation
├── tests/
│   ├── test_sheets_client.py
│   └── test_inventory_service.py
├── requirements.txt          # Python dependencies
├── example_usage.py          # Usage examples
└── README.md                 # This file
```

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

All 19 tests should pass:
- 13 tests for inventory service functionality
- 6 tests for Google Sheets client

## API Documentation

### InventoryService

**`get_item_stock(item_name: str) -> Optional[float]`**
- Returns the current stock quantity for an item
- Case-insensitive lookup
- Returns `None` if item not found

**`get_low_stock_items(threshold: float) -> List[Dict]`**
- Returns items with stock below the threshold
- Returns list of dicts with `item_name` and `quantity`

**`get_all_items() -> List[Dict]`**
- Returns all items in the inventory

**`reload_inventory()`**
- Refreshes inventory data from Google Sheets

See `services/README.md` for complete API documentation.

## Requirements

- Python 3.8+
- Google Sheets API enabled in Google Cloud
- Service account with Sheets read access

## Security

- Credentials loaded via environment variables only
- No hardcoded secrets in codebase
- Service account with minimum required permissions
- CodeQL security scans: 0 vulnerabilities

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please ensure:
- All tests pass
- Code follows existing style
- New features include tests
- Documentation is updated