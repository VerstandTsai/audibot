import discord
from discord.ext import commands
from yt_dlp import YoutubeDL
import os
import json
from shutil import rmtree
from secrets import token_urlsafe

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'The bot has logged in as {bot.user}.')

@bot.command()
async def help(ctx, botname):
    if botname != bot.user.name:
        return
    '''
    await ctx.send(
            '資訊與說明：\n'
            '!help               列出此訊息\n'
            '下載音訊、影片：\n'
            '!getaudio <網址>    下載 mp3 音訊\n'
            '!getvideo <網址>    下載 mp4 影片\n'
            '在語音頻道中播放音樂：\n'
            f'!join               讓{bot.user.name}加入您所在的語音頻道\n'
            f'!leave              讓{bot.user.name}離開語音頻道\n'
            '!play [編號/網址]   播放清單中的音樂\n'
            '                    若有指定編號，則播放清單中該編號的音樂\n'
            '                    若有指定網址，則播放該網址中的音樂\n'
            '!pause              暫停目前播放的音樂\n'
            '!resume             繼續播放已暫停的音樂\n'
            '!stop               停止播放目前播放的音樂\n'
            '!prev               播放清單中的上一首音樂\n'
            '!next               播放清單中的下一首音樂\n'
            '!list               列出目前清單中的音樂\n'
            '!add <網址>         將網址中的音樂加入清單中\n'
            '!pop <編號>         將清單中該編號的音樂刪去'
    )'''

@bot.command()
async def getaudio(ctx, url):
    await ctx.send('正在下載音訊...')
    ydl_opts = {
            'format': 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3'
            }],
            'outtmpl': 'audio.mp3'
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
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
    ydl_opts = {
            'format': 'mp4',
            'outtmpl': f'{video_id}.mp4'
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    await ctx.send(
            f'下載完成，點擊以下連結以下載\n'
            f'https://audibot-discord.herokuapp.com/downloads/{video_id}'
    )
'''
@bot.command()
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send(f'請{ctx.author.name}先加入語音頻道')
        return
    await ctx.author.voice.channel.connect()
    os.mkdir(f'./playlists/{ctx.guild.id}')
    with open(f'./playlists/{ctx.guild.id}/filelist.json', 'w') as fp:
        pass

@bot.command()
async def leave(ctx):
    vc = ctx.voice_client
    if vc.is_connected():
        await vc.disconnect()
        rmtree(f'./playlists/{ctx.guild.id}')

@bot.command()
async def play(ctx, arg=None):
    pass

@bot.command()
async def pause(ctx):
    pass

@bot.command()
async def resume(ctx):
    pass

@bot.command()
async def stop(ctx):
    pass

@bot.command()
async def prev(ctx):
    pass

@bot.command()
async def next(ctx):
    pass

@bot.command()
async def list(ctx):
    playlist = []
    with open(f'./playlists/{ctx.guild.id}/playlist.json', 'r') as fp:
        playlist = json.load(fp)

@bot.command()
async def add(ctx, url):
    pass

@bot.command()
async def pop(ctx, num):
    pass
'''
bot.run(os.getenv('TOKEN'))
