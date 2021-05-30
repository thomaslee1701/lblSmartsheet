from utils import *
import sys

""" 
Setup code taken from example code at https://github.com/smartsheet-samples/python-read-write-sheet.
"""
# Install the smartsheet sdk with the command: pip install smartsheet-python-sdk
import smartsheet
import os

API_TOKEN = os.environ['SMARTSHEET_ACCESS_TOKEN']
smart = smartsheet.Smartsheet(API_TOKEN)
smart.errors_as_exceptions(True)

# s: String in the form {a:b,c:d,e:f} <-- no spaces between elements!
def stringToDict(s):
    # Removes the curly braces and splits the different key-value pairs
    lst = s.replace("{","").replace("}", "").split(",")
    keyValueLst = [item.split(":") for item in lst]
    retDict = {}
    for pair in keyValueLst:
        retDict[pair[0]] = pair[1]
    return retDict


def setSheetId(sheetName):
    for sheet in smart.Sheets:
        if sheet.name == sheetName:
            SHEET_ID = sheet.id

"""
Currently supported operations:
get SHEETNAME PROPS
update SHEETNAME PROPS;UPDATEDPROPS
"""

if __name__ == '__main__':
    args = sys.argv
    if len(args) != 4:
        print('Invalid args.')
    else:
        SHEET_ID = None
        for sheet in smart.Sheets.list_sheets(include_all=True).data:
            if sheet.name == args[2]:
                SHEET_ID = sheet.id
                break      
        sheet = smart.Sheets.get_sheet(SHEET_ID)

        # columnMap Source: https://github.com/smartsheet-samples/python-read-write-sheet
        # Sets up easy access to columns using column names rather than ids
        columnMap = {}
        for column in sheet.columns:
            columnMap[column.title] = column.id    

        if args[1] == 'get':
            props = stringToDict(args[3])
            print(getRowValues(props, sheet, columnMap))
        elif args[1] == 'update':
            splitArgs = args[3].split(';')
            props = stringToDict(splitArgs[0])
            updatedProps = stringToDict(splitArgs[1])
            rowToUpdate = getRow(props, sheet, columnMap)
            updateRowValues(rowToUpdate, updatedProps, sheet, columnMap)


