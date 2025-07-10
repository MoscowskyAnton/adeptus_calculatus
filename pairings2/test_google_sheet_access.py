# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 12:13:05 2025

@author: 79165
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import numpy as np

# Define the scope for Google Sheets and Drive API
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

# Authenticate using the service account credentials file
creds = ServiceAccountCredentials.from_json_keyfile_name('C:/Users/79165/Downloads/tlenpairings-3eb977831fce.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheet by its name
spreadsheet = client.open("TLEN FEST JUL\'25")

# Access the worksheet by its exact sheet name (case-sensitive)

worksheets = spreadsheet.worksheets()

# Extract and print all sheet names
sheet_names = [ws.title for ws in worksheets]
print(sheet_names)

worksheet = spreadsheet.worksheet('Team: Knut')


data = worksheet.acell('B7').value
print(data)

data = worksheet.get('D7:K30')
#print(data)

full_len = 8
def_value = 0
ch = []
for d in data:
    dc = [def_value if i == '' else int(i) for i in d]
    for i in range(len(dc), full_len):
        dc.append(def_value)
    ch.append(dc)

#print(ch)
data_formed = np.array(ch).reshape(8, 3, 8).transpose(0, 2, 1)

print(data_formed)