import time
import handledata
import scrapedata
from . import commonScrapes

class CurrentDayScrape:
    def __init__(self):
        from . import get_paths
        paths_arr = get_paths()
        path_to_path = paths_arr[7]
        handledata_module = handledata
        handledata_module.initialize_path(path_to_path)
        self.commonFuncs = handledata_module.CommonFunctions()
        self.scrapedata_module = scrapedata
        self.scrapedata_module.initialize_path(path_to_path)
        self.commonScrape = commonScrapes.CommonScrapes()
        
    def scrape_all(self):
        self.commonFuncs.clear_match_hist_stats()
        self.commonScrape.get_todays_schedule_refresh()
        self.commonScrape.leaderboard_refresh()
        paths_arr = self.commonFuncs.get_path()
        path_to_schedule = paths_arr[2]
        schedule_data = self.commonFuncs.load_json_file(path_to_schedule)
        for date, matches in schedule_data.items():
            for match in matches:
                t1 = match[0]
                at_vs = match[1]
                t2 = match[2]
                self.commonScrape.teams_matchHist_thisSeason_plusPrevTwoYears_noRefresh(t1)
                self.commonScrape.teams_matchHist_thisSeason_plusPrevTwoYears_noRefresh(t2)