
import regexFrontend as rf
import regexBackend as rb
import sys
import ast
import json
import numpy

def get_saved_regex_lists():
    with open('src/Tasks/RegExp/JSONFiles/regex_lists.json', 'r') as file:
        data = json.load(file)
        return data['rows'], data['columns']
    
def createValidationMatrix(userData,regexListAllRows, regexListAllColumns):
    matrixColumns = len(userData[0]) if userData else 0
    matrixRows= len(userData)
    validationmatrix = [[None for _ in range(matrixColumns)] for _ in range(matrixRows)]
    for row_index in range(matrixRows):
        for col_index in range(matrixColumns):
            user_input = userData[row_index][col_index]
            
            if user_input is None:
                validationmatrix[row_index][col_index] = None
            elif rb.check_input(user_input, regexListAllColumns[col_index][row_index], regexListAllRows[row_index][col_index]):
                validationmatrix[row_index][col_index] = True
            else:
                validationmatrix[row_index][col_index] = False
    return validationmatrix


def validateRegex(userData):
    
    regexListAllRows, regexListAllColumns = get_saved_regex_lists()
    validationmatrix=createValidationMatrix(userData,regexListAllRows, regexListAllColumns)
    with open("src/Tasks/RegExp/JSONFiles/validationmatrix.json", "w") as f:
        json.dump(validationmatrix, f)
    return validationmatrix

if __name__ == "__main__":
    with open('src/Tasks/RegExp/JSONFiles/userData.json', 'r') as file:
        loaded_matrix = json.load(file)
    validateRegex(loaded_matrix)
       
