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
    specific_match_player_stats = os.path.expandvars(paths.get("SPECIFICMATCH_PLAYER_STATS"))
    model_path = os.path.expandvars(paths.get("MODELS"))
    handledata_path = os.path.expandvars(paths.get("HANDLEDATA"))
    scrapedata_path = os.path.expandvars(paths.get("SCRAPEDATA"))
    path_to_path = os.path.expandvars(paths.get("PATHTOPATH"))
    return matchhistory_path, leaderboard_path, schedule_path, specific_match_player_stats, model_path, handledata_path, scrapedata_path, path_to_path

from .analyzeMatchHist import AnalyzeMatchHist
from .commonFunctions import CommonFunctions
from .pointPrediction import PointPrediction
from .accuracyEstimate import AccuracyEstimate
from .prevWinner import PrevWinner
from .analyzeMatchHist2 import AnalyzeMatchHist2

__all__ = ['AnalyzeMatchHist', 'CommonFunctions', 'PointPrediction', 'AccuracyEstimate', 'PrevWinner', 'AnalyzeMatchHist2']