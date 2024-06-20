import time
from pyrogram import filters

from .logging import LOGGER
import config


SUDOERS = filters.user()

_boot_ = time.time()


def sudo():
    global SUDOERS
    for user_id in config.OWNER_ID:
        SUDOERS.add(user_id)
    LOGGER("YMusic").info("SUDO USERS LOADED")
