import discord
from discord import app_commands
from utils import (
    save_twitch_usernames,
    TWITCH_USERNAMES,
    save_notif_settings,
)

# /addtwitch (Moderator only)
@app_commands.command(name="addtwitch", description="Add a Twitch username to the list (Moderator only).")
@app_commands.describe(username="The Twitch username to add.")
async def addtwitch(interaction: discord.Interaction, username: str):
    if discord.utils.get(interaction.user.roles, name="Unpaid Intern") or discord.utils.get(interaction.user.roles, name="Idiot Streamer Guy"):
        username = username.strip()
        if username not in TWITCH_USERNAMES:
            TWITCH_USERNAMES.append(username)
            save_twitch_usernames(TWITCH_USERNAMES)
            await interaction.response.send_message(
                f"Added {username} to the Twitch usernames list.", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"{username} is already in the Twitch usernames list.", ephemeral=True
            )
    else:
        await interaction.response.send_message(
            "You do not have permission to use this command.", ephemeral=True
        )

# /rmtwitch (Moderator only)
@app_commands.command(name="rmtwitch", description="Remove a Twitch username from the list (Moderator only).")
@app_commands.describe(username="The Twitch username to remove.")
async def rmtwitch(interaction: discord.Interaction, username: str):
    if discord.utils.get(interaction.user.roles, name="Unpaid Intern") or discord.utils.get(interaction.user.roles, name="Idiot Streamer Guy"):
        username = username.strip()
        if username in TWITCH_USERNAMES:
            TWITCH_USERNAMES.remove(username)
            save_twitch_usernames(TWITCH_USERNAMES)
            await interaction.response.send_message(
                f"Removed {username} from the Twitch usernames list.", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"{username} is not in the Twitch usernames list.", ephemeral=True
            )
    else:
        await interaction.response.send_message(
            "You do not have permission to use this command.", ephemeral=True
        )

# /setnotifs (Moderator only)
@app_commands.command(
    name="setnotifs",
    description="Set the notification channel and role for Twitch streams (Moderator only).",
)
@app_commands.describe(
    channel="The channel to send notifications to.",
    role="The role to ping for Twitch notifications.",
)
@app_commands.checks.has_permissions(manage_channels=True)
async def setnotifs(
    interaction: discord.Interaction,
    channel: discord.TextChannel,
    role: discord.Role,
):
    if discord.utils.get(interaction.user.roles, name="Unpaid Intern") or discord.utils.get(interaction.user.roles, name="Idiot Streamer Guy"):
        save_notif_settings(interaction.guild.id, channel_id=channel.id, role_id=role.id)
        await interaction.response.send_message(
            f"Set the notification channel to {channel.mention} and the ping role to {role.mention}.",
            ephemeral=True,
        )
    else:
        await interaction.response.send_message(
            "You do not have permission to use this command.", ephemeral=True
        )

mod_commands = [addtwitch, rmtwitch, setnotifs]