from pyrogram import filters
from YMusic import app
import config

PREFIX = config.PREFIX
START_COMMAND = ["START", "ST"]
HELP_COMMAND = ["HELP", "HP"]

HELP_MESSAGE = f"""
**YMusic Bot Help**

**Commands:**
- `{PREFIX}start` - Check if the bot is online
- `{PREFIX}ping` - Check the bot's ping
- `{PREFIX}play [name|link|reply]` - Play a song audio by giving song name or link or reply to an audio file
- `{PREFIX}vplay [name|link|reply]` - Play a song video by giving song name or link or reply to a video file
- `{PREFIX}pause` - Pause the current song
- `{PREFIX}resume` - Resume the current song
- `{PREFIX}mute` - Mute the bot in the voice chat
- `{PREFIX}unmute` - Unmute the bot in the voice chat
- `{PREFIX}skip` - Skip the current song
- `{PREFIX}stop` - Stop the music player
- `{PREFIX}chup` - Stop the music player
- `{PREFIX}volume` - Adjust the volume
- `{PREFIX}vol` - Adjust the volume
- `{PREFIX}loop` - Loop the current song 5 times
- `{PREFIX}endloop` - End the loop
- `{PREFIX}help` - Show this help message

**More commands coming soon!**
"""

@app.on_message(filters.private & filters.command(START_COMMAND, PREFIX))
async def _start(_, message):
    await message.reply_text(
        "Hey user how are you.\nIf you need any help just ping me I am here to help you."
    )

@app.on_message(filters.command(HELP_COMMAND, PREFIX))
async def _help(_, message):
    await message.reply_text(HELP_MESSAGE)
