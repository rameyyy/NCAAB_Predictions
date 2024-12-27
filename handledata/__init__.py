#handledata/__init__.py

import os
import json

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

from .analysis_part1 import MatchFirst500
from .common_functions import GrabData
from .point_predict import PointPrediction

__all__ = ['GrabData', 'MatchFirst500', 'PointPrediction']