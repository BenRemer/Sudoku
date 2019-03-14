import numpy as np
from collections import Counter

complete_list = '123456789'
max_tries = 20

def check_row(matrix, number, row):
    # print('checking number', number, 'on row', row)
    for i in range(9):
        # print('row', matrix[row][i])
        if matrix[row][i] == number:
            # print('number found')
            return False
    # print('good number')
    return True

def check_col(matrix, number, col):
    # print('checking number', number, 'on col', col)
    for i in range(9):
        # print('row', matrix[i][col])
        if matrix[i][col] == number:
            # print('number found')
            return False
    # print('good number')
    return True

def find_block(number):
    if number > 5:
        return 6
    elif number > 2:
        return 3
    else:
        return 0

def check_square(matrix, number, row, col):
    # print(col,row)
    block_col = find_block(col)
    block_row = find_block(row)
    # print('square col,row', block_col, block_row)
    if np.any(matrix[block_row:block_row+3, block_col:block_col+3] == number): # Checks 3x3 block
        # print('number found')
        return False
    # print('good number')
    return True

def complete_check(matrix, number, row, col):
    row_checked = check_row(matrix, number, row)
    col_checked = check_col(matrix, number, col)
    block_checked = check_square(matrix, number, row, col)
    if not row_checked or not col_checked or not block_checked:
        return False
    return True

def check_one_number(number):
    # number = matrix[row][col]
    # print(number)
    return {
        1 : True,
        2 : True,
        3 : True,
        4 : True,
        5 : True,
        6 : True,
        7 : True,
        8 : True,
        9 : True
    }.get(number, False)

def check_remove(row, col, test_row, test_col):
    returnState = False
    if row == test_row:
        returnState = True
    elif col == test_col:
        returnState = True

    block_col = find_block(col)
    block_row = find_block(row)
    test_block_col = find_block(test_col)
    test_block_row = find_block(test_row)

    if block_row == test_block_row and block_col == test_block_col:
        returnState = True

    return returnState

def naked_singels(matrix):
    empyt_squares = {} # Empty Dictionary 
    locations = [] # List of locations
    for row in range(9): # For each row
        for col in range(9): # For each col
            if matrix[row][col] != 0.0: # If number is 0 already, skip
                continue
            empyt_squares[(row,col)] = complete_list # this row,col is set to all numbers
            locations.append((row,col)) # row,col is saved
            # print(empyt_squares[(row,col)])
            for number in range(1,10): # For each number
                if not complete_check(matrix, number, row, col): # If number can't fit there
                    # print(str(int(empyt_squares[(row,col)])).replace(str(number),''))
                    empyt_squares[(row,col)] = int(str(empyt_squares[(row,col)]).replace(str(number),'')) # Remove it from list
                    # print(empyt_squares[(row,col)])
    # print('squares', empyt_squares, 'size', len(empyt_squares))
    completed = [] # Looked at empty spots
    tries = 0
    while len(completed) != len(locations): # While there are spots not looked at
        if tries > max_tries:
            return False
        for i in range(len(locations)): # For each spot
            row,col = locations[i] # Get row and col
            if check_one_number(empyt_squares[(row,col)]) and i not in completed: # If only 1 number is possible and hasn't been looked at yet
                completed.append(i) # Add it has been looked at
                number = empyt_squares[(row,col)] # Get number
                for j in range(len(locations)): # Remove from any other spots it was in
                    if j not in completed:
                        test_row, test_col = locations[j]
                        if str(number) in str(empyt_squares[(test_row, test_col)]) and check_remove(row, col, test_row, test_col):
                            empyt_squares[(test_row, test_col)] = int(str(empyt_squares[(test_row,test_col)]).replace(str(number),''))
        tries += 1
    return True
        
def hidden_singles(matrix):
    empyt_squares = {} # Empty Dictionary 
    locations = [] # List of locations
    for row in range(9): # For each row
        for col in range(9): # For each col
            if matrix[row][col] != 0.0: # If number is 0 already, skip
                continue
            empyt_squares[(row,col)] = str(complete_list) # this row,col is set to all numbers
            locations.append((row,col)) # row,col is saved
            for number in range(1,10): # For each number
                if not complete_check(matrix, number, row, col): # If number can't fit there
                    empyt_squares[(row,col)] = empyt_squares[(row,col)].replace(str(number),'') # Remove it from list
    # print('seen', empyt_squares)
    

    completed = [] # Looked at empty spots
    tries = 0
    while len(completed) != len(locations): # While there are spots not looked at
        if tries > max_tries:
            return False
        for i in range(len(locations)):
            row,col = locations[i]
            block_numbers = empyt_squares[(row,col)]
            if not check_one_number(int(block_numbers)):
                block_length = len(block_numbers)
                for j in range(block_length):
                    number = block_numbers[j]
                    not_found = True
                    for current_row in range(9):
                        if matrix[current_row][col] != 0.0 or current_row == row:
                            continue
                        current_numbers = empyt_squares[(current_row,col)]
                        for k in range(len(current_numbers)):
                            if number == current_numbers[k]:
                                not_found = False
                    if not_found:
                        empyt_squares[(row,col)] = str(number)
        tries += 1
    return True

                    

            



    # for i in range(len(locations)):
    #     row,col = locations[i]
    #     temp_row = []
    #     temp_col = []
    #     temp_square = []
    #     for j in range(1,len(locations)):
    #         test_row,test_col = locations[j]
    #         block_col = find_block(col)
    #         block_row = find_block(row)
    #         test_block_col = find_block(test_col)
    #         test_block_row = find_block(test_row)
    #         if row == test_row:
    #             temp_row.append((test_row, test_col))
    #         if col == test_col:
    #             temp_col.append((test_row, temp_col))
    #         if block_row == test_block_row and block_col == test_block_col:
    #             temp_square.append((temp_row,test_col))
        # print(temp_row,temp_col, temp_square)
        



    return False