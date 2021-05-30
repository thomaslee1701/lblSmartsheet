""" 
Setup code taken from example code at https://github.com/smartsheet-samples/python-read-write-sheet.
"""
# Install the smartsheet sdk with the command: pip install smartsheet-python-sdk
import smartsheet
import logging
import os
import sys

API_TOKEN = os.environ['SMARTSHEET_ACCESS_TOKEN']
smart = smartsheet.Smartsheet(API_TOKEN)
smart.errors_as_exceptions(True)

sheetId = 1600831905654660
sheet = smart.Sheets.get_sheet(sheetId)

columnMap = {}
for column in sheet.columns:
    columnMap[column.title] = column.id


def getColumnDisplayValueOfRow(row, columnName):
    columnId = columnMap[columnName]
    return row.get_column(columnId).display_value

testRow = sheet.rows[1]
print(getColumnDisplayValueOfRow(testRow, "Name"))

"""
if __name__ == "__main__":
    args = sys.argv
    if (len(args) != 2):
        print('Invalid args. Please input a single string in the form [[org=xyz company; phase=nda; task=execute NDA; in progress; 25%;awaiting response from collaborator]]')
"""
