import discord
from discord.ext import commands
import os
import subprocess
from shutil import rmtree
from secrets import token_urlsafe

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'The bot has logged in as {client.user}.')

@bot.command()
async def getaudio(ctx, url):
    await ctx.send('正在下載音訊...')
    subprocess.run(f'yt-dlp --extract-audio --audio-format mp3 -o audio.mp3 {url}'.split())
    await ctx.send(file=discord.File('audio.mp3'))
    os.remove('audio.mp3')

@bot.command()
async def getvideo(ctx, url):
    download_folder = './downloads'
    if len(os.listdir(download_folder)) > 5:
        rmtree(download_folder)
        os.mkdir(download_folder)
    await ctx.send('正在下載影片...')
    video_id = token_urlsafe(6)
    subprocess.run(f'yt-dlp -f mp4 -o {download_folder}/{video_id}.mp4 {url}'.split())
    await ctx.send(f'下載完成，點擊以下連結以下載')
    await ctx.send(f'https://audibot-discord.herokuapp.com/downloads/{video_id}')

bot.run(os.getenv('TOKEN'))
