import os
import asyncio
import logging

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("bot")

# --- Intents ---
# Το bot χρειάζεται αυτά τα intents. Πρέπει να τα ενεργοποιήσεις
# ΚΑΙ στο Discord Developer Portal (Bot -> Privileged Gateway Intents):
#   - SERVER MEMBERS INTENT (για auto-roles / moderation σε members)
#   - MESSAGE CONTENT INTENT (αν αργότερα προσθέσεις text-based commands)
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    log.info(f"Συνδέθηκε ως {bot.user} (ID: {bot.user.id})")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="τον server σου με ! εντολές 👀")
    )


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("_"):
            ext_name = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(ext_name)
                log.info(f"Φορτώθηκε: {ext_name}")
            except Exception as e:
                log.error(f"Αποτυχία φόρτωσης {ext_name}: {e}")


async def main():
    if not TOKEN:
        raise RuntimeError(
            "Δεν βρέθηκε DISCORD_TOKEN. Δημιούργησε ένα αρχείο .env (δες .env.example) "
            "και βάλε εκεί το token του bot σου."
        )
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
