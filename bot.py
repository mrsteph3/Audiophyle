import os

import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
from dotenv import load_dotenv

'''
Audiophyle: A Discord bot intended to retrieve information 
of songs such as artist, title, lyrics, album name, and release date.

Strictly made with the intent for educational and non-commercial purposes only.

Author: Matthew Stephenson
    GitHub: /mrsteph3
    LinkedIn: /in/matthew-r-stephenson
'''

# Pull discord bot token from local environment variable.
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GENIUS_TOKEN = os.getenv('GENIUS_TOKEN')

# Initialize bot instance with specified command prefix.
bot = commands.Bot(command_prefix='>>')


# Bot 'Commands' and 'Events'

# This is a console output to signify that the bot 
# is running and ready to process events/commands.
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# This is currently an echo command where the bot 
# will respond when called using >>s [arg0, arg1, ...]
@bot.command(name='s', help='Search for information on a song with a query {$s [query]}')
async def s(ctx, *args):

    # Get the search term from the command message
    search_term = ' '.join(args)

    # Send some messages with information
    await ctx.send('Finding the lyrics for: \"' + search_term + '\"')
    await ctx.send('Please wait...')

    # Setup the API Requests
    URL_API = 'https://api.genius.com'
    URL_SEARCH = URL_API + '/search'
    bearer = f'Bearer {GENIUS_TOKEN}'
    headers = {'Authorization': bearer}
    params = {'q': search_term}

    # Do the request
    response = requests.get(URL_SEARCH, params=params, headers=headers)

    # Parse
    json = response.json()
    SONG_TITLE = json['response']['hits'][0]['result']['full_title']
    API_PATH = json['response']['hits'][0]['result']['api_path']
    URL_SONG = URL_API + API_PATH

    # Another request
    response = requests.get(URL_SONG, headers=headers)

    # Parse
    songJson = response.json()
    path = songJson['response']['song']['path']
    URL_PAGE = 'https://genius.com' + path
    page = requests.get(URL_PAGE)

    # Scrape the lyrics
    html = BeautifulSoup(page.text, 'html.parser')
    [h.extract() for h in html('script')]
    lyrics = html.find('div', class_='lyrics').get_text()

    # Send a message with the song title
    await ctx.send(SONG_TITLE)

    # Some formatting magic here
    lyricsList = lyrics.split('\n\n')
    while '' in lyricsList:
        lyricsList.remove('')
    for section in lyricsList:
        if section != '':
            abridged = '```' + section + '```'
            # Send each song section in its own container (Markdown)
            await ctx.send(abridged)

bot.run(DISCORD_TOKEN)
