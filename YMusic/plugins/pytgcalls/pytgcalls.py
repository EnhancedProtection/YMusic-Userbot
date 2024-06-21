from pytgcalls import PyTgCalls, filters
from pytgcalls.types import Update, MediaStream

from YMusic import call, app
from YMusic.utils.queue import QUEUE, get_queue, clear_queue, pop_an_item
from YMusic.utils.loop import get_loop, set_loop

import time


async def _skip(chat_id):
    loop = await get_loop(chat_id)
    if loop == 0:
        pass
    else:
        try:
            chat_queue = get_queue(chat_id)
            loop = loop - 1
            await set_loop(chat_id, loop)
            title = chat_queue[0][1]
            duration = chat_queue[0][2]
            songlink = chat_queue[0][3]
            link = chat_queue[0][4]
            await call.play(
                chat_id,
                MediaStream(
                    songlink,
                    video_flags=MediaStream.Flags.IGNORE,
                ),
            )
            finish_time = time.time()
            return [title, duration, link, finish_time]
        except Exception as e:
            return [2, f"Error:- <code>{e}</code>"]

    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await stop(chat_id)
            clear_queue(chat_id)
            return 1
        else:
            try:
                title = chat_queue[1][1]
                duration = chat_queue[1][2]
                songlink = chat_queue[1][3]
                link = chat_queue[1][4]
                await call.play(
                    chat_id,
                    MediaStream(
                        songlink,
                        video_flags=MediaStream.Flags.IGNORE,
                    ),
                )
                finish_time = time.time()
                pop_an_item(chat_id)
                return [title, duration, link, finish_time]
            except Exception as e:
                return [2, f"Error:- <code>{e}</code>"]
    await stop(chat_id)
    return 1


@call.on_update(filters.stream_end)
async def handler(client: PyTgCalls, update: Update):
    start_time = time.time()
    chat_id = update.chat_id
    resp = await _skip(chat_id)
    if resp == 1:
        pass
    elif resp[0] == 2:
        await app.send_message(chat_id, resp[1])
    else:
        total_time_taken = str(int(start_time - resp[3])) + "s"
        await app.send_message(
            chat_id,
            f"Playing Your Song\n\nSongName:- [{resp[0]}]({resp[2]})\nDuration:- {resp[1]}\nTime taken to play:- {total_time_taken}",
            disable_web_page_preview=True,
        )


async def stop(chat_id):
    try:
        await call.leave_call(
            chat_id,
        )
    except:
        pass
