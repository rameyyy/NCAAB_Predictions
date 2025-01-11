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
    
    def __point_analysis(self, points_arr):
        t1_points = int(points_arr[0])
        t2_points = int(points_arr[1])
        t1_prcnt = t1_points / (t1_points + t2_points)
        t2_prcnt = t2_points / (t1_points + t2_points)
        arr = [t1_prcnt, t2_prcnt]
        return arr
    
    def determine_bet_safety_rating(self, accuracy_est_arr, analyze_matchhist_arr, prevWinner_arr):
        t1_wins_bool_amh = False
        t1_wins_bool_prev = False
        risk_value = accuracy_est_arr[0] + accuracy_est_arr[1]
        if analyze_matchhist_arr[0] > analyze_matchhist_arr[1]:
            t1_wins_bool_amh = True
        if prevWinner_arr[0] > prevWinner_arr[1]:
            t1_wins_bool_prev = True
        if t1_wins_bool_prev == t1_wins_bool_amh:
            if risk_value > 2:
                return_string = f'\t<-> Highly Safe Bet (PL)\n'
            else:
                return_string = f'\t<-> Very Safe Bet (ML)\n'
        else:
            return_string = f'\t<-> Risky Bet\n'
        return return_string
    
    def prev_winner_str(self, winners_arr):
        return_string = f'\t\t-> {winners_arr[0]}: '
        except_count = 0
        del winners_arr[0]
        for data in winners_arr:
            try:
                test = int(data)
                return_string += f' | {data}: '
                except_count = 0
            except Exception:
                if except_count == 0:
                    return_string += f'{data}'
                else:
                    return_string += f', {data}'
                except_count += 1
        return_string += '\n\n'
        return return_string
    
    def calculate_run_time(self, start_time, final_print:bool):
        if final_print != True:
            elapsed_time = time.time() - start_time
            mins, secs = divmod(elapsed_time, 60)
            print(f"\rElapsed time: {mins:.0f} minutes, {secs:.2f} seconds", end="", flush=True)
        else:
            final_time = time.time() - start_time
            mins_final, secs_final = divmod(final_time, 60)
            print(f'\nFinished in {mins_final:.0f} minutes, {secs_final:.2f} seconds.')
    
    def generate_report(self, print_yes_no:bool, file_yes_no:bool, file_name:str, ignore_point_predict:bool):
        paths_arr = self.commonFuncs.get_path()
        path_to_schedule = paths_arr[2]
        schedule_data = self.commonFuncs.load_json_file(path_to_schedule)
        final_write_str = ''
        start_time = time.time()
        for dateStr, matches in schedule_data.items():
            self.calculate_run_time(start_time, False)
            date_string = self.__format_date_str_prettify(dateStr)
            final_write_str += f'<- Games on {date_string} analysis ->\n'
            final_write_str += f'If <Historical Prediction Accuracy> fields = -1:\n\t-> historic matches were not recorded...\n'
            for match in matches:
                t1 = match[0]
                at_vs = match[1]
                t2 = match[2]
                final_write_str += f'\n{t1} {at_vs} {t2}\n'
                self.calculate_run_time(start_time, False)
                matchHist_odds_arr = self.analysis_module.AnalyzeMatchHist(t1, at_vs, t2, False).return_odds()
                accuracyEst_odds_arr = self.analysis_module.AccuracyEstimate(t1, at_vs, t2, False).return_odds()
                prevWinner_arr = self.analysis_module.PrevWinner(t1, at_vs, t2, False).return_odds()
                prevWinner_odds_arr = prevWinner_arr[0]
                prevWinners_str_arr = prevWinner_arr[1]
                if ignore_point_predict != True:
                    pointPrediction_arr = self.analysis_module.PointPrediction(t1, at_vs, t2, False).return_odds()
                winstreak_arr = matchHist_odds_arr[2]
                safe_bet_string = self.determine_bet_safety_rating(accuracyEst_odds_arr, matchHist_odds_arr, prevWinner_odds_arr)
                final_write_str += safe_bet_string
                final_write_str += f'\t<-> Analyze Match History Prediction -> '
                final_write_str += f'\t{t1}: {matchHist_odds_arr[0]:.2f}% | {t2}: {matchHist_odds_arr[1]:.2f}%\n'
                if ignore_point_predict != True:
                    if pointPrediction_arr == 'Fail':
                        pointPrediction_arr = [-1, -1]
                    point_prcnt_arr = self.__point_analysis(pointPrediction_arr)
                    final_write_str += f'\t<-> Point Prediction Model -> '
                    final_write_str += f'{t1}: {point_prcnt_arr[0]*100:.2f}% | {t2}: {point_prcnt_arr[1]*100:.2f}%\n'
                    final_write_str += f'\t<-> Point Prediction -> '
                    final_write_str += f'{t1}: {pointPrediction_arr[0]:.0f} | {t2}: {pointPrediction_arr[1]:.0f}\n'
                final_write_str += f'\t<-> Current Win Streaks -> '
                final_write_str += f'\t\t\t\t\t{t1}: {winstreak_arr[0]:.0f} | {t2}: {winstreak_arr[1]:.0f}\n'
                final_write_str += f'\t<-> Prediction Accuracy Estimate -> '
                risk_value = accuracyEst_odds_arr[0] + accuracyEst_odds_arr[1]
                final_write_str += f'\t\t{t1}: {accuracyEst_odds_arr[0]:.2f} | {t2}: {accuracyEst_odds_arr[1]:.2f} | Risk Val: {risk_value:.2f}\n'
                final_write_str += f'\t<-> Historical Prediction Accuracy and Previous Years Winners <->\n'
                final_write_str += f'\t\t-> {t1}: {prevWinner_odds_arr[0]:.2f}% | {t2}: {prevWinner_odds_arr[1]:.2f}%\n'
                final_write_str += self.prev_winner_str(prevWinners_str_arr)
        final_write_str += f'<>'
        if print_yes_no == True:
            print(final_write_str)
        if file_yes_no == True:
            with open(file_name, 'w') as f:
                f.write(final_write_str)
        self.calculate_run_time(start_time, True)