import sys
import os
import handledata
import scrapedata

class CommonScrapes:
    def __init__(self):
        from . import get_paths
        paths_arr = get_paths()
        path_to_path = paths_arr[7]
        handledata_module = handledata
        handledata_module.initialize_path(path_to_path)
        self.commonFuncs = handledata_module.CommonFunctions()
        self.scrapedata_module = scrapedata
        self.scrapedata_module.initialize_path(path_to_path)
    
    def get_todays_schedule_refresh(self):
        dateStr = self.commonFuncs.get_formatted_date()
        self.commonFuncs.clear_game_sched_file()
        self.scrapedata_module.GameSchedule(dateStr).scrape_data()
        
    def get_schedule_set_date(self, date_str):
        self.commonFuncs.clear_game_sched_file()
        self.scrapedata_module.GameSchedule(date_str).scrape_data()
    
    def game_winners(self, dateStr):
        self.scrapedata_module.GameWinners(dateStr).scrape_data()
    
    def teams_matchHist_thisSeason_plusPrevTwoYears_noRefresh(self, teams_name):
        dateStr = self.commonFuncs.get_formatted_date()
        yearStr_curr = self.commonFuncs.get_ncaa_season_year(dateStr)
        yearStr_curr_int = int(yearStr_curr)
        yearStr_curr_int -= 1
        yearStr_prev = str(yearStr_curr_int)
        yearStr_curr_int -= 1
        yearStr_prevPrev = str(yearStr_curr_int)
        self.scrapedata_module.MatchHistory(teams_name, yearStr_curr).scrape_data()
        self.scrapedata_module.MatchHistory(teams_name, yearStr_prev).scrape_data()
        self.scrapedata_module.MatchHistory(teams_name, yearStr_prevPrev).scrape_data()
    
    def leaderboard_refresh(self):
        dateStr = self.commonFuncs.get_formatted_date()
        yearStr_curr = self.commonFuncs.get_ncaa_season_year(dateStr)
        yearStr_curr_int = int(yearStr_curr)
        yearStr_curr_int -= 1
        yearStr_prev = str(yearStr_curr_int)
        yearStr_curr_int -= 1
        yearStr_prevPrev = str(yearStr_curr_int)
        self.commonFuncs.clear_leaderboard_file(yearStr_curr)
        self.commonFuncs.clear_leaderboard_file(yearStr_prev)
        self.commonFuncs.clear_leaderboard_file(yearStr_prevPrev)
        self.scrapedata_module.LeaderboardStats(yearStr_curr).scrape_data()
        self.scrapedata_module.LeaderboardStats(yearStr_prev).scrape_data()
        self.scrapedata_module.LeaderboardStats(yearStr_prevPrev).scrape_data()
        
    def get_playerStats_with_match_hist(self, team):
        paths_arr = self.commonFuncs.get_path()
        dateStr = self.commonFuncs.get_formatted_date()
        year_str = self.commonFuncs.get_ncaa_season_year(dateStr)
        matchHist_path = self.commonFuncs.adjust_matchHist_file_path(year_str)
        match_history_json_data = self.commonFuncs.load_json_file(matchHist_path)
        teams_matchHist_data = self.commonFuncs.get_team_data(match_history_json_data, team)
        teams_matchHist_data.pop('Rank')
        ops_name = teams_matchHist_data.pop('team_name')
        for matches_team_name, stats in teams_matchHist_data.items():
            date_unformatted = stats.get('Date')
            date_formatted = self.commonFuncs.reformat_date(date_unformatted)
            self.scrapedata_module.MatchPlayerStats(team, matches_team_name, date_formatted, year_str).scrape_data()