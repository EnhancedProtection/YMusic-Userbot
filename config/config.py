import os


API_ID: int = int(os.getenv("API_ID")) or int()

API_HASH: str = os.getenv("API_HASH") or str("")

SESSION_STRING: str = os.getenv("SESSION_STRING") or str("")

OWNER_ID: list[int] = [int(os.getenv("OWNER_ID"))] or []

LOG_GROUP_ID: int = int(os.getenv("LOG_GROUP_ID")) or int()

PREFIX: str = str(".")

RPREFIX: str = str("$")


# No Need To Edit Below This

LOG_FILE_NAME: str = "YMusic.txt"
