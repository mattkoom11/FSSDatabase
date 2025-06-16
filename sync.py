import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Step 1: Google Sheets auth
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Step 2: Open spreadsheet
spreadsheet = client.open("Client Information")
worksheet = spreadsheet.worksheet("Clients Database")

# Step 3: Read all data
all_values = worksheet.get_all_values()

# Step 4: Header starts at row 10 (index 9)
header_row_index = 9
headers = all_values[header_row_index]
data_rows = all_values[header_row_index + 1:]

# Step 5: Build DataFrame
df = pd.DataFrame(data_rows, columns=headers)
df.columns = df.columns.str.strip()  # remove whitespace around column names
df = df.loc[:, df.columns != '']     # remove blank column headers

# Step 6: Remove rows missing client name
if 'CLIENT NAME' in df.columns:
    df = df[df['CLIENT NAME'].str.strip() != '']
    df = df.dropna(subset=['CLIENT NAME'])

# Preview
print("📋 Cleaned Columns:", df.columns.tolist())
print("🧪 First clean row of data:")
print(df.iloc[0])
