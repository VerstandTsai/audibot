import discord
from discord.ext import commands
from yt_dlp import YoutubeDL
import os
import json
from shutil import rmtree

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'The bot has logged in as {bot.user}.')

'''
@bot.command()
async def help(ctx, botname):
    if botname != bot.user.name:
        return
    await ctx.send(
            '資訊與說明：\n'
            '!help               列出此訊息\n'
            '下載音訊、影片：\n'
            '!getaudio <網址>    下載 mp3 音訊\n'
            '!getvideo <網址>    下載 mp4 影片\n'
            '在語音頻道中播放音樂：\n'
            f'!join               讓{bot.user.name}加入您所在的語音頻道\n'
            f'!leave              讓{bot.user.name}離開語音頻道\n'
            '!play [編號/網址]   從清單中的第一項開始播放音樂\n'
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
    )
'''
@bot.command()
async def getaudio(ctx, url):
    ydl_opts = {
            'format': 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3'
            }],
            'outtmpl': 'audio.mp3'
    }
    with YoutubeDL(ydl_opts) as ydl:
        title = ydl.extract_info(url, download=False)['title']
        await ctx.send(f'正在下載 {title}')
        ydl.download([url])
    await ctx.send(file=discord.File('audio.mp3'))
    os.remove('audio.mp3')

@bot.command()
async def getvideo(ctx, url):
    download_folder = './downloads'
    if len(os.listdir(download_folder)) > 5:
        rmtree(download_folder)
        os.mkdir(download_folder)
    info = YoutubeDL({}).extract_info(url, download=False)
    ydl_opts = {
            'format': 'mp4',
            'outtmpl': f'./downloads/{info["id"]}.mp4'
    }
    with YoutubeDL(ydl_opts) as ydl:
        await ctx.send(f'正在下載 {info["title"]}')
        ydl.download([url])
    await ctx.send(
            '下載完成，點擊以下連結以下載\n'
            f'https://audibot-discord.herokuapp.com/downloads/{info["id"]}'
    )

@bot.command()
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send(f'請{ctx.author.name}先加入語音頻道')
        return
    await ctx.author.voice.channel.connect()
    os.mkdir(f'./playlists/{ctx.guild.id}')
    with open(f'./playlists/{ctx.guild.id}/playlist.json', 'w') as fp:
        json.dump([], fp)

@bot.command()
async def leave(ctx):
    vc = ctx.voice_client
    if vc.is_connected():
        await vc.disconnect()
        rmtree(f'./playlists/{ctx.guild.id}')

@bot.command()
async def play(ctx, arg=None):
    vc = ctx.voice_client
    if arg == None:
        pass
    elif arg.isdigit():
        playlist = []
        with open(f'./playlists/{ctx.guild.id}/playlist.json', 'r') as fp:
            playlist = json.load(fp)
        index = int(arg)-1
        title = playlist[index]['title']
        vc.play(discord.FFmpegPCMAudio(f'./playlists/{ctx.guild.id}/{playlist[index]["file"]}'))
        await ctx.send(f'現正播放 {title}')
    else:
        ydl_opts = {
                'format': 'bestaudio',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3'
                }],
                'outtmpl': 'audio.mp3'
        }
        title = ''
        with YoutubeDL(ydl_opts) as ydl:
            title = ydl.extract_info(arg, download=False)['title']
            await ctx.send(f'正在獲取 {title}')
            ydl.download([arg])
        vc.play(discord.FFmpegPCMAudio('audio.mp3'))
        os.remove('audio.mp3')
        await ctx.send(f'現正播放 {title}')

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
    liststr = ''
    for i in range(len(playlist)):
        liststr += f'{i+1}. '
        liststr += playlist[i]['title']
        liststr += '\n'
    await ctx.send(liststr)

@bot.command()
async def add(ctx, url):
    info = YoutubeDL({}).extract_info(url, download=False)
    ydl_opts = {
            'format': 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3'
            }],
            'outtmpl': f'./playlists/{ctx.guild.id}/{info["id"]}.mp3'
    }
    await ctx.send(f'正在加入 {info["title"]}')
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    playlist = []
    with open(f'./playlists/{ctx.guild.id}/playlist.json', 'r') as fp:
        playlist = json.load(fp)
    song = {}
    song['title'] = info['title']
    song['file'] = f'{info["id"]}.mp3'
    playlist.append(song)
    with open(f'./playlists/{ctx.guild.id}/playlist.json', 'w') as fp:
        json.dump(playlist, fp)
    await ctx.send(f'已將 {song["title"]} 加入清單中')

@bot.command()
async def pop(ctx, num):
    playlist = []
    with open(f'./playlists/{ctx.guild.id}/playlist.json', 'r') as fp:
        playlist = json.load(fp)
    index = int(num)-1
    title = playlist[index]['title']
    os.remove(f'./playlists/{ctx.guild.id}/{playlist[index]["file"]}')
    playlist.pop(index)
    with open(f'./playlists/{ctx.guild.id}/playlist.json', 'w') as fp:
        json.dump(playlist, fp)
    await ctx.send(f'已將 {title} 自清單中移除')

bot.run(os.getenv('TOKEN'))
