


from pyrogram import filters

from YMusic import app
from YMusic.utils.queue import clear_queue
from YMusic.utils.loop import get_loop, set_loop
from YMusic.core import userbot
import config



PREFIX = config.PREFIX

RPREFIX = config.RPREFIX

STOP_COMMAND = ["STOP", "CHUP"]

PAUSE_COMMAND = ["PAUSE"]

RESUME_COMMAND = ["RESUME"]

MUTE_COMMAND = ["MUTE"]

UNMUTE_COMMAND = ["UNMUTE"]

VOLUME_COMMAND = ["VOLUME"]

LOOP_COMMAND = ["LOOP"]

LOOPEND_COMMAND = ["ENDLOOP"]


@app.on_message(filters.command(STOP_COMMAND, PREFIX))
async def _stop(_, message):
	Text = await userbot.stop(message.chat.id)
	try :
		clear_queue(message.chat.id)
	except :
		pass
	await message.reply_text(Text)

@app.on_message(filters.command(STOP_COMMAND, RPREFIX))
async def _stop(_, message):
	if (len(message.command)) != 2 :
		await message.reply_text("You forgot to pass an argument")
	else :
		msg_id = msg_id = message.text.split(" ", 1)[1]
		Text = await userbot.stop(msg_id)
		await message.reply_text(Text)




@app.on_message(filters.command(PAUSE_COMMAND, PREFIX))
async def _pause(_, message):
	Text = await userbot.pause(message.chat.id)
	await message.reply_text(Text)

@app.on_message(filters.command(PAUSE_COMMAND, RPREFIX))
async def _pause(_, message):
	if (len(message.command)) != 2 :
		await message.reply_text("You forgot to pass an argument")
	else :
		msg_id = msg_id = message.text.split(" ", 1)[1]
		Text = await userbot.pause(msg_id)
		await message.reply_text(Text)




@app.on_message(filters.command(RESUME_COMMAND, PREFIX))
async def _resume(_, message):
	Text = await userbot.resume(message.chat.id)
	await message.reply_text(Text)

@app.on_message(filters.command(RESUME_COMMAND, RPREFIX))
async def _resume(_, message):
	if (len(message.command)) != 2 :
		await message.reply_text("You forgot to pass an argument")
	else :
		msg_id = msg_id = message.text.split(" ", 1)[1]
		Text = await userbot.resume(msg_id)
		await message.reply_text(Text)




@app.on_message(filters.command(MUTE_COMMAND, PREFIX))
async def _mute(_, message):
	if message.from_user and message.from_user.is_self :
		reply = message.edit
	else :
		reply = message.reply_text
	Text = await userbot.mute(message.chat.id)
	await reply(Text)

@app.on_message(filters.command(MUTE_COMMAND, RPREFIX))
async def _mute(_, message):
	if (len(message.command)) != 2 :
		await message.reply_text("You forgot to pass an argument")
	else :
		msg_id = msg_id = message.text.split(" ", 1)[1]
		Text = await userbot.mute(msg_id)
		await message.reply_text(Text)




@app.on_message(filters.command(UNMUTE_COMMAND, PREFIX))
async def _unmute(_, message):
	Text = await userbot.unmute(message.chat.id)
	await message.reply_text(Text)

@app.on_message(filters.command(UNMUTE_COMMAND, RPREFIX))
async def _mute(_, message):
	if (len(message.command)) != 2 :
		await message.reply_text("You forgot to pass an argument")
	else :
		msg_id = msg_id = message.text.split(" ", 1)[1]
		Text = await userbot.unmute(msg_id)
		await message.reply_text(Text)



@app.on_message(filters.command(VOLUME_COMMAND, PREFIX))
async def _volume(_, message):
	try :
		vol = int(message.text.split()[1])
		Text = await userbot.changeVolume(message.chat.id, vol)
	except :
		Text = await userbot.changeVolume(message.chat.id)
	await message.reply_text(Text)




@app.on_message(filters.command(LOOP_COMMAND, PREFIX))
async def _loop(_, message) :
	loop = await get_loop(message.chat.id)
	if loop == 0 :
		try :
			await set_loop(message.chat.id, 5)
			await message.reply_text("Loop enabled. Now current song will be played 5 times")
		except Exception as e:
			return await message.reply_text(f"Error:- <code>{e}</code>")
	
	else :
		await message.reply_text("Loop already enabled")


@app.on_message(filters.command(LOOPEND_COMMAND, PREFIX))
async def _endLoop(_, message) :
	loop = await get_loop(message.chat.id)
	if loop == 0 :
		await message.reply_text("Lopp is not enabled")
	else :
		try :
			await set_loop(message.chat.id, 0)
			await message.reply_text("Loop Disabled")
		except Exception as e :
			return await message.reply_text(f"Error:- <code>{e}</code>")

