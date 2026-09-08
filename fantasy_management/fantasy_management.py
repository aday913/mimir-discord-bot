import logging
import os

from espn_api.football import League, Player
from dotenv import load_dotenv

class FantasyManager:
    def __init__(self, league_id: int, year: int, espn_s2: str, swid: str):
        try:
            self.league = League(league_id=league_id, year=year, espn_s2=espn_s2, swid=swid)
        except Exception as e:
            print(f"Error initializing League: {e}")
            raise


if __name__ == "__main__":
    log = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    load_dotenv()

    try:
        league_id = int(os.getenv("LEAGUE_ID"))
        year = int(os.getenv("YEAR"))
        espn_s2 = os.getenv("ESPN_S2")
        swid = os.getenv("SWID")

        fantasy_manager = FantasyManager(league_id, year, espn_s2, swid)
    except Exception as e:
        log.error(f"An error occurred while initializing FantasyManager: {e}")
        raise
    
    league = fantasy_manager.league

    my_team = league.teams[0]  # Assuming you want the first team in the league

    for player in my_team.roster:
        print(f"{player.name:<20} Position: {player.position:<5} Linup Slot: {player.lineupSlot:<10} Status: {player.injuryStatus}")
