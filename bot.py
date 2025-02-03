import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import yt_dlp as youtube_dl
from discord import FFmpegPCMAudio
from discord.ext.commands import Bot
import asyncio

# Loading environment variables
load_dotenv()

def get_bot_token():
    # Getting the Bot Token
    return os.getenv("DISCORD_TOKEN")

def create_bot():
    # Creating the bot
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot_instance = commands.Bot(command_prefix='.', intents=intents)
    return bot_instance

def add_commands(bot_instance):
    # Defining the bot commands
    
    @bot_instance.command()
    async def greeting(ctx: commands.Context):
        # Greet the user
        user = ctx.author
        await ctx.reply(f'Hi, {user.display_name}!')
    

    @bot_instance.command()
    async def join(ctx):
        # Make the bot join the user's voice channel
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.reply('Please enter a voice channel first.')


    @bot_instance.command()
    async def leave(ctx):
        # Make the bot leave the voice channel
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        else:
            await ctx.reply('The bot is not in a voice channel.')

    
    @bot_instance.command()
    async def play(ctx, url: str):
        # Play a song from a URL
        if not ctx.voice_client:
            if ctx.author.voice:
                channel = ctx.author.voice.channel
                await channel.connect()
            else:
                await ctx.reply("You need to join a voice channel first.")
                return

        YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': True}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
            print(f"URL: {URL}")  # Print URL for debugging

        voice_client = ctx.voice_client
        if voice_client.is_playing():
            voice_client.stop()  # Stop any currently playing music
        voice_client.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: print(f"Error playing audio: {e}"))

        await ctx.reply(f"Now playing: {url}")

        try:
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
                URL = info['formats'][0]['url']
        except Exception as e:
            await ctx.reply(f"Error: {e}")
    

        if ctx.voice_client and ctx.voice_client.channel != ctx.author.voice.channel:
            await ctx.reply("The bot is already in another voice channel.")
            return

    
    @bot_instance.command()
    async def pause(ctx):
        # Pause the currently playing song
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await ctx.reply('Song paused.')
        else:
            await ctx.reply('Nothing is playing.')

    @bot_instance.command()
    async def resume(ctx):
        # Resume the currently paused song
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await ctx.reply('Song resumed.')
        else:
            await ctx.reply('Nothing is paused.')

    @bot_instance.command()
    async def stop(ctx):
        # Stop the currently playing song
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await ctx.reply('Song stopped.')
        else:
            await ctx.reply('Nothing is playing.')


def setup_events(bot_instance):

    @bot_instance.event
    async def on_ready():
        # Bot is ready
        print(f'The bot "{bot_instance.user}" is ready.')

bot = create_bot()
add_commands(bot)
setup_events(bot)

TOKEN = get_bot_token()
bot.run(TOKEN)
