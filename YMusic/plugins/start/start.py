from pyrogram import filters
from YMusic import app
import config

PREFIX = config.PREFIX
START_COMMAND = ["START", "ST"]

@app.on_message(filters.private 
	& filters.command(START_COMMAND, PREFIX)
	)
async def _start(_, message):
	await message.reply_text("Hey user how are you.\nIf you need any help just ping me I am here to help you.")
