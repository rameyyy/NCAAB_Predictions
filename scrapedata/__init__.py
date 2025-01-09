#scrapedata/__init__.py
# All scraping from NCAAB Barttorvik stats
import json
import os

def initialize_path(path_to_paths:str):
    global expanded_path
    expanded_path = os.path.expandvars(path_to_paths)
    
def get_paths():
    with open(expanded_path, 'r') as f:
        path_data = json.load(f)
    paths = path_data.get("PATHS")
    matchhistory_path = os.path.expandvars(paths.get("MATCHHIST"))
    leaderboard_path = os.path.expandvars(paths.get("LEADERBOARD"))
    schedule_path = os.path.expandvars(paths.get("SCHEDULE"))
    specific_match_player_stats = os.path.expandvars(paths.get("SPECIFICMATCH_PLAYER_STATS"))
    return matchhistory_path, leaderboard_path, schedule_path, specific_match_player_stats

# import modules
from .matchHistory import MatchHistory
from .leaderboardStats import LeaderboardStats
from .gameSchedule import GameSchedule
from .matchPlayerStats import MatchPlayerStats
from .gameWinners import GameWinners

# define __all__ aka import *
__all__ = ['MatchHistory', 'LeaderboardStats', 'GameSchedule', 'MatchPlayerStats', 'GameWinners']