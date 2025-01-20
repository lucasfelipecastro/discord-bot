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
        user = ctx.author
        await ctx.reply(f'Hi, {user.display_name}!')
    

    @bot_instance.command()
    async def join(ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.reply('Enter in a voice channel.')


    @bot_instance.commands()
    async def leave(ctx):
        if ctx.voice_cliente:
            await ctx.voice_cliente.disconnect()
        else:
            await ctx.reply('The bot is not in a voice channel.')

    
    @bot_instance.command()
    async def play(ctx, url: str):
        if not ctx.voice_client:
            if ctx.author.voice:
                channel = ctx.author.voice.channel
                await channel.connect()
            else:
                await ctx.reply('You need to be in a voice channel first.')
                return 
        
        YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': True}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']

        voice_client = ctx.voice_client
        voice_client.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: print('done', e))

    
    @bot_instance.command()
    async def pause(ctx):
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await ctx.reply('Song paused.')
        else:
            await ctx.reply('Nothing is playing.')


    @bot_instance.command()
    async def resume(ctx):
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await ctx.reply('Song resumed.')
        else:
            await ctx.reply('Nothing is resumed.')
        
    @bot_instance.command()
    async def stop(ctx):
        voice_client = ctx.voice_client
        if voice_client and voice_client.is_playling():
            voice_client.stop()
            await ctx.reply('Song stopped.')
        else:
            await ctx.reply('Nothing is playing.')


def setup_events(bot_instance):

    @bot_instance.event
    async def on_ready():
        print(f'The bot "{bot_instance.user}" is ready.')