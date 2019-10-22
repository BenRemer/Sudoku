# import discord
# import config
# from discord.ext import commands
import numpy as np
import random
import solve
import custom_emojis

size = 9 # Size of every block and number of blocks
max_tries = 100 # Maximum number of board tries
custom_number_switcher = custom_emojis.custom_number_switcher


col_switcher = { # Switch statement to add letter boarder for columns
    0 : ':regional_indicator_a:',
    1 : ':regional_indicator_b:',
    2 : ':regional_indicator_c:',
    3 : ':regional_indicator_d:',
    4 : ':regional_indicator_e:',
    5 : ':regional_indicator_f:',
    6 : ':regional_indicator_g:',
    7 : ':regional_indicator_h:',
    8 : ':regional_indicator_i:'
}

row_switcher = { # Switch statement to add letter boarder for rows
    0 : ':regional_indicator_j:',
    1 : ':regional_indicator_k:',
    2 : ':regional_indicator_l:',
    3 : ':regional_indicator_m:',
    4 : ':regional_indicator_n:',
    5 : ':regional_indicator_o:',
    6 : ':regional_indicator_p:',
    7 : ':regional_indicator_q:',
    8 : ':regional_indicator_r:'
}

number_switcher = {
    0 : ':heavy_multiplication_x:',
    1 : ':one:',
    2 : ':two:',
    3 : ':three:',
    4 : ':four:',
    5 : ':five:',
    6 : ':six:',
    7 : ':seven:',
    8 : ':eight:',
    9 : ':nine:'
}

cmd_col_switcher = { # Switch statement to add letter boarder for columns
    0 : 'A',
    1 : 'B',
    2 : 'C',
    3 : 'D',
    4 : 'E',
    5 : 'F',
    6 : 'G',
    7 : 'H',
    8 : 'I'
}

cmd_row_switcher = { # Switch statement to add letter boarder for rows
    0 : 'J',
    1 : 'K',
    2 : 'L',
    3 : 'M',
    4 : 'N',
    5 : 'O',
    6 : 'P',
    7 : 'Q',
    8 : 'R'
}

def print_board_console(matrix): # Prints board and boarder
    print('\n')
    print('  ', end='')
    for i in range(size):
        print(' ', cmd_col_switcher.get(i), ' ', end='')
    print('')
    for row in range(size):
        if row % 3 == 0:
            print('  |--------------|--------------|-------------|')
        print(cmd_row_switcher.get(row), end='')
        for col in range(size):
            if col % 3 == 0:
                print(' |', end='')
                print(matrix[row][col], end='')
            else:
                print(' ', matrix[row][col], end='')
        print('|')
    print('  |--------------|--------------|-------------|')

def print_board_bot(matrix, given): # Prints board and boarder
    message = ''
    message += ':heavy_multiplication_x:   '
    for i in range(size):
        if i % 3 == 0 and i != 0:
            message += '    '
        message += '   '
        message +=  col_switcher.get(i)
        # message += ' '
    message += '\n'
    for row in range(size):
        if row % 3 == 0:
            message += '        |-------------------|-------------------|------------------|\n'
        else:
            message += '        |                              |                               |                             |\n'
        if row % 3 == 2:
            message += 'STRING_SPLIT'
        message += (row_switcher.get(row))
        for col in range(size):
            if col % 3 == 0:
                message += '  |   '
                # message += number_switcher.get(int(matrix[row][col]))
            else:
                message += '  '
                # message += number_switcher.get(int(matrix[row][col]))
            if (row,col) in given:  # if original number, print in red
                message += custom_number_switcher.get(int(matrix[row][col]))
            else:   # else put as blue
                message += number_switcher.get(int(matrix[row][col]))
            message += ' '
        message += '|\n'
    message += '        |-------------------|-------------------|------------------|'
    return message

def create_board(matrix): # Goes number by number and row by row to create board
    for number in range(1,10):
        for row in range(size):
            col = create_spot(number, row, matrix)
            if col == 'BAD_BOARD':
                return (False, matrix)
            matrix[row][col] = number
    return (True, matrix)
            
def create_spot(number, row, matrix): # Creates random column and checks if the number can be in there 
    time = 0
    fair_number = False
    while(not fair_number):
        if time > max_tries: # After max tries amount of time it gives up on the board
            return 'BAD_BOARD'
        time += 1
        fair_number = True
        col = random.randint(0,8)
        for x in range(size): # Checks rows for the col
            if matrix[x][col] == number:
                fair_number = False
                continue
        for y in range(col):
            if matrix[row][y] == number: # Checks col for rows
                fair_number = False
                continue

        if col > 5:
            add_col = 6
        elif col > 2:
            add_col = 3
        else:
            add_col = 0

        if row > 5:
            add_row = 6
        elif row > 2:
            add_row = 3
        else:
            add_row = 0

        if np.any(matrix[add_row:add_row+3, add_col:add_col+3] == number): # Checks 3x3 block
            fair_number = False
            continue
        if matrix[row][col] != 0.0: # Checks to make sure it's not another number
            fair_number = False
            continue
    return col

def blank_board(matrix, max_remove):
    print_board_console(matrix)
    local = matrix
    solvable = True
    blanksquaresleft = True
    number_removed = 0
    time = 0
    while solvable and number_removed < max_remove:
        # print(number_removed)
        if time > max_tries: # After max tries amout of time it gives up on the board
            return matrix
        matrix = local
        row = random.randint(0,8)
        col = random.randint(0,8)
        local[row][col] = 0
        number_removed += 1
        # print_board_console(local)
        solvable = (solve.naked_singels(local) or solve.hidden_singles(local))
        if not solvable:
            # print('row', row, 'col', col, "removed", number_removed)
            time += 1
            number_removed -= 1
            local[row][col] = matrix[row][col]
        # print(solvable)    
    # print_board_console(matrix)
    # print(number_removed)
    return matrix

def letter_is_col(letter):
    return {
        'A' : True,
        'B' : True,
        'C' : True,
        'D' : True,
        'E' : True,
        'F' : True,
        'G' : True,
        'H' : True,
        'I' : True
    }.get(letter, False)

def letter_is_row(letter):
    return {
        'J' : True,
        'K' : True,
        'L' : True,
        'M' : True,
        'N' : True,
        'O' : True,
        'P' : True,
        'Q' : True,
        'R' : True
    }.get(letter, False)

col_to_number = { # Switch statement to add letter boarder for columns
    'A' : 0,
    'B' : 1,
    'C' : 2,
    'D' : 3,
    'E' : 4,
    'F' : 5,
    'G' : 6,
    'H' : 7,
    'I' : 8
}

row_to_number = { # Switch statement to add letter boarder for rows
    'J' : 0,
    'K' : 1,
    'L' : 2,
    'M' : 3,
    'N' : 4,
    'O' : 5,
    'P' : 6,
    'Q' : 7,
    'R' : 8
}