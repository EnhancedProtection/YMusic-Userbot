from YMusic import app
from YMusic.core import userbot
from YMusic.utils import ytDetails
from YMusic.utils.queue import QUEUE, add_to_queue
from YMusic.misc import SUDOERS

from pyrogram import filters

import asyncio
import random
import time

import config

VIDEO_PLAY = ["VPLAY"]

PREFIX = config.PREFIX

RPREFIX = config.RPREFIX


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "best[height<=?720][width<=?1280]",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


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


async def playWithLinks(link):
    if "&" in link:
        pass
    if "?" in link:
        pass

    return 0


@app.on_message((filters.command(VIDEO_PLAY, PREFIX) | filters.command(VIDEO_PLAY, RPREFIX)))
async def _vPlay(_, message):
    start_time = time.time()
    chat_id = message.chat.id
    if (message.reply_to_message) is not None:
        await message.reply_text("Currently this is not supported")
    elif (len(message.command)) < 2:
        await message.reply_text("Link kon daalega mai? 🤔")
    else:
        m = await message.reply_text("Rukja...Tera video dhund raha hu...")
        query = message.text.split(" ", 1)[1]
        try:
            title, duration, link = ytDetails.searchYt(query)
        except Exception as e:
            await message.reply_text(f"Error :- <code>{e}</code>")
            return
        await m.edit("Rukja...Tera video download kar raha hu...")
        resp, ytlink = await ytdl(link)
        if resp == 0:
            await m.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
        else:
            if chat_id in QUEUE:
                queue_num = add_to_queue(
                    chat_id, title[:19], duration, ytlink, link)
                await m.edit(f"# {queue_num}\n{title[:19]}\nTera Video queue me daal diya hu")
                return
            # await asyncio.sleep(2)
            Status, Text = await userbot.playVideo(chat_id, ytlink)
            if Status == False:
                await m.edit(Text)
            else:
                if duration is None:
                    duration = "Playing From LiveStream"
                add_to_queue(chat_id, title[:19], duration, ytlink, link)
                finish_time = time.time()
                total_time_taken = str(int(finish_time - start_time)) + "s"
                await m.edit(f"Tera video play kar rha hu aaja vc\n\nVideoName:- [{title[:19]}]({link})\nDuration:- {duration}\nTime taken to play:- {total_time_taken}", disable_web_page_preview=True)
