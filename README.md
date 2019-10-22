# Discord Sudoku bot
This is a discord bot that allows users to play sudoku on your server or in the bots private chat.

## Install Guide
### Prereqs 
 - Install the discord.py API by following the instructions here: ```https://github.com/Rapptz/discord.py```.
 - Install numpy using the following instructions: ```https://scipy.org/install.html```.

### Creating the bot
- Install Sudoku by first cloaning the GitHub repository: ```git clone https://github.com/BenRemer/sudoku.git```.
- Go to ```https://discordapp.com/developers/applications/``` and create a new application.
- One the bot is created copy the Token found in the Bot tab and by clicking ```Click to Reveal Token```.
	- Create a new file called config.py and add the token as ```TOKEN = "xxxx"```.
- Go the server settings tab in discord.
	- Click on the Emoji tab and upload the numbers in [`red_numbers`](red_numbers).
	- Once uploaded, for each number find the custom ID of the emoji.
		- This is done by typing ```\:emojiName:``` to get the ID.
		- For each number save that in the [`custom_emojis.py`](custom_emojis.py) file for the corresponding number.

### Running the bot
- Open up a terminal and move into the main folder.
- To start the bot run: ```./bot.py``` if on Unix.
	- If on windows run ```python3 bot.py```.
- Type ```!commands``` into chat to see the bots commands.