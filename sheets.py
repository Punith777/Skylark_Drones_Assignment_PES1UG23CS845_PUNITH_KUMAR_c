import json
import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


# Google Sheets access scope
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from Streamlit secrets
creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])

creds = ServiceAccountCredentials.from_json_keyfile_dict(
    creds_dict,
    scope
)

# Authorize Google client
client = gspread.authorize(creds)

# Spreadsheet name
SPREADSHEET_NAME = "Skylark_Drone_Data"


# ---------------------------
# Get worksheet
# ---------------------------
def get_sheet(sheet_name):
    spreadsheet = client.open(SPREADSHEET_NAME)
    return spreadsheet.worksheet(sheet_name)


# ---------------------------
# Read sheet as DataFrame
# ---------------------------
def read_sheet(sheet_name):
    sheet = get_sheet(sheet_name)
    data = sheet.get_all_records()
    return pd.DataFrame(data)


# ---------------------------
# Update a cell value
# ---------------------------
def update_row(sheet_name, row_index, col_name, value):
    sheet = get_sheet(sheet_name)

    headers = sheet.row_values(1)
    col_index = headers.index(col_name) + 1

    sheet.update_cell(row_index, col_index, value)
