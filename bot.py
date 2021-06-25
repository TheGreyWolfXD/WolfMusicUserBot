# Examined dashezup's vcbot repo for make this turning out just for contacts and userbot!
#Wolf Bot @AboutGreyWolfXD

import os
from pytgcalls import GroupCall
import ffmpeg
from config import Config
from datetime import datetime
from pyrogram import filters, Client, idle
import requests
import wget
import aiohttp
from random import randint
import aiofiles

VOICE_CHATS = {}
DEFAULT_DOWNLOAD_DIR = 'downloads/wolfmusic/'

# deezer download web of william butcher bot
ARQ = "https://thearq.tech/"

api_id=Config.API_ID
api_hash=Config.API_HASH
session_name=Config.STRING_SESSION
app = Client(session_name, api_id, api_hash)

# userbot and contacts filter by dashezup's tgvc-userbot
self_or_contact_filter = filters.create(
    lambda
    _,
    __,
    message:
    (message.from_user and message.from_user.is_contact) or message.outgoing
)

# fetch url for deezer download
async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            try:
                data = await resp.json()
            except:
                data = await resp.text()
    return data

# get args for saavn download
def get_arg(message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])

# start message
@app.on_message(filters.command('start'))
async def start(client, message):
    await message.reply("Hey✌, How Are You\nI am Alive😉\n\nDeploy ME Now --  https://github.com/TheGreyWolfXD/WolfMusicUserBot",
                        disable_web_page_preview=True)

#free promotion hehehe
@app.on_message(filters.command('about') & self_or_contact_filter)
async def about(_, message):
    await message.reply('Join @AboutGreyWolfXD to know more 😉')


# ping
@app.on_message(filters.command('ping') & self_or_contact_filter)
async def ping(client, message):
    start = datetime.now()
    tauk = await message.reply('Pong!')
    end = datetime.now()
    m_s = (end - start).microseconds / 1000
    await tauk.edit(f'**Pong!**\n> `{m_s} ms`')

# jiosaavn song download
@app.on_message(filters.command('saavn') & self_or_contact_filter)
async def song(client, message):
    message.chat.id
    message.from_user["id"]
    args = get_arg(message) + " " + "song"
    if args.startswith(" "):
        await message.reply("What's the song you want 🧐")
        return ""
    pak = await message.reply('Downloading...')
    try:
#Ahh The Fuck is too long😒
        r = requests.get(f"https://jevcplayerbot-saavndl.herokuapp.com/result/?query={args}")
    except Exception as e:
        await pak.edit(str(e))
        return
    sname = r.json()[0]["song"]
    slink = r.json()[0]["media_url"]
    ssingers = r.json()[0]["singers"]
    file = wget.download(slink)
    ffile = file.replace("mp4", "m4a")
    os.rename(file, ffile)
    await pak.edit('Uploading...')
    await message.reply_audio(audio=ffile, title=sname, performer=ssingers)
    os.remove(ffile)
    await pak.delete()

async def download_song(url):
    song_name = f"{randint(6969, 6999)}.mp3"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(song_name, mode="wb")
                await f.write(await resp.read())
                await f.close()
    return song_name

# deezer download by william butcher bot
@app.on_message(filters.command("deezer") & self_or_contact_filter)
async def deezer(_, message):
    if len(message.command) < 2:
        await message.reply_text("What's the song you want 🧐")
        return
    text = message.text.split(None, 1)[1]
    query = text.replace(" ", "%20")
    hike = await message.reply_text("Searching...")
    try:
        r = await fetch(f"{ARQ}deezer?query={query}&count=1")
        title = r[0]["title"]
        url = r[0]["url"]
        artist = r[0]["artist"]
    except Exception as e:
        await hike.edit(str(e))
        return
    await hike.edit("Downloading...")
    song = await download_song(url)
    await hike.edit("Uploading...")
    await message.reply_audio(audio=song, title=title, performer=artist)
    os.remove(song)
    await hike.delete()

@app.on_message(filters.command('play') & self_or_contact_filter)
async def play_track(client, message):
    if not message.reply_to_message or not message.reply_to_message.audio:
        return
    input_filename = os.path.join(
        client.workdir, DEFAULT_DOWNLOAD_DIR,
        'input.raw',
    )
    audio = message.reply_to_message.audio
    audio_original = await message.reply_to_message.download()
    a = await message.reply('Downloading...')
    ffmpeg.input(audio_original).output(
        input_filename,
        format='s16le',
        acodec='pcm_s16le',
        ac=2, ar='48k',
    ).overwrite_output().run()
    os.remove(audio_original)
    if VOICE_CHATS and message.chat.id in VOICE_CHATS:
        text = f'▶️ Playing **{audio.title}** By @AboutGreyWolfXD...'
    else:
        try:
            group_call = GroupCall(client, input_filename)
            await group_call.start(message.chat.id)
        except RuntimeError:
            await message.reply('Group Call doesnt exist')
            return
        VOICE_CHATS[message.chat.id] = group_call
    await a.edit(f'▶️ Playing **{audio.title}** By @AboutGreyWolfXD...')


@app.on_message(filters.command('stopvc') & self_or_contact_filter)
async def stop_playing(_, message):
    group_call = VOICE_CHATS[message.chat.id]
    group_call.stop_playout()
    os.remove('downloads/wolfmusic/input.raw')
    await message.reply('Stopped Playing ❌')


@app.on_message(filters.command('joinvc') & self_or_contact_filter)
async def join_voice_chat(client, message):
    input_filename = os.path.join(
        client.workdir, DEFAULT_DOWNLOAD_DIR,
        'input.raw',
    )
    if message.chat.id in VOICE_CHATS:
        await message.reply('Already joined to Voice Chat 🛠')
        return
    chat_id = message.chat.id
    try:
        group_call = GroupCall(client, input_filename)
        await group_call.start(chat_id)
    except RuntimeError:
        await message.reply('lel error!')
        return
    VOICE_CHATS[chat_id] = group_call
    await message.reply('Joined the Voice Chat ✅')


@app.on_message(filters.command('leavevc') & self_or_contact_filter)
async def leave_voice_chat(client, message):
    chat_id = message.chat.id
    group_call = VOICE_CHATS[chat_id]
    await group_call.stop()
    VOICE_CHATS.pop(chat_id, None)
    await message.reply('Left Voice Chat ✅')

app.start()
print('/nStarted😊')
idle()
app.stop()
print('/nStopped😒')
