import discord
import os
import subprocess

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

client.run(os.getenv('TOKEN'))
