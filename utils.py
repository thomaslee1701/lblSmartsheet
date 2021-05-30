import smartsheet
import os

API_TOKEN = os.environ['SMARTSHEET_ACCESS_TOKEN']
smart = smartsheet.Smartsheet(API_TOKEN)
smart.errors_as_exceptions(True)

# row: row object
# columnName: String
# columnMap: dictionary of columnName:columnId
# Gets the cell of the inputted column name from a row.
def getRowCell(row, columnName, columnMap):
    columnId = columnMap[columnName]
    return row.get_column(columnId)

# props: dictionary (String:String)
# sheet: sheet object
# columnMap: dictionary of columnName:columnId
# Gets the row from the inputted sheet with the inputted properties. They all have to match exactly.
# Currently using display_value for comparisons. Might switch to value.
# Returns the row if found. Returns False if not found.
def getRow(props, sheet, columnMap):
    rows = sheet.rows
    for row in rows:
        found = True
        for key in props.keys():
            if getRowCell(row, key, columnMap).display_value != props[key]:
                found = False
                break
        if found:
            return row
    return False

# props: dictionary (String:String)
# Returns a list of values in the order of the row.
def getRowValues(props, sheet, columnMap):
    row = getRow(props, sheet, columnMap)
    return [cell.display_value for cell in row.cells]

# HELPER FUNCTION for updateRowValues
# row: row object
# columnName: String
# updatedValue: String
# columnMap: dictionary of columnName:columnId
# Updates the cell value of the inputted column name from a given row.
def updateCellValue(row, columnName, updatedValue, sheet, columnMap):
    cell = getRowCell(row, columnName, columnMap)
    cell.value = updatedValue
    cell.strict = False
    updatedRow = smart.models.Row()
    updatedRow.id = row.id
    updatedRow.cells.append(cell)
    smart.Sheets.update_rows(sheet.id, [updatedRow])

# row: row object
# updatedProps: dictionary (String:String)
# Updates the values of a given row with the inputted properties from the updatedProps
def updateRowValues(row, updatedProps, sheet, columnMap):
    for key in updatedProps.keys():
        updateCellValue(row, key, updatedProps[key], sheet, columnMap)

#updateRowValues(getRow({"Name":"cheese"}), {"Name":"Josh", "Age":"10", "Salary":"100000"})
