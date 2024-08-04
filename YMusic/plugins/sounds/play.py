from YMusic import app
from YMusic.core import userbot
from YMusic.utils.ytDetails import searchYt, extract_video_id
from YMusic.utils.queue import QUEUE, add_to_queue
from YMusic.misc import SUDOERS

from pyrogram import filters

import asyncio
import random
import time

import config

PLAY_COMMAND = ["P", "PLAY"]

PREFIX = config.PREFIX

RPREFIX = config.RPREFIX


async def ytdl(format: str, link: str):
    stdout, stderr = await bash(
        f'yt-dlp --geo-bypass -g -f "{format}" {link}'
    )
    if stdout:
        return 1, stdout
    return 0, stderr


async def bash(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    err = stderr.decode().strip()
    out = stdout.decode().strip()
    return out, err


async def processReplyToMessage(message):
    msg = message.reply_to_message
    if msg.audio or msg.voice:
        m = await message.reply_text("Rukja...Tera Audio Download kar raha hu...")
        audio_original = await msg.download()
        input_filename = audio_original
        return input_filename, m
    return None


async def playWithLinks(link):
    if "&" in link:
        pass
    if "?" in link:
        pass

    return 0


@app.on_message((filters.command(PLAY_COMMAND, [PREFIX, RPREFIX])) & filters.group)
async def _aPlay(_, message):
    start_time = time.time()
    chat_id = message.chat.id
    if (message.reply_to_message) is not None:
        if message.reply_to_message.audio or message.reply_to_message.voice:
            input_filename, m = await processReplyToMessage(message)
            if input_filename is None:
                await message.reply_text(
                    "Audio pe reply kon karega mai? ya phir song link kon dalega mai? 🤔"
                )
                return
            await m.edit("Rukja...Tera Audio Play karne vala hu...")
            Status, Text = await userbot.playAudio(chat_id, input_filename)
            if Status == False:
                await m.edit(Text)
            else:
                if chat_id in QUEUE:
                    queue_num = add_to_queue(
                        chat_id,
                        message.reply_to_message.audio.title[:19],
                        message.reply_to_message.audio.duration,
                        message.reply_to_message.audio.file_id,
                        message.reply_to_message.link,
                    )
                    await m.edit(
                        f"# {queue_num}\n{message.reply_to_message.audio.title[:19]}\nTera gaana queue me daal diya hu"
                    )
                    return
                finish_time = time.time()
                total_time_taken = str(int(finish_time - start_time)) + "s"
                await m.edit(
                    f"Tera gaana play kar rha hu aaja vc\n\nSongName:- [{message.reply_to_message.audio.title[:19]}]({message.reply_to_message.link})\nDuration:- {message.reply_to_message.audio.duration}\nTime taken to play:- {total_time_taken}",
                    disable_web_page_preview=True,
                )
    elif (len(message.command)) < 2:
        await message.reply_text("Song name kon dalega mai? 🤔")
    else:
        m = await message.reply_text("Rukja...Tera gaana dhund raha hu...")
        query = message.text.split(maxsplit=1)[1]
        video_id = extract_video_id(query)
        try:
            if video_id is None:
                video_id = query
            title, duration, link = searchYt(video_id)
            if (title, duration, link) == (None, None, None):
                return await m.edit("No results found")
        except Exception as e:
            await message.reply_text(f"Error:- <code>{e}</code>")
            return

        await m.edit("Rukja...Tera gaana download kar raha hu...")
        format = "bestaudio"
        resp, songlink = await ytdl(format, link)
        if resp == 0:
            await m.edit(f"❌ yt-dl issues detected\n\n» `{songlink}`")
        else:
            if chat_id in QUEUE:
                queue_num = add_to_queue(chat_id, title[:19], duration, songlink, link)
                await m.edit(
                    f"# {queue_num}\n{title[:19]}\nTera gaana queue me daal diya hu"
                )
                return
            # await asyncio.sleep(1)
            Status, Text = await userbot.playAudio(chat_id, songlink)
            if Status == False:
                await m.edit(Text)
            if duration is None:
                duration = "Playing From LiveStream"
            add_to_queue(chat_id, title[:19], duration, songlink, link)
            finish_time = time.time()
            total_time_taken = str(int(finish_time - start_time)) + "s"
            await m.edit(
                f"Tera gaana play kar rha hu aaja vc\n\nSongName:- [{title[:19]}]({link})\nDuration:- {duration}\nTime taken to play:- {total_time_taken}",
                disable_web_page_preview=True,
            )


@app.on_message((filters.command(PLAY_COMMAND, [PREFIX, RPREFIX])) & SUDOERS)
async def _raPlay(_, message):
    start_time = time.time()
    if (message.reply_to_message) is not None:
        await message.reply_text("Currently this is not supported")
    elif (len(message.command)) < 3:
        await message.reply_text("You Forgot To Pass An Argument")
    else:
        m = await message.reply_text("Searching Your Query...")
        query = message.text.split(" ", 2)[2]
        msg_id = message.text.split(" ", 2)[1]
        title, duration, link = searchYt(query)
        await m.edit("Downloading...")
        format = "bestaudio"
        resp, songlink = await ytdl(format, link)
        if resp == 0:
            await m.edit(f"❌ yt-dl issues detected\n\n» `{songlink}`")
        else:
            Status, Text = await userbot.playAudio(msg_id, songlink)
            if Status == False:
                await m.edit(Text)
            if duration is None:
                duration = "Playing From LiveStream"
            finish_time = time.time()
            total_time_taken = str(int(finish_time - start_time)) + "s"
            await m.edit(
                f"Tera gaana play kar rha hu aaja vc\n\nSongName:- [{title[:19]}]({link})\nDuration:- {duration}\nTime taken to play:- {total_time_taken}",
                disable_web_page_preview=True,
            )
