from googleapiclient.discovery import build
from IPython.display import  JSON
import pandas as pd
from datetime import datetime 
import gspread # high level api ontop of the operations you can perform on the sheet
from google.oauth2.service_account import Credentials
import os

from Analysis.video_level_analysis import final
from Analysis.search_request import search_query

from dotenv import load_dotenv
load_dotenv()
sheet_id = os.getenv("SHEET_ID")
api_key = os.getenv("API_KEY")
from gspread_dataframe import get_as_dataframe, set_with_dataframe

api_service_name = "youtube"
api_version = "v3"


youtube = build(api_service_name, api_version, developerKey=api_key)



# differnet things you can do on the file
scopes = ["https://www.googleapis.com/auth/spreadsheets"] # View the Sheet function
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes) # Link Credentials file that contains keys and more
client = gspread.authorize(creds) # Authorize the credentials, returns a client to access different google sheets 

# Id of the Google Sheet we want to access
workbook = client.open_by_key(sheet_id) # Open the Spread sheet

# When user runs the program, by default it will Create a worksheet, with the search query as the title
#   First row: Keywords from Genre
#   Rest: Final Data 


worksheet_list = map(lambda x: x.title, workbook.worksheets())
new_worksheet_names = search_query

if new_worksheet_names in worksheet_list:
    sheet = workbook.worksheet(new_worksheet_names)

else:
    sheet = workbook.add_worksheet(new_worksheet_names, rows=1000, cols=1000)


sheet.clear() 
set_with_dataframe(sheet, final)




# #VIEW SHEETS W/TITLE
# sheets = map(lambda x: x.title, workbook.worksheets()) # Contain ID and Title
# print(list(sheets))

# # #MODIFYING SHEET TITLE
# sheet = workbook.worksheet("Sheet1")
# sheet.update_title("Hello World")

# # #MODIFYING INDIVIDUAL CELLS
# sheet = workbook.worksheet("Hello World")
# sheet.update_acell('A1', "TEST") # Using A1 Notation
# sheet.update_cell(2,1, "HI") # Using Coordinate Mapping

# READ VALUE OF CELL
# value = sheet.acell("A1").value
# print(value)

# FIND CELL USING VALUE
# cell = sheet.find("this is the value")
# print(cell.row, cell.col)


# FORMAT A CELL BLOCK 
# sheet.fomat("A1", {"textFormat: {bold: True}"})