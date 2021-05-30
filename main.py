from utils import *
import sys
import json

# s: String in the form {a:b,c:d,e:f} <-- no spaces between elements!
def stringToDict(s):
    # Removes the curly braces and splits the different key-value pairs
    lst = s.replace("{","").replace("}", "").split(",")
    keyValueLst = [item.split(":") for item in lst]
    retDict = {}
    for pair in keyValueLst:
        retDict[pair[0]] = pair[1]
    return retDict

"""
Currently supported operations:
get PROPS
update PROPS;UPDATEDPROPS
"""


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 3:
        print('Invalid args.')    
    elif args[1] == 'get':
        props = stringToDict(args[2])
        print(getRowValues(props))
    elif args[1] == 'update':
        splitArgs = args[2].split(';')
        props = stringToDict(splitArgs[0])
        updatedProps = stringToDict(splitArgs[1])
        rowToUpdate = getRow(props)
        updateRowValues(rowToUpdate, updatedProps)

