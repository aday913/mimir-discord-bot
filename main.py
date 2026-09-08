#!/usr/bin/env python3

import json
import logging
import os
import time

from discord import Intents
from discord import utils as discord_utils
from discord.ext import commands
from dotenv import load_dotenv

from fantasy_management.fantasy_management import FantasyManager

log = logging.getLogger(__name__)

intents = Intents.all()

bot = commands.Bot(
    command_prefix="?",
    intents=intents,
    case_insensitive=True,
)

fantasy_manager: FantasyManager = None

@bot.command(name="roster", help="Get the roster of a team by team ID")
async def roster(ctx):
    logging.info(f"Roster command invoked by {ctx.author} in channel {ctx.channel}")
    league = fantasy_manager.league

    my_team = league.teams[0]  # Assuming you want the first team in the league

    message = """Example Roster:\n"""
    for player in my_team.roster:
        message += f"{player.name:<20} Position: {player.position:<5} Linup Slot: {player.lineupSlot:<10} Status: {player.injuryStatus}\n"
    logging.info(f"Roster command completed. Sending message:\n{message}")
    await ctx.send(f"```{message}```")


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

        league_id = int(os.getenv("LEAGUE_ID"))
        year = int(os.getenv("YEAR"))
        espn_s2 = os.getenv("ESPN_S2")
        swid = os.getenv("SWID")

        fantasy_manager = FantasyManager(league_id, year, espn_s2, swid)

        bot.run(os.getenv("DISCORD_TOKEN"))
    except Exception as e:
        log.error(f"An error occurred: {e}")
        raise
    finally:
        log.info("Bot has stopped.")
