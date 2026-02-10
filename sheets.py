import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)

client = gspread.authorize(creds)

SPREADSHEET_NAME = "Skylark_Drone_Data"  # your sheet file name

def get_sheet(sheet_name):
    spreadsheet = client.open(SPREADSHEET_NAME)
    return spreadsheet.worksheet(sheet_name)

def read_sheet(sheet_name):
    sheet = get_sheet(sheet_name)
    data = sheet.get_all_records()
    return pd.DataFrame(data)

# To update the data (assign pilot etc)
def update_row(sheet_name, row_index, col_name, value):
    sheet = get_sheet(sheet_name)

    headers = sheet.row_values(1)
    col_index = headers.index(col_name) + 1

    sheet.update_cell(row_index, col_index, value)
