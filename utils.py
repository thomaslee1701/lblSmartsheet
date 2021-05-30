""" 
Setup code taken from example code at https://github.com/smartsheet-samples/python-read-write-sheet.
"""
# Install the smartsheet sdk with the command: pip install smartsheet-python-sdk
import smartsheet
import os

API_TOKEN = os.environ['SMARTSHEET_ACCESS_TOKEN']
smart = smartsheet.Smartsheet(API_TOKEN)
smart.errors_as_exceptions(True)

SHEET_ID = 1600831905654660
sheet = smart.Sheets.get_sheet(SHEET_ID)

# Sets up easy access to columns using column names rather than ids
columnMap = {}
for column in sheet.columns:
    columnMap[column.title] = column.id

# row: row object
# columnName: String
# Gets the cell of the inputted column name from a row.
def getRowCell(row, columnName):
    columnId = columnMap[columnName]
    return row.get_column(columnId)

# props: dictionary (String:String)
# Gets the row from the inputted sheet with the inputted properties. They all have to match exactly.
# Currently using display_value for comparisons. Might switch to value.
# Returns the row if found. Returns False if not found.
def getRow(props):
    rows = sheet.rows
    for row in rows:
        found = True
        for key in props.keys():
            if getRowCell(row, key).display_value != props[key]:
                found = False
                break
        if found:
            return row
    return False

# props: dictionary (String:String)
# Returns a list of values in the order of the row.
def getRowValues(props):
    row = getRow(props)
    return [cell.display_value for cell in row.cells]

# HELPER FUNCTION for updateRowValues
# row: row object
# columnName: String
# updatedValue: String
# Updates the cell value of the inputted column name from a given row.
def updateCellValue(row, columnName, updatedValue):
    cell = getRowCell(row, columnName)
    cell.value = updatedValue;
    updatedRow = smart.models.Row()
    updatedRow.id = row.id
    updatedRow.cells.append(cell)
    smart.Sheets.update_rows(SHEET_ID, [updatedRow])

# row: row object
# updatedProps: dictionary (String:String)
# Updates the values of a given row with the inputted properties from the updatedProps
def updateRowValues(row, updatedProps):
    for key in updatedProps.keys():
        updateCellValue(row, key, updatedProps[key])

#updateRowValues(getRow({"Name":"cheese"}), {"Name":"Josh", "Age":"10", "Salary":"100000"})
