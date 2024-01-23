from YMusic import call
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls import StreamType
from pytgcalls.types import AudioParameters, VideoParameters, AudioQuality, VideoQuality

audio_file = "http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4"


async def playAudio(chat_id, audio_file=audio_file):
    try:
        await call.join_group_call(
            chat_id,
            AudioPiped(
                audio_file,
                AudioParameters.from_quality(AudioQuality.STUDIO),
            ),
        )
        return True, None
    except Exception as e:
        return False, f"Error:- <code>{e}</code>"


async def playVideo(chat_id, video_file=audio_file):
    try:
        await call.join_group_call(
            chat_id,
            AudioVideoPiped(
                video_file,
                AudioParameters.from_quality(AudioQuality.STUDIO),
                VideoParameters.from_quality(VideoQuality.UHD_4K),
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
        await call.leave_group_call(
            chat_id,
        )
        return "Stream Ended"
    except Exception as e:
        return f"Error:- <code>{e}</code>"
