from . import commonFunctions

class AccuracyEstimate:
    def __init__(self, team1:str, at_or_vs:str, team2:str, ignore_data_bool:bool):
        self.commonFuncObj = commonFunctions.CommonFunctions()
        self.ignore_data_boolean = ignore_data_bool
        self.match_info_arr = [team1, at_or_vs, team2]
    
    def get_individual_data(self, team1, team2):
        dateStr = self.commonFuncObj.get_formatted_date()
        yearStr = self.commonFuncObj.get_ncaa_season_year(dateStr)
        file_path = self.commonFuncObj.adjust_matchHist_file_path(yearStr)
        dataset = self.commonFuncObj.load_json_file(file_path)
        team1_data = self.commonFuncObj.get_team_data(data_set=dataset, team_name=team1)
        team2_data = self.commonFuncObj.get_team_data(data_set=dataset, team_name=team2)
        return team1_data, team2_data
    
    def get_ordered_ops_list(self, t1_data, t2_data):
        t2_name = t2_data.get('team_name')
        t2_rank = t2_data.get('Rank')
        t1_name = t1_data.get('team_name')
        t1_rank = t1_data.get('Rank')
        t1_list = self.commonFuncObj.get_sorted_rank_list(t1_data, t2_rank, t2_name, self.ignore_data_boolean)
        t2_list = self.commonFuncObj.get_sorted_rank_list(t2_data, t1_rank, t1_name, self.ignore_data_boolean)
        return t1_list, t2_list, t1_rank, t2_rank
    
    def accuracy_estimator(self, team_arr, ops_rank):
        dateStr = self.commonFuncObj.get_formatted_date()
        yearStr = self.commonFuncObj.get_ncaa_season_year(dateStr)
        adjusted_path = self.commonFuncObj.adjust_leaderboard_file_path(yearStr)
        leaderboard_json = self.commonFuncObj.load_json_file(adjusted_path)
        if len(team_arr) > 3:
            top4_array = team_arr[:4]
        else:
            return None
        rank_arr = []
        for team in leaderboard_json:
            if team['team_name'] in top4_array:
                teams_rank = team['Rank']
                rank_arr.append(teams_rank)
        rank_arr_len = len(rank_arr)
        if rank_arr_len != 4:
            lowest_rank_in_league = self.commonFuncObj.get_lowest_rank() + 51
            for i in range(0, 4):
                try:
                    test = rank_arr[i]
                except Exception:
                    rank_arr.append(lowest_rank_in_league)
        rank_avg = sum(rank_arr) / len(rank_arr)
        range_avg = rank_avg - ops_rank
        return range_avg
    
    def return_odds(self):
        t1 = self.match_info_arr[0]
        t2 = self.match_info_arr[2]
        at_vs = self.match_info_arr[1]
        t1_data, t2_data = self.get_individual_data(t1, t2)
        ordered_lists = self.get_ordered_ops_list(t1_data, t2_data)
        t1_list, t2_list, t1_rank, t2_rank = ordered_lists[0], ordered_lists[1], ordered_lists[2], ordered_lists[3]
        t1_range = self.accuracy_estimator(t1_list, t2_rank)
        t2_range = self.accuracy_estimator(t2_list, t1_rank)
        return t1_range, t2_range