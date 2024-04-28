from YMusic import call
from pytgcalls.types import MediaStream

audio_file = "http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4"


async def playAudio(chat_id, audio_file=audio_file):
    try:
        await call.play(
            chat_id,
            MediaStream(
                audio_file,
                video_flags=MediaStream.Flags.IGNORE,
            ),
        )
        return True, None
    except Exception as e:
        return False, f"Error:- <code>{e}</code>"


async def playVideo(chat_id, video_file=audio_file):
    try:
        await call.play(
            chat_id,
            MediaStream(
                video_file,
            ),
        )
        return True, None
    except Exception as e:
        return False, f"Error:- <code>{e}</code>"


async def pause(chat_id):
    try:
        await call.pause_stream(
            chat_id,
        )
        return "Stream Paused"
    except Exception as e:
        return f"Error:- <code>{e}</code>"


async def resume(chat_id):
    try:
        await call.resume_stream(
            chat_id,
        )
        return "Stream Resumed"
    except Exception as e:
        return f"Error:- <code>{e}</code>"


async def mute(chat_id):
    try:
        await call.mute_stream(
            chat_id,
        )
        return "Stream Muted"
    except Exception as e:
        return f"Error:- <code>{e}</code>"


async def unmute(chat_id):
    try:
        await call.unmute_stream(
            chat_id,
        )
        return "Stream Unmuted"
    except Exception as e:
        return f"Error:- <code>{e}</code>"


async def changeVolume(chat_id, volume: int = 200):
    try:
        await call.change_volume_call(
            chat_id,
            volume,
        )
        return f"🎧Volume Changed To:- {volume}%"
    except Exception as e:
        return f"Error:- <code>{e}</code>"


async def stop(chat_id):
    try:
        await call.leave_call(
            chat_id,
        )
        return "Stream Ended"
    except Exception as e:
        return f"Error:- <code>{e}</code>"
