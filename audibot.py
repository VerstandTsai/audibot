import discord
from discord.ext import commands
from yt_dlp import YoutubeDL
import requests
import os
from shutil import rmtree
import asyncio

bot = commands.Bot(command_prefix='!', help_command=None)
queues = {}
website = 'https://audibot-discord.herokuapp.com'

@bot.event
async def on_ready():
    print(f'The bot has logged in as {bot.user}.')
    while True:
        await asyncio.sleep(10*60)
        requests.get(website)

@bot.command()
async def help(ctx, botname):
    if botname != bot.user.name:
        return
    await ctx.send(
        '```'
        '資訊與說明：\n'
        f'!help {bot.user.name}              列出此訊息\n'
        '下載音訊、影片：\n'
        '!getaudio <網址/關鍵字>     下載 mp3 音訊\n'
        '!getvideo <網址/關鍵字>     下載 mp4 影片\n'
        '在語音頻道中播放音樂：\n'
        f'!join                      讓{bot.user.name}加入您所在的語音頻道\n'
        f'!leave                     讓{bot.user.name}離開語音頻道\n'
        '!play <網址/關鍵字>         播放指定的音樂\n'
        '!pause                     暫停播放音樂\n'
        '!resume                    繼續播放音樂\n'
        '!stop                      停止播放音樂並清空播放清單\n'
        '!skip                      跳過並播放清單中的下一首音樂\n'
        '!queue                     列出目前清單中的音樂\n'
        '!pop <編號>                將清單中該編號的音樂刪去'
        '```'
    )

@bot.command()
async def getaudio(ctx, *, arg):
    is_url = False
    info = {}
    try:
        requests.get(arg)
    except:
        is_url = False
        info = YoutubeDL({}).extract_info(f'ytsearch:{arg}', download=False)['entries'][0]
    else:
        is_url = True
        info = YoutubeDL({}).extract_info(arg, download=False)
    ydl_opts = {
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3'
        }],
        'outtmpl': 'audio.mp3'
    }
    with YoutubeDL(ydl_opts) as ydl:
        await ctx.send(f'正在下載 {info["title"]}')
        ydl.download([arg if is_url else f'ytsearch:{arg}'])
    await ctx.send(file=discord.File('audio.mp3'))
    os.remove('audio.mp3')

@bot.command()
async def getvideo(ctx, *, arg):
    download_folder = './downloads'
    if len(os.listdir(download_folder)) > 5:
        rmtree(download_folder)
        os.mkdir(download_folder)
    is_url = False
    info = {}
    try:
        requests.get(arg)
    except:
        is_url = False
        info = YoutubeDL({}).extract_info(f'ytsearch:{arg}', download=False)['entries'][0]
    else:
        is_url = True
        info = YoutubeDL({}).extract_info(arg, download=False)
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': f'./downloads/{info["id"]}.mp4'
    }
    with YoutubeDL(ydl_opts) as ydl:
        await ctx.send(f'正在下載 {info["title"]}')
        ydl.download([arg if is_url else f'ytsearch:{arg}'])
    await ctx.send(
        '下載完成，點擊以下連結以下載\n'
        f'{website}/downloads/{info["id"]}'
    )

@bot.command()
async def join(ctx):
    if not ctx.author.voice:
        await ctx.send(f'請{ctx.author.name}先加入語音頻道')
        return
    await ctx.author.voice.channel.connect()
    guild_id = str(ctx.guild.id)
    queues[guild_id] = []
    os.mkdir(f'./queues/{guild_id}')

@bot.command()
async def leave(ctx):
    vc = ctx.voice_client
    if vc.is_connected():
        await vc.disconnect()
        guild_id = str(ctx.guild.id)
        queues.pop(guild_id)
        rmtree(f'./queues/{guild_id}')

@bot.command()
async def play(ctx, *, arg):
    vc = ctx.voice_client
    if vc == None:
        await ctx.send(f'請先用!join讓{bot.user.name}加入語音頻道')
        return

    is_url = False
    info = {}
    try:
        requests.get(arg)
    except:
        is_url = False
        info = YoutubeDL({}).extract_info(f'ytsearch:{arg}', download=False)['entries'][0]
    else:
        is_url = True
        info = YoutubeDL({}).extract_info(arg, download=False)

    guild_id = str(ctx.guild.id)
    filepath = f'./queues/{guild_id}/{info["id"]}.webm'
    async with ctx.typing():
        ydl_opts = {
            'format': 'bestaudio',
            'outtmpl': filepath
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([arg if is_url else f'ytsearch:{arg}'])
    if not vc.is_playing():
        vc.play(discord.FFmpegPCMAudio(filepath), after=lambda e: play_next(ctx))
        await ctx.send(f'現正播放 {info["title"]}')
        return

    song = {}
    song['title'] = info['title']
    song['filename'] = f'{info["id"]}.webm'
    queues[guild_id].append(song)
    await ctx.send(f'已將 {info["title"]} 加入清單中')

def play_next(ctx):
    vc = ctx.voice_client
    guild_id = str(ctx.guild.id)
    if len(queues[guild_id]) == 0:
        return
    title = queues[guild_id][0]['title']
    filename = queues[guild_id][0]['filename']
    filepath = f'./queues/{guild_id}/{filename}'
    vc.play(discord.FFmpegPCMAudio(filepath), after=lambda e: play_next(ctx))
    queues[guild_id].pop(0)

@bot.command()
async def pause(ctx):
    vc = ctx.voice_client
    if vc == None:
        await ctx.send(f'請先用!join讓{bot.user.name}加入語音頻道')
        return
    if vc.is_playing():
        vc.pause()
        await ctx.send('音樂已暫停')

@bot.command()
async def resume(ctx):
    vc = ctx.voice_client
    if vc == None:
        await ctx.send(f'請先用!join讓{bot.user.name}加入語音頻道')
        return
    if vc.is_paused():
        vc.resume()

@bot.command()
async def stop(ctx):
    vc = ctx.voice_client
    if vc == None:
        await ctx.send(f'請先用!join讓{bot.user.name}加入語音頻道')
        return
    if vc.is_playing():
        guild_id = str(ctx.guild.id)
        queues[guild_id] = []
        rmtree(f'./queues/{guild_id}')
        os.mkdir(f'./queues/{guild_id}')
        vc.stop()
        await ctx.send('已停止播放音樂')

@bot.command()
async def skip(ctx):
    vc = ctx.voice_client
    if vc == None:
        await ctx.send(f'請先用!join讓{bot.user.name}加入語音頻道')
        return
    if vc.is_playing():
        vc.stop()

@bot.command()
async def queue(ctx):
    if ctx.voice_client == None:
        await ctx.send(f'請先用!join讓{bot.user.name}加入語音頻道')
        return
    queue = queues[str(ctx.guild.id)]
    if len(queue) == 0:
        await ctx.send('播放清單是空的')
        return
    liststr = ''
    for i in range(len(queue)):
        liststr += f'{i+1}. '
        liststr += queue[i]['title']
        liststr += '\n'
    await ctx.send(liststr)

@bot.command()
async def pop(ctx, num):
    if ctx.voice_client == None:
        await ctx.send(f'請先用!join讓{bot.user.name}加入語音頻道')
        return
    guild_id = str(ctx.guild.id)
    index = int(num)-1
    title = queues[guild_id][index]['title']
    os.remove(f'./queues/{guild_id}/{queues[guild_id][index]["filename"]}')
    queues[guild_id].pop(index)
    await ctx.send(f'已將 {title} 自清單中移除')

bot.run(os.getenv('TOKEN'))
