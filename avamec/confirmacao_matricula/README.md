# Google Sheets Automation

This script automates the creation of city-specific Google Sheets from a Master Spreadsheet.

## Prerequisites

1.  **Python 3**: Ensure Python is installed.
2.  **Google Cloud Project**:
    - Enable **Google Sheets API** and **Google Drive API**.
    - Create a **Service Account**.
    - Download the JSON key file and rename it to `service_account.json`.
    - **Important**: Share your Master Spreadsheet with the Service Account email address (found in the JSON file) so it can read it.

## Setup

1.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2.  Configure the script (`automate_sheets.py`):
    - Open `automate_sheets.py`.
    - Update `MASTER_SPREADSHEET_ID` with the ID of your master sheet (found in the URL).
    - Update `CITIES_TAB_NAME` if your list of cities is in a different tab.
    - Update `CITY_COLUMN_INDEX` if the city names are not in the first column (Column A = 0).

3.  Place your `service_account.json` in this directory.

## Running the Script

```bash
python automate_sheets.py
```

## Notes

- The script will create a new spreadsheet for each city found in the list.
- It will rename the file to the City Name.
- It will update the cell in 'Status de confirmação de matrícula' (currently set to A1, change in script if needed).
- It will hide other tabs.
- It will restrict download/copy permissions for viewers.
- **#REF! Errors**: As noted in the plan, you may still need to manually open the sheets and click "Allow Access" for `IMPORTRANGE` formulas if they reference other sheets. The API cannot bypass this security feature.
