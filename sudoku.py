import discord
import config
from discord.ext import commands
import numpy as np
import random


TOKEN = config.TOKEN # Get token form config file
bot_prefix = ('!') # Prefix to use
bot = commands.Bot(command_prefix=bot_prefix) # Set bot

message_limit = 2000 # Limit for discord's messages
output_size = 30 # Will be a square, so used for both X and Y
size = 9 # Size of every block and number of blocks
max_tries = 100 # Maximun number of board tries

# matrix = [[0 for x in range(size)]for y in range(size)] # Seen as matrix[col][row]

col_switcher = { # Switch statement to add letter boarder for columns
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

row_switcher = { # Switch statement to add letter boarder for rows
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
    print('  ', end='')
    for i in range(size):
        print(' ', col_switcher.get(i), ' ', end='')
    print('\n')
    for row in range(size):
        if row % 3 == 0:
            print('  |--------------|--------------|-------------|')
        print(row_switcher.get(row), end='')
        for col in range(size):
            if col % 3 == 0:
                print(' |', end='')
                print(matrix[row][col], end='')
            else:
                print(' ', matrix[row][col], end='')
        print('|')
    print('  |--------------|--------------|-------------|')

def create_board(matrix): # Goes number by number and row by row to create board
    for number in range(1,10):
        for row in range(size):
            col = create_spot(number, row, matrix)
            if col == 'BAD_BOARD':
                return False
            matrix[row][col] = number
    return 'good'
            
def create_spot(number, row, matrix): # Creates random column and checks if the number can be in there 
    time = 0
    fair_number = False
    while(not fair_number):
        if time > max_tries: # After max tries amout of time it gives up on the board
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

@bot.event
async def on_ready():
    print("Connected")
    print("---------")
    good = False
    while(not good):
        matrix = np.zeros((size, size)) # matrix[col][row]
        good = create_board(matrix)
    print_board_console(matrix)


@bot.command(name='play')
async def draw_image(context, arg):
    create_board()
    msg = 'Function being implemeted!'
    await context.send(msg + '\n' + arg)


bot.run(TOKEN)