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
        
    def calculate_run_time(self, start_time, final_print:bool):
        if final_print != True:
            elapsed_time = time.time() - start_time
            mins, secs = divmod(elapsed_time, 60)
            print(f"\rElapsed time: {mins:.0f} minutes, {secs:.2f} seconds", end="", flush=True)
        else:
            final_time = time.time() - start_time
            mins_final, secs_final = divmod(final_time, 60)
            print(f'\nFinished in {mins_final} minutes, {secs_final} seconds.')
        
    def scrape_all(self, dont_scrape_player_stats:bool):
        start_time = time.time()
        self.commonFuncs.clear_match_hist_stats()
        self.calculate_run_time(start_time, False)
        self.commonScrape.get_todays_schedule_refresh()
        self.calculate_run_time(start_time, False)
        self.commonScrape.leaderboard_refresh()
        self.calculate_run_time(start_time, False)
        paths_arr = self.commonFuncs.get_path()
        path_to_schedule = paths_arr[2]
        schedule_data = self.commonFuncs.load_json_file(path_to_schedule)
        for date, matches in schedule_data.items():
            for match in matches:
                t1 = match[0]
                t2 = match[2]
                self.calculate_run_time(start_time, False)
                self.commonScrape.teams_matchHist_thisSeason_plusPrevTwoYears_noRefresh(t1)
                self.calculate_run_time(start_time, False)
                self.commonScrape.teams_matchHist_thisSeason_plusPrevTwoYears_noRefresh(t2)
                if dont_scrape_player_stats != True:
                    self.calculate_run_time(start_time, False)
                    self.commonScrape.get_playerStats_with_match_hist(t1)
                    self.calculate_run_time(start_time, False)
                    self.commonScrape.get_playerStats_with_match_hist(t2)
        self.calculate_run_time(start_time, True)
                