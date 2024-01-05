
from YMusic import app
from YMusic.core import userbot
from YMusic.utils import ytDetails
from pyrogram import filters
import asyncio
import time
import config

# Todo - Make vplay to support Queue;
VIDEO_PLAY = "VPLAY"

PREFIX = config.PREFIX

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


@app.on_message(filters.command(VIDEO_PLAY, PREFIX))
async def _vPlay(_, message) :
	start_time = time.time()
	if (len(message.command)) < 2 :
		await message.reply_text("Sale Link To Dal De")
	else :
		m = await message.reply_text("Downloading...")
		query = message.text.split(" ", 1)[1]
		title, duration, link = ytDetails.searchYt(query)
		resp, ytlink = await ytdl(link)
		if resp == 0:
			await m.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
		else :
			Status, Text = await userbot.playVideo(message.chat.id, ytlink)
			if Status == False :
				await m.edit(Text)
			else :
				if duration is None :
					duration = "Playing From LiveStream"
				finish_time = time.time()
				total_time_taken = str(int(finish_time - start_time)) + "s"
				await m.edit(f"Playing Your Song\n\nSongName:- [{title[:19]}]({link})\nDuration:- {duration}\nTime taken to play:- {total_time_taken}", disable_web_page_preview=True)
		




