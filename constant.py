import os
from dotenv import load_dotenv

# load .env variables
load_dotenv()

# guildIds = [833210288681517126] # test discord server
guildIds = None # force global commands

temp_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "temp")

TOKEN = os.getenv("TOKEN")
ckey = "pictureSurprise"
TENOR_KEY = os.getenv("tenor_key")
