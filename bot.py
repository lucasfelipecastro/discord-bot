import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
permissions = discord.Intents.default()
bot = commands.Bot(command_prefix='.', intents=permissions)
bot.run(TOKEN)