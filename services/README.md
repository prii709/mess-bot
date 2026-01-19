# Inventory Automation Service

Backend service for reading and analyzing mess inventory data from Google Sheets.

## Features

- **Google Sheets Integration**: Secure authentication using service account credentials
- **Inventory Management**: Read and query inventory data from Google Sheets
- **Stock Lookup**: Get current stock levels for specific items
- **Low Stock Alerts**: Find items below specified thresholds
- **Pandas Integration**: Efficient data processing with pandas DataFrame

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Set up the Google Sheets service account credentials as an environment variable:

```bash
export GOOGLE_SHEETS_CREDENTIALS='{"type": "service_account", "project_id": "...", ...}'
```

The credentials JSON should contain:
- `type`: "service_account"
- `project_id`: Your Google Cloud project ID
- `private_key_id`: Service account key ID
- `private_key`: Service account private key
- `client_email`: Service account email
- `client_id`: Service account client ID
- `auth_uri`: Google OAuth2 auth URI
- `token_uri`: Google OAuth2 token URI

## Usage

### Basic Example

```python
from services.inventory_service import InventoryService

# Initialize the service with your spreadsheet ID
service = InventoryService(
    spreadsheet_id='your-spreadsheet-id',
    worksheet_name='inventory_sheet'  # Optional, defaults to 'inventory_sheet'
)

# Get stock for a specific item
stock = service.get_item_stock('Rice')
print(f"Rice stock: {stock}")

# Get items with low stock (below threshold)
low_stock_items = service.get_low_stock_items(threshold=10)
for item in low_stock_items:
    print(f"{item['item_name']}: {item['quantity']}")

# Get all items
all_items = service.get_all_items()
```

### Google Sheets Client

```python
from services.sheets_client import SheetsClient

# Initialize the client
client = SheetsClient()

# Get all records from a worksheet
records = client.get_all_records(
    spreadsheet_id='your-spreadsheet-id',
    worksheet_name='inventory_sheet'
)

# Get a specific worksheet
worksheet = client.get_worksheet(
    spreadsheet_id='your-spreadsheet-id',
    worksheet_name='inventory_sheet'
)
```

## Google Sheets Format

The inventory sheet should have the following columns:

| item_name | quantity |
|-----------|----------|
| Rice      | 100      |
| Wheat     | 50       |
| Sugar     | 5        |

Required columns:
- `item_name`: Name of the inventory item
- `quantity`: Current stock quantity (numeric)

## API Reference

### InventoryService

#### `__init__(spreadsheet_id: str, worksheet_name: str = 'inventory_sheet')`
Initialize the inventory service.

#### `get_item_stock(item_name: str) -> Optional[float]`
Get the current stock quantity for a specific item. Returns `None` if item not found.
Item lookup is case-insensitive.

#### `get_low_stock_items(threshold: float) -> List[Dict[str, float]]`
Get all items with stock below the specified threshold.

Returns a list of dictionaries with `item_name` and `quantity` keys.

#### `get_all_items() -> List[Dict[str, float]]`
Get all items in the inventory.

#### `reload_inventory()`
Reload inventory data from Google Sheets.

### SheetsClient

#### `__init__(credentials_env_var: str = 'GOOGLE_SHEETS_CREDENTIALS')`
Initialize the Google Sheets client with service account credentials.

#### `get_worksheet(spreadsheet_id: str, worksheet_name: str)`
Get a specific worksheet from a spreadsheet.

#### `get_all_records(spreadsheet_id: str, worksheet_name: str) -> list`
Get all records from a worksheet as a list of dictionaries.

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=services --cov-report=html
```

## Error Handling

The service handles the following scenarios:
- Missing credentials: Raises `ValueError`
- Invalid JSON credentials: Raises `ValueError`
- Missing required columns: Raises `ValueError`
- Item not found: Returns `None` (for `get_item_stock`)
- Empty inventory: Returns empty list (for `get_low_stock_items`)
- Non-numeric quantities: Converts to 0

## Security

- Credentials are loaded from environment variables only
- Never commit credentials to source control
- Use service accounts with minimum required permissions
- Grant read-only access to the Google Sheets
