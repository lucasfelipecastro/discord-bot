import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
permissions = discord.Intents.default()
permissions.message_content = True
permissions.members = True
bot = commands.Bot(command_prefix='.', intents=permissions)

@bot.command()
async def hi(ctx:commands.Context):
    user = ctx.author
    await ctx.reply(f"Hi, {user.display_name}")

@bot.event
async def on_ready():
    print('Ready.')

bot.run(TOKEN)