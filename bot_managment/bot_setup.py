import discord
from discord.ext import commands

intents = discord.Intents.default() # Allows a default set of options.
intents.message_content = True # Makes so the bot can read messages.
intents.guilds = True # Makes so the bot can see and interact with the guilds it's in.

# This initializes your bots ability to execute commands. Command prefix decides the prefix for every command. Intents decided what permissions the bot will have when executing a command.
bot = commands.Bot(command_prefix='!', intents=intents)