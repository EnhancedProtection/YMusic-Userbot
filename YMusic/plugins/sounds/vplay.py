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

VIDEO_PLAY = ["VP", "VPLAY"]

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


async def processReplyToMessage(message):
    msg = message.reply_to_message
    if msg.video or msg.video_note:
        m = await message.reply_text("Rukja...Tera Video Download kar raha hu...")
        video_original = await msg.download()
        return video_original, m
    else:
        return None


async def playWithLinks(link):
    if "&" in link:
        pass
    if "?" in link:
        pass

    return 0


async def playback_completed(chat_id):
    if chat_id in QUEUE and QUEUE[chat_id]:
        next_video = QUEUE[chat_id].pop(0)
        await userbot.playVideo(chat_id, ytlink=next_video["ytlink"])
        await app.send_message(chat_id, f"Playing next video in queue:\n\n{next_video['title']}\n{next_video['link']}")
    else:
        # Leave the voice chat if there are no more videos in the queue
        await userbot.leaveVC(chat_id)


@app.on_message((filters.command(VIDEO_PLAY, PREFIX) | filters.command(VIDEO_PLAY, RPREFIX)) & filters.group)
async def _vPlay(_, message):
    start_time = time.time()
    chat_id = message.chat.id
    if (message.reply_to_message) is not None:
        if message.reply_to_message.video or message.reply_to_message.video_note:
            input_filename, m = await processReplyToMessage(message)
            if input_filename is None:
                await message.reply_text("Video pe reply kon karega mai? ya phir video link kon dalega mai? 🤔")
                return
            await m.edit("Rukja...Tera Video Play kar raha hu...")
            Status, Text = await userbot.playVideo(chat_id, input_filename)
            if Status == False:
                await m.edit(Text)
            else:
                await message.delete()
                if chat_id in QUEUE:
                    queue_num = add_to_queue(
                        chat_id, message.reply_to_message.video.title[:19], message.reply_to_message.video.duration, message.reply_to_message.video.file_id, message.reply_to_message.link)
                    await m.edit(f"# {queue_num}\n{message.reply_to_message.video.title[:19]}\nTera video queue me daal diya hu")
                    return
                finish_time = time.time()
                total_time_taken = str(int(finish_time - start_time)) + "s"
                await m.edit(f"Tera video play kar rha hu aaja vc\n\nVideoName:- [{message.reply_to_message.video.title[:19]}]({message.reply_to_message.link})\nDuration:- {message.reply_to_message.video.duration}\nTime taken to play:- {total_time_taken}", disable_web_page_preview=True)

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
            # Check if the video ended
            if Status == False:
                await m.edit(Text)
            else:
                if duration is None:
                    duration = "Playing From LiveStream"
                add_to_queue(chat_id, title[:19], duration, ytlink, link)

            # Trigger playback of the next video in the queue
            await playback_completed(chat_id)
        finish_time = time.time()
        total_time_taken = str(int(finish_time - start_time)) + "s"
        await m.edit(f"Tera video play kar rha hu aaja vc\n\nVideoName:- [{title[:19]}]({link})\nDuration:- {duration}\nTime taken to play:- {total_time_taken}", disable_web_page_preview=True)
