
import discord
from discord import app_commands
import aiohttp
import asyncio
from utils import (
    tokens,
    TWITCH_USERNAMES,
    STREAMER,
    TWITCH_CLIENT_ID,
    get_twitch_access_token,
    load_notif_settings,
    get_all_guild_ids,
)

guild_ids = get_all_guild_ids()
CHECK_INTERVAL = 60  # Seconds between checks

async def check_live_status(access_token, usernames):
    """Check if any Twitch users are live."""
    url = "https://api.twitch.tv/helix/streams"
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {access_token}"
    }
    live_users = []
    async with aiohttp.ClientSession() as session:
        for username in usernames:
            params = {"user_login": username}
            async with session.get(url, headers=headers, params=params) as response:
                data = await response.json()
                if len(data["data"]) > 0:  # User is live
                    live_users.append(username)
    return live_users

async def notify_when_live(bot):
    """Periodically check if Twitch users are live and send notifications."""
    access_token = await get_twitch_access_token()
    notified_users_per_guild = {}  # Track notified users for each guild

    while True:
        try:
            for guild_id in guild_ids:
                guild = bot.get_guild(guild_id)
                if guild is None:
                    print(f"Could not find guild with ID {guild_id}")
                    continue

                # Load notification channel and role IDs from notif.json
                notif_channel_id, notif_role_id = load_notif_settings(guild_id)
                if notif_channel_id is None or notif_role_id is None:
                    print(f"Notification channel or role not set for guild {guild_id}.")
                    continue

                channel = bot.get_channel(notif_channel_id)
                role = guild.get_role(notif_role_id)
                if channel is None or role is None:
                    print(f"Could not find channel or role for IDs {notif_channel_id}, {notif_role_id}")
                    continue

                # Initialize notified users for this guild if not already done
                if guild_id not in notified_users_per_guild:
                    notified_users_per_guild[guild_id] = set()

                live_users = await check_live_status(access_token, TWITCH_USERNAMES)
                for user in live_users:
                    if user not in notified_users_per_guild[guild_id]:
                        if user == STREAMER:
                            await channel.send(
                                f"I'm now live on Twitch!! Come say hi!! https://www.twitch.tv/{user} {role.mention}"
                            )
                        else:
                            await channel.send(
                                f"{user} is now live on Twitch!! Go check them out!! https://www.twitch.tv/{user} {role.mention}"
                            )
                        notified_users_per_guild[guild_id].add(user)

                # Remove users who are no longer live from the notified list for this guild
                notified_users_per_guild[guild_id] = notified_users_per_guild[guild_id].intersection(live_users)
        except Exception as e:
            print(f"Error checking Twitch live status: {e}")
        await asyncio.sleep(CHECK_INTERVAL)
