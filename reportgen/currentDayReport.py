import time
import handledata
import scrapedata
from . import commonScrapes

class CurrentDayReport:
    def __init__(self):
        from . import get_paths
        paths_arr = get_paths()
        path_to_path = paths_arr[7]
        handledata_module = handledata
        handledata_module.initialize_path(path_to_path)
        self.analysis_module = handledata_module
        self.commonFuncs = handledata_module.CommonFunctions()
        self.scrapedata_module = scrapedata
        self.scrapedata_module.initialize_path(path_to_path)
        self.commonScrape = commonScrapes.CommonScrapes()
    
    def __format_date_str_prettify(self, date_string):
        from datetime import datetime
        date_obj = datetime.strptime(date_string, '%Y%m%d')
        formatted_date_obj = date_obj.strftime('%m/%d/%Y')
        formatted_date_str = str(formatted_date_obj)
        return formatted_date_str
    
    def generate_report(self, print_yes_no:bool, file_yes_no:bool, file_name:str):
        paths_arr = self.commonFuncs.get_path()
        path_to_schedule = paths_arr[2]
        schedule_data = self.commonFuncs.load_json_file(path_to_schedule)
        final_write_str = ''
        for dateStr, matches in schedule_data.items():
            date_string = self.__format_date_str_prettify(dateStr)
            final_write_str += f'<- Games on {date_string} analysis ->\n'
            final_write_str += f'If <Historical Prediction Accuracy> fields = -1:\n\t-> historic matches were not recorded...\n'
            for match in matches:
                t1 = match[0]
                at_vs = match[1]
                t2 = match[2]
                final_write_str += f'\n{t1} {at_vs} {t2}\n'
                matchHist_odds_arr = self.analysis_module.AnalyzeMatchHist(t1, at_vs, t2, False).return_odds()
                accuracyEst_odds_arr = self.analysis_module.AccuracyEstimate(t1, at_vs, t2, False).return_odds()
                prevWinner_odds_arr = self.analysis_module.PrevWinner(t1, at_vs, t2, False).return_odds()
                winstreak_arr = matchHist_odds_arr[2]
                final_write_str += f'\t<-> Analyze Match History Prediction <->\n'
                final_write_str += f'\t{t1}: {matchHist_odds_arr[0]:.2f}% | {t2}: {matchHist_odds_arr[1]:.2f}%\n'
                final_write_str += f'\t<-> Current Win Streaks <->\n'
                final_write_str += f'\t{t1}: {winstreak_arr[0]:.0f} | {t2}: {winstreak_arr[1]:.0f}\n'
                final_write_str += f'\t<-> Prediction Accuracy Estimate <->\n'
                final_write_str += f'\t{t1}: {accuracyEst_odds_arr[0]:.2f} | {t2}: {accuracyEst_odds_arr[1]:.2f}\n'
                final_write_str += f'\t<-> Historical Prediction Accuracy (of this game) <->\n'
                final_write_str += f'\t{t1}: {prevWinner_odds_arr[0]:.2f}% | {t2}: {prevWinner_odds_arr[1]:.2f}%\n\n'
        final_write_str += f'<>'
        if print_yes_no == True:
            print(final_write_str)
        if file_yes_no == True:
            with open(file_name, 'w') as f:
                f.write(final_write_str)