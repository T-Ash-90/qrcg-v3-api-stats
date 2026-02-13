# QR Code Statistics Export Tool

A simple Python script to export scan statistics for all Dynamic QR Codes in your QR Code Generator account.

---

## What It Does

- Asks for your API Key
- Lets you choose:
  - All-time scan totals  
  - Scan statistics between two dates
- Fetches all your Dynamic QR Codes
- Exports results to a CSV file
- Respects API rate limits (max 10 requests per second)

---

## Requirements

- Python 3.8+
- requests library

---

## How to Use

Run the script (run.py) and follow the prompts.

1. Enter your API Key
2. Choose:
   - `1` for all-time totals
   - `2` for date range
3. If date range, enter:
   - Start date (YYYY-MM-DD)
   - End date (YYYY-MM-DD)

---

## Output

The script creates: qr_code_statistics.csv

### All-Time Mode Columns

- QR ID  
- Title  
- Type  
- Status  
- Created At  
- Total Scans  
- Unique Scans  

### Date-Range Mode Columns

- QR ID  
- Title  
- Type  
- Status  
- Created At  
- Date  
- Total Scans  
- Unique Scans  