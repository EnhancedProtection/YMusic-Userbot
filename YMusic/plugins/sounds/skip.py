from httpx import delete
from YMusic import app, call
from YMusic.core import userbot
from YMusic.utils.queue import QUEUE, pop_an_item, get_queue, clear_queue
from YMusic.utils.loop import get_loop
from YMusic.misc import SUDOERS

from pytgcalls.types import MediaStream

# from pytgcalls.types.input_stream import AudioPiped
# from pytgcalls.types.input_stream.quality import HighQualityAudio


from pyrogram import filters
from pyrogram.enums import ChatMembersFilter

import time

import config

SKIP_COMMAND = ["SKIP"]

PREFIX = config.PREFIX

RPREFIX = config.RPREFIX


@app.on_message((filters.command(SKIP_COMMAND, [PREFIX, RPREFIX])) & filters.group)
async def _aSkip(_, message):
    start_time = time.time()
    chat_id = message.chat.id

    # Get administrators
    administrators = []
    async for m in app.get_chat_members(
        chat_id, filter=ChatMembersFilter.ADMINISTRATORS
    ):
        administrators.append(m)

    if (message.from_user.id) in SUDOERS or (message.from_user.id) in [
        admin.user.id for admin in administrators
    ]:
        m = await message.reply_text("Trying to skip the current song...")
        loop = await get_loop(chat_id)
        if loop != 0:
            return await m.edit_text(
                f"Loop is enabled for the current song. Please disable it with {PREFIX}endloop to skip the song."
            )
        if chat_id in QUEUE:
            chat_queue = get_queue(chat_id)
            if len(chat_queue) == 1:
                clear_queue(chat_id)
                await stop(chat_id)
                await m.edit_text(
                    f"There is no next track. I'm leaving the voice chat..."
                )
                return
            try:
                title = chat_queue[1][1]
                duration = chat_queue[1][2]
                songlink = chat_queue[1][3]
                link = chat_queue[1][4]
                await call.play(
                    chat_id,
                    MediaStream(
                        songlink,
                        video_flags=MediaStream.Flags.AUTO_DETECT,
                    ),
                )
                finish_time = time.time()
                pop_an_item(chat_id)
                total_time_taken = str(int(start_time - finish_time)) + "s"
                await m.delete()
                await app.send_message(
                    chat_id,
                    f"Playing Your Song\n\nSongName:- [{title}]({link})\nDuration:- {duration}\nTime taken to play:- {total_time_taken}",
                    disable_web_page_preview=True,
                )
                # return [title, duration, link, finish_time]
            except Exception as e:
                await m.delete()
                return await app.send_message(chat_id, f"Error:- <code>{e}</code>")
        else:
            clear_queue(chat_id)
            await stop(chat_id)
            return await m.edit_text("Gadhe queue empty hai... songs queue me toh daal")
    else:
        return await message.reply_text(
            "Abe saale... (Maaf karna wo gusse me thora sa idhar udhar ho jata hu) terepe perms naa hai admins ko bol..."
        )

@app.on_message(filters.command("queue", [PREFIX, RPREFIX]) & filters.group)
async def _queue(_, message):
    chat_id = message.chat.id
    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await message.reply_text(
                f"Queue is empty"
            )
            return
        queue = chat_queue[1:]
        output = "**Queue:**\n"
        for i, item in enumerate(queue):
            title = item[1]
            duration = item[2]
            link = item[4]
            output += f"{i + 1}. [{title}]({link}) - {duration}\n"
        await message.reply_text(output, disable_web_page_preview=True)
    else:
        await message.reply_text("Queue is empty")

async def stop(chat_id):
    try:
        await call.leave_call(chat_id)
    except:
        pass
