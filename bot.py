import os

import discord
import requests
from discord.ext import commands
from dotenv import load_dotenv

'''
Audiophyle: A Discord bot intended to retrieve information of songs such as artist, title, album name, and release date.
Written by: Matthew Stephenson
GitHub: /mrsteph3
LinkedIn: /in/matthew-r-stephenson
'''

# Pull discord bot token from local environment variable.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Initialize bot with specified command prefix.
bot = commands.Bot(command_prefix='>>')


# Bot 'Commands' and 'Events'

# This is a console output to signify that the bot is running and ready to process events/commands.
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# This is currently an echo command where the bot will respond when called using >>s [arg0, arg1, ...]
@bot.command(name='s', help='Search for information on a song with a query {$s [query]}')
async def s(ctx, *args):
    argument = ' '.join(args)
    
    await ctx.send(argument)

bot.run(TOKEN)
