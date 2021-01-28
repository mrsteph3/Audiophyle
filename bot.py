import os
import requests

from bs4 import BeautifulSoup
from discord.ext import commands
from web_server import keep_alive

'''
Audiophyle: A Discord bot intended to retrieve song lyrics.

Strictly made with the intent for educational and non-commercial purposes only.

Author: Matthew Stephenson
    GitHub: /mrsteph3
    LinkedIn: /in/matthew-r-stephenson
'''

# Pull discord bot token from local environment variable.
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GENIUS_TOKEN = os.getenv('GENIUS_TOKEN')

# Initialize bot instance with specified command prefix.
bot = commands.Bot(command_prefix='>>')

###############################
# Bot 'Commands' and 'Events' #
###############################

# This is a console output to signify that the bot 
# is running and ready to process events/commands.
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# This is a command that can be executed by a user.
@bot.command(name='lyrics', 
             help='Search for song lyrics\
              {>>lyrics [song name] [artist]}')
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
    
    # Parse the search JSON response for the exact song title.
    json = response.json()
    SONG_TITLE = json['response']['hits'][0]['result']['full_title']
    API_PATH = json['response']['hits'][0]['result']['api_path']
    URL_SONG = URL_API + API_PATH

    # Request the for the song data.
    response = requests.get(URL_SONG, headers=headers)

    # Parse the song JSON response for the URL of the song on Genius.
    songJson = response.json()
    path = songJson['response']['song']['path']
    URL_PAGE = 'https://genius.com' + path
    page = requests.get(URL_PAGE)

    # Scrape the song lyrics from the Genius URL using BeautifulSoup.
    html = BeautifulSoup(page.text, 'html.parser')
    for h in html('script'):
        h.extract()
    lyrics = html.find('div', class_='lyrics').get_text()

    # Send a message with the song title
    await ctx.send(SONG_TITLE)

    ##############################################################
    # NOTE: The Discord API limits messages to 2000 charaters    #
    # so we have to do some formatting and verse-splitting here. #
    ##############################################################

    # Split the lyrics into a list of sections.
    lyricsList = lyrics.split('\n\n')

    # Remove empty/whitespace lines
    while '' in lyricsList:
        lyricsList.remove('')

    # If there is a section with greater than 1000 characters,
    # we split it at the first newline character after index 900.
    for i in range(len(lyricsList)):
        if len(lyricsList[i]) > 1000:
            splitIndex = lyricsList[i].index('\n', 900)
            temp = lyricsList[i][splitIndex+1:]
            lyricsList.insert(i+1, temp)
            lyricsList[i] = lyricsList[i][:splitIndex+1]

    # Send the lyric sections 
    for section in lyricsList:
        if section != '':
            abridged = '```' + section + '```'
            # Send each song section in its own container
            await ctx.send(abridged)

# Keep the bot running.
keep_alive()

# Run the bot.
bot.run(DISCORD_TOKEN)
