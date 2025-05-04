# Discord Bot Blueprint
Super enkel Discord bot blueprint. Bruk denne som utgangspunkt for å lage din egen Discord bot.

## Oppsett
Installer dependencies (discord):
```bash
pip install -r requirements.txt
```

Eventuelt kan du finne den i PyCharm sin "Packages" fane, eller kjøre følgende i terminalen:
```bash
pip install discord
```

## Lag botten
Du må lage din egen discord bot og legge token i en fil `token.txt` i src mappen, filen genereres av `setup.py`.

Følg stegene her for å lage en bot: https://discordpy.readthedocs.io/en/latest/discord.html, før du kjører `setup.py` (eller rediger `token.txt` manuelt).

Merk at du må gi botten `Message Content Intents` under `Special Privileges`, for å kunne lese meldinger som blir sendt i en chat.


## Kjør botten og rediger koden
Sørg for at `token.txt` eksisterer, hvis ikke kjør `setup.py` først.

Botten ligger i `main.py`. Du kan redigere denne filen for å legge til funksjonalitet til botten. Det er lagt inn 2 eksempelfunksjoner.

## Dokumentasjon
Dokumentasjon for discord.py: https://discordpy.readthedocs.io/en/stable/intro.html

Å lese dokumentasjon er en god øvelse!
