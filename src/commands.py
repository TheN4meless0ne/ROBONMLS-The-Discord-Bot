import discord
from discord import app_commands
from utils import (
    STREAMER,
    SOCIALS_CHANNEL_ID,
)

# /socials
@app_commands.command(name="socials", description="Send to links channel.")
async def socials(interaction: discord.Interaction):
    socials_channel = interaction.guild.get_channel(SOCIALS_CHANNEL_ID)
    if socials_channel:
        await interaction.response.send_message(
            f"{STREAMER}'s socials and links can be found in {socials_channel.mention}.", ephemeral=True
        )
    else:
        await interaction.response.send_message(
            "The #links channel could not be found. Please contact an admin.", ephemeral=True
        )

# List of commands to register with the bot
commands_list = [socials]