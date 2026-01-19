# Google Sheets Templates

This document provides templates for the Google Sheets that should be set up for the Mess Bot application.

## 1. Inventory Sheet Template

**Sheet Name:** Inventory (or any name you prefer)

**Columns:**
| item_name | quantity | unit | last_updated |
|-----------|----------|------|--------------|
| Rice      | 50       | kg   | 2024-01-15   |
| Wheat     | 30       | kg   | 2024-01-15   |
| Milk      | 20       | liters | 2024-01-16 |
| Sugar     | 8        | kg   | 2024-01-16   |
| Oil       | 15       | liters | 2024-01-14 |

**Required Columns:**
- `item_name` (or `Item Name` or `name`): Name of the inventory item
- `quantity` (or `Quantity` or `qty` or `stock` or `Stock`): Quantity in stock (numeric)
- `unit`: Unit of measurement (optional)
- `last_updated`: Last update date (optional)

**Notes:**
- Items with quantity below the `LOW_STOCK_THRESHOLD` will trigger alerts
- The sheet accepts various column name formats (case-insensitive)

---

## 2. Attendance Sheet Template

**Sheet Name:** Attendance (or any name you prefer)

**Columns:**
| date       | present | absent | total |
|------------|---------|--------|-------|
| 2024-01-15 | 245     | 5      | 250   |
| 2024-01-16 | 238     | 12     | 250   |
| 2024-01-17 | 248     | 2      | 250   |
| 2024-01-18 | 240     | 10     | 250   |
| 2024-01-19 | 242     | 8      | 250   |

**Required Columns:**
- `date` (or `Date` or `DATE`): Date of the attendance record
- `present` (or `Present` or `PRESENT`): Number of students present
- `absent` (or `Absent` or `ABSENT`): Number of students absent
- `total` (or `Total` or `TOTAL`): Total number of students (optional)

**Notes:**
- More historical data improves attendance prediction accuracy
- The prediction algorithm uses the last 7 days of data
- Dates should be in a consistent format (YYYY-MM-DD recommended)

---

## 3. Feedback Sheet Template

**Sheet Name:** Feedback (or any name you prefer)

**Columns:**
| date       | meal_type | rating | comments                        |
|------------|-----------|--------|---------------------------------|
| 2024-01-15 | breakfast | 4.5    | Good variety, fresh items       |
| 2024-01-15 | lunch     | 4.0    | Tasty, good quantity            |
| 2024-01-15 | dinner    | 3.5    | Could be warmer                 |
| 2024-01-16 | breakfast | 4.2    | Excellent                       |
| 2024-01-16 | lunch     | 2.0    | Cold food, needs improvement    |

**Required Columns:**
- `date` (or `Date` or `DATE`): Date of the feedback
- `meal_type` (or `Meal Type` or `meal` or `type`): Type of meal (breakfast/lunch/dinner)
- `rating` (or `Rating` or `RATING` or `score`): Rating score (1-5 scale recommended)
- `comments`: Optional feedback comments

**Notes:**
- Ratings below `LOW_RATING_THRESHOLD` will trigger alerts
- The sheet accepts various column name formats (case-insensitive)
- Multiple feedback entries per day are supported

---

## Setting Up Google Sheets

### Step 1: Create Your Sheets
1. Create three Google Sheets (one for each: Inventory, Attendance, Feedback)
2. Add the column headers as shown in the templates above
3. Add some initial data to test the system

### Step 2: Get Sheet IDs
1. Open each Google Sheet in your browser
2. Copy the Sheet ID from the URL:
   ```
   https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit
   ```
3. Save these IDs for your `.env` file

### Step 3: Share with Service Account
1. In each Google Sheet, click "Share" button
2. Add the service account email (found in your `service_account.json` file)
3. Give "Editor" permissions
4. Click "Send" (uncheck "Notify people" if you don't want an email)

### Step 4: Configure Environment
Update your `.env` file with the Sheet IDs:
```env
INVENTORY_SHEET_ID=your_inventory_sheet_id_here
ATTENDANCE_SHEET_ID=your_attendance_sheet_id_here
FEEDBACK_SHEET_ID=your_feedback_sheet_id_here
```

---

## Notes on Data Format

- **Column Names**: The application is flexible with column names and accepts various formats (case-insensitive)
- **Dates**: Use a consistent date format. YYYY-MM-DD is recommended for best compatibility
- **Numbers**: Make sure quantity and rating columns contain numeric values
- **Empty Rows**: Empty rows at the end of the sheet are ignored
- **Missing Columns**: If optional columns are missing, the application will work with available data

---

## Testing Your Setup

Once configured, you can test your sheets by:
1. Starting the application
2. Using the `/chat` endpoint with queries like:
   - "Show me the inventory"
   - "What's the attendance statistics?"
   - "Show average feedback rating"

The application will fetch data directly from your Google Sheets and process it in real-time.
