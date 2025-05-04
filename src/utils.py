import json
import aiohttp
import os

# Hent Twitch-brukernavn fra en fil
# Hvis filen ikke finnes, returner en liste med standard brukernavn
def load_twitch_usernames():
    try:
        with open("twitch_usernames.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return [STREAMER]

# Save Twitch usernames to a file
def save_twitch_usernames(usernames):
    with open("twitch_usernames.json", "w") as file:
        json.dump(usernames, file)

# Load tokens from token.txt
def load_tokens():
    tokens = {}
    with open("token.txt", "r") as file:
        for line in file:
            key, value = line.strip().split("=")
            tokens[key] = value
    return tokens

async def get_twitch_access_token():
    """Fetch an access token from Twitch."""
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": TWITCH_CLIENT_ID,
        "client_secret": TWITCH_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, params=params) as response:
            data = await response.json()
            return data["access_token"]

# Save/load notification channel and role IDs per guild in notif.json
NOTIF_FILE = "notif.json"

def get_all_guild_ids():
    """Return a list of all guild IDs present in notif.json as integers."""
    if not os.path.exists(NOTIF_FILE):
        return []
    with open(NOTIF_FILE, "r") as f:
        data = json.load(f)
    return [int(gid) for gid in data.keys()]

def save_notif_settings(guild_id: int, channel_id: int = None, role_id: int = None):
    """Save the notification channel and/or role ID for a guild in notif.json."""
    data = {}
    if os.path.exists(NOTIF_FILE):
        with open(NOTIF_FILE, "r") as f:
            data = json.load(f)
    guild_key = str(guild_id)
    if guild_key not in data:
        data[guild_key] = {}
    if channel_id is not None:
        data[guild_key]["NOTIF_CHANNEL_ID"] = channel_id
    if role_id is not None:
        data[guild_key]["NOTIF_ROLE_ID"] = role_id
    with open(NOTIF_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_notif_settings(guild_id: int):
    """Load the notification channel and role ID for a guild from notif.json."""
    if not os.path.exists(NOTIF_FILE):
        return None, None
    with open(NOTIF_FILE, "r") as f:
        data = json.load(f)
    guild_key = str(guild_id)
    guild_data = data.get(guild_key, {})
    channel_id = guild_data.get("NOTIF_CHANNEL_ID")
    role_id = guild_data.get("NOTIF_ROLE_ID")
    return channel_id, role_id

# variables and constants
tokens = load_tokens()
TWITCH_USERNAMES = load_twitch_usernames()
STREAMER = "nmlsval"
SOCIALS_CHANNEL_ID = 1357714657573470430

TWITCH_CLIENT_SECRET = tokens["TWITCH_CLIENT_SECRET"]
TWITCH_CLIENT_ID = tokens["TWITCH_CLIENT_ID"]