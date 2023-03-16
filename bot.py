# Importing necessary files
import os
import discord
from dotenv import load_dotenv
import logging.handlers

# .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD_ID')

# Set up logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
logging.getLogger('discord.http').setLevel(logging.INFO)

handler = logging.handlers.RotatingFileHandler(
    filename='discord.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,  # 32 MiB
    backupCount=5,  # Rotate through 5 files
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Intents are like permissions; groups of events
intents = discord.Intents.default() # use the default set of intents
intents.message_content = True # allow the message_content events into our app

# load a new discord client with the intents we specified above
client = discord.Client(intents=intents)

# when the on_ready event is triggered,
@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'BOT({client.user}) Successfully Connected To Guild: {guild.name} (id: {guild.id})'
    )

# when the on_message event is triggered,
@client.event
async def on_message(message):
    if message.author == client.user: # stop the bot from messaging itself
        return

    if message.content.startswith('$hello'): # basic $hello command
        await message.channel.send('Hello!') # returns "Hello!"

client.run(TOKEN, log_handler=None) # run the discord client/bot using our client token (on dev portal)