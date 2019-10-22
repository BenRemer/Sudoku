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
size = 9 # Size of every block and number of blocks

async def print_matrix(context, matrix, given): # print board to discord
    message = sudoku.print_board_bot(matrix, given)
    firstpart, secondpart = message[:len(message)//2], message[len(message)//2:]
    split_message = message.split('STRING_SPLIT')
    for split in split_message:
        await context.send(split)

@bot.event # On start
async def on_ready():
    print("Connected")
    print("---------")
    
    
    

@bot.command(name='play') # For command !play
async def start_game(context, difficulty = None):
    max_remove = 0
    if not difficulty: # If there was no difficulty given
        await context.send('Incorrect arguments: Type !play \'difficulty\'\nExample: !play easy')
        return
    if difficulty.lower() == 'easy' or difficulty == 'Easy': # If easy
        await context.send('Easy Game:')
        max_remove = 35
    elif difficulty.lower() == 'medium' or difficulty == 'Medium': # If medium
        await context.send('Medium Game:')
        max_remove = 48
    elif difficulty.lower() == 'hard' or difficulty == 'Hard': # If hard
        await context.send('Hard Game:')
        max_remove = 56
    else:
        await context.send('Incorrect arguments: Type !play \'difficulty\'\nExample: !play easy') # If something else there was an error
        return
        
    good = False
    while(not good): # While there is not a good board
        matrix = np.zeros((size, size)) # matrix[row][col]
        good, matrix = sudoku.create_board(matrix)
    matrix = sudoku.blank_board(matrix, max_remove) # Set board

    np.save('boards/'+str(context.author.id)+'.npy', matrix) # Save board to file
    given = {}
    for row in range(9):
        for col in range(9):
            if matrix[row][col] != 0.0:
                given[(row,col)] = matrix[row][col]
    np.save('boards/'+str(context.author.id)+'given.npy', given) # Save given spots to file

    await print_matrix(context, matrix, given)

@bot.command(name='put') # For command !put
async def put(context, *, location = None):
    try: # Try to load matrix and starting matrix
        matrix = np.load('boards/'+str(context.author.id)+'.npy')
        given = np.load('boards/'+str(context.author.id)+'given.npy').item()
    except: # If they don't exist error and return
        await context.send('Must start a game first: Type !play \'difficulty\'\nExample: !play easy')
        return
    if not location: # If they did not put a location error and return
        await context.send('Must put a location! Type !put (X,Y,#)\nExample: !put (A,J,1)')
        return

    location = location.replace('(', '').replace(')','').replace(',','').replace(' ', '').upper() # Remove all characters but row,col,number
    if len(location) != 3: # If not all three error
        await context.send('Location wrong! Type !put (X,Y,#)\nExample: !put (A,J,1)')
        return
    row = None
    col = None
    number = int(location[2])
    # Figure out which was the row and which was the column and if number is good
    if sudoku.letter_is_row(location[1]) and sudoku.letter_is_col(location[0]) and solve.check_one_number(number):
        row = sudoku.row_to_number.get(location[1])
        col = sudoku.col_to_number.get(location[0])
    elif sudoku.letter_is_row(location[0]) and sudoku.letter_is_col(location[1]) and solve.check_one_number(number):
        row = sudoku.row_to_number.get(location[0])
        col = sudoku.col_to_number.get(location[1])
    else: # Else error out
        await context.send('Error! Type !put (X,Y,#)\nExample: !put (A,J,1)')
        return

    if (row,col) in given: # If location given originally don't let them get rid of it
        await context.send('That location was given to begin with, don\'t change it')
    else: # Change matrix and save it
        matrix[row][col] = number
        np.save('boards/'+str(context.author.id)+'.npy', matrix)

    await print_matrix(context, matrix, given) # Print out board
        
@bot.command(name='remove') # remove a certain spot
async def remove(context, *, location = None):
    try: # Try to load matrix and starting matrix
        matrix = np.load('boards/'+str(context.author.id)+'.npy')
        given = np.load('boards/'+str(context.author.id)+'given.npy').item()
    except: # If they don't exist error and return
        await context.send('Must start a game first: Type !play \'difficulty\'\nExample: !play easy')
        return
    if not location: # If they did not put a location error and return
        await context.send('Must put a location! Type !remove (X,Y)\nExample: !remove (A,J)')
        return
    location = location.replace('(', '').replace(')','').replace(',','').replace(' ', '').upper() # Remove all characters but row,col,number
    if len(location) != 2: # If there aren't two points
        await context.send('Location wrong! Type !remove (X,Y)\nExample: !remove (A,J)')
        return
    row = None
    col = None
    if sudoku.letter_is_row(location[1]) and sudoku.letter_is_col(location[0]):
        row = sudoku.row_to_number.get(location[1])
        col = sudoku.col_to_number.get(location[0])
    elif sudoku.letter_is_row(location[0]) and sudoku.letter_is_col(location[1]):
        row = sudoku.row_to_number.get(location[0])
        col = sudoku.col_to_number.get(location[1])
    else: # Else error out
        await context.send('Error! Type !remove (X,Y)\nExample: !remove (A,J)')
        return

    if (row,col) in given: # If location given originally don't let them get rid of it
        await context.send('That location was given to begin with, don\'t change it')
    else: # Change matrix and save it
        matrix[row][col] = 0
        np.save('boards/'+str(context.author.id)+'.npy', matrix)
    await print_matrix(context, matrix, given) # Print out matrix

@bot.command(name='reset') # Command reset to reset board back to given
async def reset(context, arg=None):
    await context.send('Board reset to beginning') # Send message
    try: # Try to load matrix and given
        matrix = np.load('boards/'+str(context.author.id)+'.npy')
        given = np.load('boards/'+str(context.author.id)+'given.npy').item()
    except: # If error quit
        await context.send('Must start a game first: Type !play \'difficulty\'\nExample: !play easy')
        return
    # Go through matrix and reset all to given
    for row in range(9):
        for col in range(9):
            if (row,col) not in given:
                matrix[row][col] = 0
    np.save('boards/'+str(context.author.id)+'.npy', matrix) # Save locally
    await print_matrix(context, matrix, given) # Print out matrix

@bot.command(name='show')
async def show(context, arg=None):
    try:
        matrix = np.load('boards/'+str(context.author.id)+'.npy')
        given = np.load('boards/'+str(context.author.id)+'given.npy').item()
    except:
        await context.send('Must start a game first: Type !play \'difficulty\'\nExample: !play easy')
        return
    await print_matrix(context, matrix, given) # Print out matrix

@bot.command(name='commands')
async def display_commands(context, arg=None):
    message = ''
    message += 'Commands to use the Sudoku Bot:\n'
    message += '\'!play (difficulty)\' to play a game\n'
    message += '\'!put (X,Y,#)\' to put a number on an already created board\n'
    message += '\'!remove (X,Y)\' to remove a number on an already created board\n'
    message += '\'!show\' to show your existing board\n'
    message += '\'!reset\' to reset board back to the original state\n'
    await context.send(message)

bot.run(TOKEN)