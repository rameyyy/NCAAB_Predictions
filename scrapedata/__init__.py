#scrapedata/__init__.py

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
    return matchhistory_path, leaderboard_path, schedule_path

# import modules
from .barttorvik_individual import IndividualTeamScrape
from .barttorvik_leaderboard import LeaderboardScrape
from .barttorvik_schedule import DateSchedule

# define __all__ aka import *
__all__ = ['IndividualTeamScrape', 'LeaderboardScrape', 'DateSchedule']