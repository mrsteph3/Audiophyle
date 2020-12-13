import os
import random
import requests

import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$')

random.seed()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='test', help='Responds with a random number from 0 to 10 (inclusive).')
async def test(ctx):
    response = random.randint(0,10)
    await ctx.send(str(response))

@bot.command(name='s', help='Search for information on a song with a query {$s [query]}')
async def s(ctx, *args):
    argument = ' '.join(args)
    
    await ctx.send(argument)

bot.run(TOKEN)
