import discord
from discord.ext import commands
import config
import sudoku
import numpy as np
import solve


TOKEN = config.TOKEN # Get token form config file
bot_prefix = ('!') # Prefix to use
bot = commands.Bot(command_prefix=bot_prefix) # Set bot
message_limit = 2000 # Limit for discord's messages

@bot.event
async def on_ready():
    print("Connected")
    print("---------")
    

@bot.command(name='play')
async def start_game(context, difficulty = None):
    max_remove = 0
    if not difficulty:
        await context.send('Incorrect arguments: Type !play \'difficulty\'\nExample: !play easy')
        return
    if difficulty == 'easy' or difficulty == 'Easy':
        await context.send('Easy Game:')
        max_remove = 35
    elif difficulty == 'medium' or difficulty == 'Medium':
        await context.send('Medium Game:')
        max_remove = 48
    elif difficulty == 'hard' or difficulty == 'Hard':
        await context.send('Hard Game:')
        max_remove = 56
    else:
        await context.send('Incorrect arguments: Type !play \'difficulty\'\nExample: !play easy')
        return
        
    good = False
    while(not good):
        matrix = np.zeros((size, size)) # matrix[row][col]
        good, matrix = sudoku.create_board(matrix)
    matrix = sudoku.blank_board(matrix, max_remove)

    message = sudoku.print_board_bot(matrix)
    firstpart, secondpart = message[:len(message)//2], message[len(message)//2:]
    split_message = message.split('STRING_SPLIT')
    for split in split_message:
        await context.send(split)
    np.save('boards/'+str(context.author.id)+'.npy', matrix)
    given = {}
    for row in range(9):
        for col in range(9):
            if matrix[row][col] != 0.0:
                given[(row,col)] = matrix[row][col]
    # save_given(given, str(context.author.id)+'given.npy')
    np.save('boards/'+str(context.author.id)+'given.npy', given)

@bot.command(name='put')
async def put(context, *, location = None):
    try:
        matrix = np.load('boards/'+str(context.author.id)+'.npy')
        given = np.load('boards/'+str(context.author.id)+'given.npy').item()
    except:
        await context.send('Must start a game first: Type !play \'difficulty\'\nExample: !play easy')
        return
    if not location:
        await context.send('Must put a location! Tpye !put (X,Y,#)\nExample: !put (A,J,1)')
        return

    location = location.replace('(', '').replace(')','').replace(',','').replace(' ', '').upper()
    if len(location) != 3:
        await context.send('Location wrong! Tpye !put (X,Y,#)\nExample: !put (A,J,1)')
        return
    row = None
    col = None
    number = int(location[2])
    if sudoku.letter_is_row(location[1]) and sudoku.letter_is_col(location[0]) and solve.check_one_number(number):
        row = sudoku.row_to_number.get(location[1])
        col = sudoku.col_to_number.get(location[0])
    elif sudoku.letter_is_row(location[0]) and sudoku.letter_is_col(location[1]) and solve.check_one_number(number):
        row = sudoku.row_to_number.get(location[0])
        col = sudoku.col_to_number.get(location[1])
    else:
        await context.send('Error! Tpye !put (X,Y,#)\nExample: !put (A,J,1)')
        return

    if (row,col) in given:
        await context.send('That location was given to begin with, don\'t change it')
    else:
        matrix[row][col] = number
        np.save('boards/'+str(context.author.id)+'.npy', matrix)

    message = sudoku.print_board_bot(matrix)
    firstpart, secondpart = message[:len(message)//2], message[len(message)//2:]
    split_message = message.split('STRING_SPLIT')
    for split in split_message:
        await context.send(split)
        
@bot.command(name='reset')
async def reset(context, arg=None):
    await context.send('Board reset to beginning')
    try:
        matrix = np.load('boards/'+str(context.author.id)+'.npy')
        given = np.load('boards/'+str(context.author.id)+'given.npy').item()
    except:
        await context.send('Must start a game first: Type !play \'difficulty\'\nExample: !play easy')
        return
    for row in range(9):
        for col in range(9):
            if (row,col) not in given:
                matrix[row][col] = 0
    np.save('boards/'+str(context.author.id)+'.npy', matrix)
    message = sudoku.print_board_bot(matrix)
    firstpart, secondpart = message[:len(message)//2], message[len(message)//2:]
    split_message = message.split('STRING_SPLIT')
    for split in split_message:
        await context.send(split)

@bot.command(name='show')
async def show(context, arg=None):
    try:
        matrix = np.load('boards/'+str(context.author.id)+'.npy')
    except:
        await context.send('Must start a game first: Type !play \'difficulty\'\nExample: !play easy')
        return
    message = sudoku.print_board_bot(matrix)
    firstpart, secondpart = message[:len(message)//2], message[len(message)//2:]
    split_message = message.split('STRING_SPLIT')
    for split in split_message:
        await context.send(split)

@bot.command(name='commands')
async def display_commands(context, arg=None):
    message = ''
    message += 'Commands to use the Sudoku Bot:\n'
    message += '\'!play (difficulty)\' to play a game\n'
    message += '\'!put (X,Y,#)\' to put a number on an already created board\n'
    message += '\'!show\' to show your existing board\n'
    message += '\'!reset\' to reset board back to the original state\n'
    await context.send(message)



bot.run(TOKEN)