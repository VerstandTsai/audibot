import discord
import os
import subprocess
from shutil import rmtree
from secrets import token_urlsafe

client = discord.Client()

@client.event
async def on_ready():
    print(f'The bot has logged in as {client.user}.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!getaudio'):
        await message.channel.send('正在下載音訊...')
        url = message.content.split()[1]
        subprocess.run(f'yt-dlp --extract-audio --audio-format mp3 -o audio.mp3 {url}'.split())
        await message.channel.send(file=discord.File('audio.mp3'))
        os.remove('audio.mp3')

    if message.content.startswith('!getvideo'):
        download_folder = './downloads'
        if len(os.listdir(download_folder)) > 5:
            rmtree(download_folder)
            os.mkdir(download_folder)
        await message.channel.send('正在下載影片...')
        video_id = token_urlsafe(6)
        url = message.content.split()[1]
        subprocess.run(f'yt-dlp -f mp4 -o {download_folder}/{video_id}.mp4 {url}'.split())
        await message.channel.send(f'下載完成，點擊以下連結以下載')
        await message.channel.send(f'https://audibot-discord.herokuapp.com/downloads/{video_id}')

client.run(os.getenv('TOKEN'))
