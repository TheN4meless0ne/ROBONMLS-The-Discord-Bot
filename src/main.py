import discord
from discord.ext import commands
from time import sleep
from commands import commands_list
from commands_mod import mod_commands
from twitch_notif import notify_when_live
from utils import DISCORD_TOKEN


intents = discord.Intents.default()
intents.message_content = True  # Må aktiveres under Privileged Gateway Intents på https://discord.com/developers/applications/
bot = commands.Bot(command_prefix="/", intents=intents)


# Registrerer kommandene i commands.py og legger dem til i botten.
@bot.event
async def on_ready():
    for command in commands_list:  # commands_list er en liste med alle kommandoene og ligger i commands.py
        bot.tree.add_command(command)
    for command in mod_commands:  # mod_commands er en liste med alle kommandoene og ligger i commands_mod.py
        bot.tree.add_command(command)
    bot.loop.create_task(notify_when_live(bot))  # Pass the bot instance here
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")


@bot.event
async def on_message(message):
    """on_message kjøres når botten mottar en melding."""
    text = message.content
    user = message.author

    # Sjekker om meldingen er fra boten selv, for å unngå at den svarer på seg selv.
    if user == bot.user:
        return

# Det finnes flere ulike events man kan bruke til ulike formål,
# se https://discordpy.readthedocs.io/en/latest/api.html#event-reference


# Til slutt; kjør botten med token fra token.txt (med litt tips og feilsøking)
# Du kan ignorere dette.
if __name__ == '__main__':
    print('Starting ')
    try:
        bot.run(DISCORD_TOKEN)
    except discord.errors.PrivilegedIntentsRequired:
        print('OBS! Din bot mangler "Message Content Intent", legg til denne \n'
              'på https://discord.com/developers/applications/ (Under Privileged Gateway Intents)')
    except discord.errors.LoginFailure:
        print('Kunne ikke logge på botten, bruker du riktig token i token.txt?')
    except FileNotFoundError:
        print('Finner ikke token.txt, har du kjørt setup.py og limt inn din token?')
    finally:
        # Vent 5 sekunder før EventLoop lukkes, som gir en større og mindre lesbar feilmelding.
        sleep(5)
