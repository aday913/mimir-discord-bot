#!/usr/bin/env python3

import json
import logging
import os
import time

from discord import Intents
from discord import utils as discord_utils
from discord.ext import commands
from dotenv import load_dotenv

log = logging.getLogger(__name__)

intents = Intents.all()

bot = commands.Bot(
    command_prefix="?",
    intents=intents,
    case_insensitive=True,
)

@bot.event
async def on_ready():
    log.info(f"Logged in as {bot.user} (ID: {bot.user.id})")
    log.info("------")

if __name__ == "__main__":
    
    log = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    try:
        load_dotenv()

        bot.run(os.getenv("DISCORD_TOKEN"))
    except Exception as e:
        log.error(f"An error occurred: {e}")
        raise
    finally:
        log.info("Bot has stopped.")
