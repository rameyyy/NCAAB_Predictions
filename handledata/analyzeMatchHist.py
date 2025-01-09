from . import commonFunctions

class AnalyzeMatchHist:
    def __init__(self, team1:str, at_or_vs:str, team2:str, ignore_data_bool:bool):
        self.commonFuncObj = commonFunctions.CommonFunctions()
        self.ignore_data_boolean = ignore_data_bool
        self.match_info_arr = [team1, at_or_vs, team2]
        # self.run_the_numbers(team1, at_or_vs, team2)
        
    def get_path(self):
        from . import get_paths
        paths_arr = get_paths()
        return paths_arr

    def get_individual_data(self, team1, team2):
        file_path_arr = self.get_path()
        file_path = file_path_arr[0]
        dataset = self.commonFuncObj.load_json_file(file_path)
        team1_data = self.commonFuncObj.get_team_data(data_set=dataset, team_name=team1)
        team2_data = self.commonFuncObj.get_team_data(data_set=dataset, team_name=team2)
        return team1_data, team2_data
    
    def check_match_history(self, team1_data, team2_data):
        total_ranked = self.commonFuncObj.get_lowest_rank()
        for i in range(0, 2):
            if i == 0:
                data = team1_data.copy()    # Create a copy of the data to work with
                ops_team_name = team2_data.get('team_name')
            else:
                data = team2_data.copy()    # Create a copy of the data to work with
                ops_team_name = team1_data.get('team_name')
            data.pop('Rank', None)
            data.pop('team_name', None)
            match_score = 0
            match_count = 0
            for key, items in data.items():
                if self.ignore_data_boolean != True:
                    ops_rank = items.get("Rank")
                    ops_diff = items.get("Diff")
                    if ops_rank == None:
                        ops_rank = self.commonFuncObj.get_lowest_rank()
                    x = (ops_rank/ops_diff/total_ranked)
                    if ops_diff < 0:
                        x = (ops_rank/total_ranked) * (ops_diff * -1)
                    else:
                        x = (ops_rank/total_ranked) / ops_diff
                    x *= 100
                    match_score += x
                    match_count += 1
                else:
                    if key == ops_team_name:
                        pass
                    else:
                        ops_rank = items.get("Rank")
                        ops_diff = items.get("Diff")
                        if ops_rank == None:
                            ops_rank = self.commonFuncObj.get_lowest_rank()
                        x = (ops_rank/ops_diff/total_ranked)
                        if ops_diff < 0:
                            x = (ops_rank/total_ranked) * (ops_diff * -1)
                        else:
                            x = (ops_rank/total_ranked) / ops_diff
                        x *= 100
                        match_score += x
                        match_count += 1
            avg_match_score = match_score / match_count
            if i == 0:
                match_score_t1 = match_score
                match_count_t1 = match_count
                avg_match_score_t1 = avg_match_score
            else:
                match_score_t2 = match_score
                match_count_t2 = match_count
                avg_match_score_t2 = avg_match_score
        match_difference = match_count_t1 - match_count_t2
        if match_difference > 0:
            match_score_t1 -= avg_match_score_t1*match_difference
        elif match_difference < 0:
            match_score_t2 -= avg_match_score_t2*match_difference
        
        total_match_score = match_score_t2 + match_score_t1
        winr_t1 = match_score_t2 / total_match_score
        winr_t2 = match_score_t1 / total_match_score
        return winr_t1, winr_t2
    
    def hna_check(self, at_vs:str):
        # if at, then that team is home and gets 100% of home/away pts
         # else neither team gets points
        if at_vs == 'at':
            return 0, 1
        else:
            return 0, 0
    
    def trank_comparison(self, team1_datas, team2_datas):
        lowest_ranked = self.commonFuncObj.get_lowest_rank()
        t1_rank =team1_datas.get('Rank')
        t2_rank =team2_datas.get('Rank')
        t1 = t1_rank/lowest_ranked
        t2 = t2_rank/lowest_ranked
        t1_prcnt = t2 / (t1 + t2)
        t2_prcnt = t1 / (t1 + t2)
        return t1_prcnt, t2_prcnt

    def add_points(self, trank_scores, match_hist_scores, hna_scores):
        t1_total = 0
        t2_total = 0
        for i in range(0, 2):
            if i % 2 == 0:
                t1_total += (trank_scores[i] * self.commonFuncObj.get_function_weight('AnalyzeMatchHist', 'TRank'))
                t1_total += (match_hist_scores[i] * self.commonFuncObj.get_function_weight('AnalyzeMatchHist', 'MatchHist'))
                t1_total += (hna_scores[i] * self.commonFuncObj.get_function_weight('AnalyzeMatchHist', 'HomeAway'))
            else:
                t2_total += (trank_scores[i] * self.commonFuncObj.get_function_weight('AnalyzeMatchHist', 'TRank'))
                t2_total += (match_hist_scores[i] * self.commonFuncObj.get_function_weight('AnalyzeMatchHist', 'MatchHist'))
                t2_total += (hna_scores[i] * self.commonFuncObj.get_function_weight('AnalyzeMatchHist', 'HomeAway'))
        return t1_total, t2_total

    def return_odds(self):
        team1 = self.match_info_arr[0]
        at_vs = self.match_info_arr[1]
        team2 = self.match_info_arr[2]
        t1_odds, t2_odds = self.run_the_numbers(team1, at_vs, team2)
        return t1_odds, t2_odds

    def run_the_numbers(self, team1, at_or_vs, team2):
        team1_data, team2_data = self.get_individual_data(team1, team2)
        match_hist_score = self.check_match_history(team1_data, team2_data)
        trank_score = self.trank_comparison(team1_data, team2_data)
        hna_score = self.hna_check(at_or_vs)
        scores = self.add_points(trank_score, match_hist_score, hna_score)
        data1 = (scores[0] / (scores[0] + scores[1])) * 100
        data2 = (scores[1] / (scores[0] + scores[1])) * 100
        # if data1 > data2:
        #     print(f'{team1}, W, {data1:.2f}% | {team2}, L, {data2:.2f}%')
        # else:
        #     print(f'{team1}, L, {data1:.2f}% | {team2}, W, {data2:.2f}%')
        return data1, data2