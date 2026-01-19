# Mess Bot - FastAPI Automation Bot for Mess Management

A Python FastAPI-based automation bot for hostel/college mess management that uses Google Sheets as a database. This bot provides intelligent chat-based interactions for managing inventory, attendance, and feedback data.

## Features

- **Google Sheets Integration**: Uses Google Sheets API via service account for data storage
- **Intelligent Chat Interface**: POST `/chat` endpoint with rule-based intent detection
- **Inventory Management**: Query stock levels and receive low stock alerts
- **Attendance Tracking**: View statistics and predict next-day attendance
- **Feedback Analysis**: Calculate average ratings and identify low-rated meals
- **Automated Alerts**: Daily scheduled tasks for monitoring stock and ratings
- **Modular Architecture**: Clean separation of concerns with service-based design

## Architecture

```
app/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration management
├── models/
│   └── schemas.py         # Pydantic models for requests/responses
└── services/
    ├── sheets_service.py      # Google Sheets API integration
    ├── intent_service.py      # Rule-based intent detection
    ├── inventory_service.py   # Inventory management logic
    ├── attendance_service.py  # Attendance tracking and prediction
    ├── feedback_service.py    # Feedback analysis
    ├── chat_service.py        # Chat request handling
    └── scheduler_service.py   # APScheduler for daily automation
```

## Setup

### Prerequisites

- Python 3.8+
- Google Cloud Service Account with Google Sheets API enabled
- Google Sheets for inventory, attendance, and feedback data

### Installation

1. Clone the repository:
```bash
git clone https://github.com/prii709/mess-bot.git
cd mess-bot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up Google Sheets credentials:
   - Create a Google Cloud project
   - Enable Google Sheets API
   - Create a service account and download the JSON credentials
   - Save the credentials as `service_account.json` in the project root
   - Share your Google Sheets with the service account email

5. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your Google Sheets IDs and configuration
```

### Configuration

Edit `.env` file with your settings:

```env
GOOGLE_SHEETS_CREDENTIALS_PATH=service_account.json
INVENTORY_SHEET_ID=your_inventory_sheet_id_here
ATTENDANCE_SHEET_ID=your_attendance_sheet_id_here
FEEDBACK_SHEET_ID=your_feedback_sheet_id_here
HOST=0.0.0.0
PORT=8000
LOW_STOCK_THRESHOLD=10
LOW_RATING_THRESHOLD=2.5
```

## Usage

### Running the Server

```bash
python -m app.main
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### POST /chat

Main chat endpoint for interacting with the bot.

**Request:**
```json
{
  "message": "What is the current inventory?"
}
```

**Response:**
```json
{
  "intent": "inventory_query",
  "response": "Inventory Summary: 25 total items, 3 items with low stock",
  "data": {
    "summary": {
      "total_items": 25,
      "low_stock_items": 3
    }
  }
}
```

### Supported Intents

1. **inventory_query**: Query inventory items
   - Example: "Show me the inventory", "Check stock for rice"

2. **low_stock_alert**: Get low stock alerts
   - Example: "Any low stock alerts?", "What needs restocking?"

3. **attendance_stats**: Get attendance statistics
   - Example: "Show attendance stats", "How many students are present?"

4. **attendance_prediction**: Predict next day attendance
   - Example: "Predict tomorrow's attendance", "Expected attendance for next day"

5. **feedback_average**: Get average feedback ratings
   - Example: "What's the average feedback?", "How are the ratings?"

6. **low_rating_alert**: Get low rating alerts
   - Example: "Any poor ratings?", "Show low rating alerts"

### Other Endpoints

- `GET /`: Health check
- `GET /health`: Detailed health status
- `GET /scheduler/jobs`: View scheduled jobs
- `GET /config`: View configuration (non-sensitive)

## Google Sheets Format

### Inventory Sheet

Expected columns:
- `item_name` or `Item Name` or `name`: Name of the item
- `quantity` or `Quantity` or `qty`: Stock quantity
- `unit`: Unit of measurement
- `last_updated`: Last update timestamp (optional)

### Attendance Sheet

Expected columns:
- `date` or `Date`: Date of record
- `present` or `Present`: Number of students present
- `absent` or `Absent`: Number of students absent
- `total` or `Total`: Total number of students

### Feedback Sheet

Expected columns:
- `date` or `Date`: Date of feedback
- `meal_type` or `Meal Type`: Type of meal (breakfast/lunch/dinner)
- `rating` or `Rating`: Rating score (1-5)
- `comments`: Optional feedback comments

## Scheduled Tasks

The bot runs the following automated tasks:

- **Daily Low Stock Check** (8:00 AM): Checks for items below threshold
- **Daily Low Rating Check** (9:00 PM): Checks for meals with poor ratings

## Development

### Project Structure

- **Modular Services**: Each service handles a specific domain (inventory, attendance, feedback)
- **Dependency Injection**: Services are singleton instances imported where needed
- **Configuration Management**: Centralized config using pydantic-settings
- **Type Safety**: Pydantic models for request/response validation
- **Pandas Processing**: All data processing uses pandas DataFrames
- **APScheduler**: Background scheduler for automated tasks

### Security

- Service account credentials are excluded from git (`.gitignore`)
- Use `.env` for configuration (not committed)
- Example configuration provided in `.env.example`

## Technologies Used

- **FastAPI**: Modern web framework for building APIs
- **Pandas**: Data processing and analysis
- **gspread**: Google Sheets Python API
- **APScheduler**: Task scheduling
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License