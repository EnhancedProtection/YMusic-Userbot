import os


API_ID: int = int(os.getenv("API_ID", 0))

API_HASH: str = os.getenv("API_HASH", "")

SESSION_STRING: str = os.getenv("SESSION_STRING", "")

OWNER_ID: list[int] = [int(os.getenv("OWNER_ID", 0))]

LOG_GROUP_ID: int = int(os.getenv("LOG_GROUP_ID", 0))

PREFIX: str = str(".")

RPREFIX: str = str("$")


# No Need To Edit Below This

LOG_FILE_NAME: str = "YMusic.txt"
