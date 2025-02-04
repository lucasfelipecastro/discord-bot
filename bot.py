import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import yt_dlp as youtube_dl
from discord import FFmpegPCMAudio
from discord.ext.commands import Bot
import asyncio
from shutil import which

# Load environment variables
load_dotenv()

def get_bot_token():
    # Get the Bot Token
    return os.getenv("DISCORD_TOKEN")

def create_bot():
    # Create the bot
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    bot_instance = commands.Bot(command_prefix='.', intents=intents)
    return bot_instance

def add_commands(bot_instance):
    # Define the bot commands
    
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
            try:
                await channel.connect()
            except Exception as e:
                await ctx.reply(f"Could not join the voice channel. Error: {e}")
        else:
            await ctx.reply('Please join a voice channel first.')

    @bot_instance.command()
    async def leave(ctx):
        # Make the bot leave the voice channel
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        else:
            await ctx.reply('The bot is not in a voice channel.')

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': True}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }

    @bot_instance.command()
    async def play(ctx, url: str):
        # Play a song from a URL
        if not ctx.author.voice:
            await ctx.reply("You need to join a voice channel first.")
            return

        if ctx.voice_client and ctx.voice_client.channel != ctx.author.voice.channel:
            await ctx.reply("The bot is already in another voice channel.")
            return

        if not ctx.voice_client:
            try:
                channel = ctx.author.voice.channel
                await channel.connect()
            except discord.errors.ClientException as e:
                await ctx.reply(f"Error to connect: {e}")
                return

        try:
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
            if info and info.get('formats') and len(info['formats']) > 0:
                audio_url = info['formats'][0]['url']
            else:
                await ctx.reply("Could not retrieve audio format from the provided URL.")
                return
        except youtube_dl.DownloadError as e:
            await ctx.reply(f"Failed to retrieve the audio. The link might be invalid.\nError: {e}")
            return
        except Exception as e:
            await ctx.reply(f"An unexpected error occurred: {e}")
            return

        voice_client = ctx.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()

        FFMPEG_PATH = which("ffmpeg")
        if not FFMPEG_PATH:
            raise RuntimeError("FFmpeg not found. Please install it and add to PATH.")
        
        voice_client.play(
            FFmpegPCMAudio(source=audio_url, executable=FFMPEG_PATH, **FFMPEG_OPTIONS), # type: ignore
            after=lambda e: print(f"Error playing audio: {e}" if e else "Playback finished.")
        )
        if not audio_url:
            await ctx.reply("Could not retrieve a valid audio URL.")
            return
        await ctx.reply(f"Now playing: {url}")

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
        print(f'The bot "{bot_instance.user}" is ready and connected to {len(bot_instance.guilds)} servers!')

bot = create_bot()
add_commands(bot)
setup_events(bot)

TOKEN = get_bot_token()

if not TOKEN:
    raise ValueError("DISCORD_TOKEN not found.")

bot.run(TOKEN)
