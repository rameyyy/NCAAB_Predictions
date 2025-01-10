from . import commonFunctions

class PrevWinner:
    def __init__(self, team1:str, at_or_vs:str, team2:str, ignore_data_bool:bool):
        self.commonFuncObj = commonFunctions.CommonFunctions()
        self.match_info_arr = [team1, at_or_vs, team2]
        self.ignore_data = ignore_data_bool
    
    def get_individual_data(self, team1, team2, file_path):
        dataset = self.commonFuncObj.load_json_file(file_path)
        team1_data = self.commonFuncObj.get_team_data(data_set=dataset, team_name=team1)
        team2_data = self.commonFuncObj.get_team_data(data_set=dataset, team_name=team2)
        return team1_data, team2_data
    
    def analyze_old_matchHist(self, t1_data, t2_data):
        file_path_arr = self.commonFuncObj.get_path()
        file_path_ = file_path_arr[7]
        from . import analyzeMatchHist
        AnalyzeMatchHistObj = analyzeMatchHist.AnalyzeMatchHist(self.match_info_arr[0], self.match_info_arr[1], self.match_info_arr[2], True)
        odds_arr = AnalyzeMatchHistObj.check_match_history(t1_data, t2_data)
        data1 = odds_arr[0]
        data2 = odds_arr[1]
        data1 *= 100
        data2 *= 100
        return data1, data2
    
    def win_or_lose(self, teams_data, ops_name):
        data = teams_data.copy()
        data.pop('team_name', None)
        data.pop('Rank', None)
        match_count = 0
        win_loss = 0
        for op, stats in data.items():
            if ops_name == op:
                who_won = stats.get('W/L')
                who_won = int(who_won)
                match_count += 1
                win_loss += who_won
        if match_count == 0:
            return -1
        winPercent = float(win_loss) / float(match_count)
        return winPercent
    
    # the higher the number for a team the more likely they will win based on previous year matchups
    def the_math(self, win_prcnt_arr, odds_arr, year_index, teams_value):
        if year_index == 0:
            x = self.commonFuncObj.get_function_weight('prevWinner', 'currentYear')
        elif year_index == 1:
            x = self.commonFuncObj.get_function_weight('prevWinner', 'prevYear')
        else:
            x = self.commonFuncObj.get_function_weight('prevWinner', 'prevPrevYear')
        t1_value = win_prcnt_arr[0] * odds_arr[0] * x
        t2_value = win_prcnt_arr[1] * odds_arr[1] * x
        teams_value[0] = teams_value[0] + t1_value
        teams_value[1] = teams_value[1] + t2_value
        return teams_value
    
    def return_odds(self):
        t1 = self.match_info_arr[0]
        t2 = self.match_info_arr[2]
        todays_date = self.commonFuncObj.get_formatted_date()
        current_NCAA_year_str = self.commonFuncObj.get_ncaa_season_year(todays_date)
        current_NCAA_year_int = int(current_NCAA_year_str)
        teams_value = [0, 0]
        if self.ignore_data == True:
            loop_var_first = current_NCAA_year_int - 2
            loop_var_second = current_NCAA_year_int
        else:
            loop_var_first = current_NCAA_year_int - 2
            loop_var_second = current_NCAA_year_int + 1
        try:
            for i in range(loop_var_first, loop_var_second):
                current_NCAA_year_str = str(i)
                file_path = self.commonFuncObj.adjust_matchHist_file_path(current_NCAA_year_str)
                t1_old_data, t2_old_data = self.get_individual_data(t1, t2, file_path)
                odds_arr = self.analyze_old_matchHist(t1_old_data, t2_old_data)
                t1_win_percent = self.win_or_lose(t1_old_data, t2)
                t2_win_percent = self.win_or_lose(t2_old_data, t1)
                if t1_win_percent < 0 or t2_win_percent < 0:
                    pass
                else:
                    win_percent_arr = [t1_win_percent, t2_win_percent]
                    teams_value = self.the_math(win_percent_arr, odds_arr, i, teams_value)
            if teams_value[0] == 0 and teams_value[1] == 0:
                return [-1, -1]
            else:
                t1_value = teams_value[0]
                t2_value = teams_value[1]
                t1_value_percent = (t1_value / (t1_value + t2_value)) * 100
                t2_value_percent = (t2_value / (t1_value + t2_value)) * 100
                arr = [t1_value_percent, t2_value_percent]
                return arr
        except Exception as e:
            return [-1, -1]