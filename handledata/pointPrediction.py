from . import commonFunctions

class PointPrediction:
    def __init__(self, team1:str, at_or_vs:str, team2:str, ignore_data_bool:bool):
        self.commonFuncObj = commonFunctions.CommonFunctions()
        self.ignore_data_boolean = ignore_data_bool
        self.match_info_arr = [team1, at_or_vs, team2]
        # self.run_the_numbers(team1, at_or_vs, team2)

    def get_individual_data(self, team1, team2):
        dateStr = self.commonFuncObj.get_formatted_date()
        yearStr = self.commonFuncObj.get_ncaa_season_year(dateStr)
        file_path = self.commonFuncObj.adjust_matchHist_file_path(yearStr)
        dataset = self.commonFuncObj.load_json_file(file_path)
        team1_data = self.commonFuncObj.get_team_data(data_set=dataset, team_name=team1)
        team2_data = self.commonFuncObj.get_team_data(data_set=dataset, team_name=team2)
        return team1_data, team2_data
    
    def __sort_team_closest_rank(self, teams_arr, ranks_arr, target_rank):
        team_rank_dict = list(zip(teams_arr, ranks_arr))
        team_rank_dict.sort(key=lambda x: abs(x[1] - target_rank))
        sorted_teams, sorted_ranks = zip(*team_rank_dict)
        return list(sorted_teams)
    
    def __analyze_closest_matchups(self, teams_data, teams_arr):
        teams_arr_len = len(teams_arr)
        check_val = self.commonFuncObj.get_function_weight('PointPrediction', 'SimilarMatch_PtAverages_loop')
        check_ = teams_arr_len-check_val
        loop_range = 0
        check_val *= -1
        if check_ == check_val: #no matches recorded
            return None
        elif check_ < 0: #less than 4 matches recorded
            loop_range = abs(check_)
        else:
            check_val *= -1
            loop_range = check_val
        team_scored = 0
        op_scored = 0
        for i in range(0, loop_range):
            for match, match_data in teams_data.items():
                if match == teams_arr[i]:
                    win_loss = match_data.get("W/L")
                    points = match_data.get("Score")
                    if win_loss == 1:
                        team_scored += points[0]
                        op_scored += points[1]
                    else:
                        team_scored += points[1]
                        op_scored += points[0]
        team_scored_avg = team_scored / loop_range
        op_scored_avg = op_scored / loop_range
        return team_scored_avg, op_scored_avg 
    
    def get_sorted_rank_list(self, teams_data, target_rank, ops_team_name):
        data = teams_data.copy()
        rank = data.pop('Rank', None)
        data.pop('team_name', None)
        rank = int(rank)
        match_arr = []
        rank_arr = []
        for match, match_data in data.items():
            if self.ignore_data_boolean == True:
                if match != ops_team_name:
                    match_arr.append(match)
                    op_rank = match_data.get("Rank")
                    if op_rank == None:
                        op_rank = self.commonFuncObj.get_lowest_rank()
                    rank_arr.append(op_rank)
            else:
                match_arr.append(match)
                op_rank = match_data.get("Rank")
                if op_rank == None:
                    op_rank = self.commonFuncObj.get_lowest_rank()
                rank_arr.append(op_rank)     
        sorted_rank_list = self.__sort_team_closest_rank(match_arr, rank_arr, target_rank)
        return sorted_rank_list
    
    def check_match_history(self, team1_data, team2_data):
        for i in range(0, 2):
            team_and_rank = {}
            if i == 0:
                data = team1_data.copy()    # Create a copy of the data to work with
                target_rank = team2_data.get('Rank')
                ops_team_name = team2_data.get("team_name")
            else:
                data = team2_data.copy()    # Create a copy of the data to work with
                target_rank = team1_data.get('Rank')
                ops_team_name = team1_data.get("team_name")         
            sorted_rank_list = self.get_sorted_rank_list(data, target_rank, ops_team_name)
            return_result = self.__analyze_closest_matchups(data, sorted_rank_list)
            if i == 0:
                t1_point_avg = return_result
            else:
                t2_point_avg = return_result
        t1_points = (t1_point_avg[0] + t2_point_avg[1]) / 2
        t2_points = (t1_point_avg[1] + t2_point_avg[0]) / 2
        return t1_points, t2_points
    
    def hna_check(self, at_vs:str):
        # if at, then that team is home and gets 100% of home/away pts
         # else neither team gets points
        HNA_value = self.commonFuncObj.get_function_weight("PointPrediction", "HNA")
        if at_vs == 'at':
            return 0, HNA_value
        else:
            return 0, 0
    
    def __loop_player_min_pts_stats(self, stats_dict, surplus):
        total_time = 0
        points = 0
        player_count = 0
        for player, data in stats_dict.items():
            if data[0] != 0:
                ppm = data[1] / data[0] # points/minutes = points per min
                min_per_game = data[0]/data[2] - surplus
                points += (ppm * min_per_game)
                total_time += min_per_game
                player_count += 1
        arr = [float(points), float(total_time), float(player_count)]
        return arr
    
    def TS_and_PlayerMinutes(self, team1_data, team2_data):
        target_ranking = team2_data.get("Rank")
        team_name = team1_data.get('team_name')
        ops_team_name = team2_data.get('team_name')
        paths_arr = self.commonFuncObj.get_path()
        dataset = self.commonFuncObj.load_json_file(paths_arr[3])
        sorted_rank_list = self.get_sorted_rank_list(team1_data, target_ranking, ops_team_name)
        player_stats_dict = {}
        loop_val = self.commonFuncObj.get_function_weight('PointPrediction', 'PlayerMin_PtAvgs_loop')
        if len(sorted_rank_list) < loop_val:
            return None
        else:
            for i in range(0, loop_val):
                match = f'{team_name}-{sorted_rank_list[i]}'
                matchup_data = self.commonFuncObj.get_player_matchup_data(dataset, match)
                for team, players in matchup_data.items():
                    if team == team_name:
                        for player, players_stats in players.items():
                            minutes = int(players_stats.get('Min'))
                            points = int(players_stats.get('Pts'))
                            if player != 'Totals':
                                if not player_stats_dict:
                                    player_stats_dict[player] = [minutes, points, 1]
                                elif player in player_stats_dict:
                                    player_arr = player_stats_dict[player]
                                    player_arr[0] += minutes
                                    player_arr[1] += points
                                    player_arr[2] += 1 #another game played
                                else:
                                    player_stats_dict[player] = [minutes, points, 1]
        arr = self.__loop_player_min_pts_stats(player_stats_dict, 0)
            # print(f'{player}, {ppm:.2f}, mins play avg: {min_per_game}')
        if (arr[1] > 200.0 or arr[1] < 200.0) and arr[2] != 0: #200 minutes total per game possible adding up all players times
            surplus = (arr[1] - 200.0)
            surplus /= arr[2]
            new_arr = self.__loop_player_min_pts_stats(player_stats_dict, surplus)
        try:
            points = new_arr[0]
            return points
        except Exception:
            return 'Brick'
    
    def calculate_points_final(self, hna, pts1, pts2):
        # weight_pts1 = self.commonFuncObj.get_function_weight('PointPrediction', 'PlayerMin_PtAvgs')
        weight_pts2 = self.commonFuncObj.get_function_weight('PointPrediction', 'SimilarMatch_PtAverages')
        weight_pts1 /= 100
        weight_pts2 /= 100
        points = [0, 0]
        for i in range(0, 2):
            points[i] += (pts1[i] * weight_pts1)
            points[i] += (pts2[i] * weight_pts2)
        points[1] += hna[1]
        return points

    def return_odds(self):
        team1 = self.match_info_arr[0]
        at_vs = self.match_info_arr[1]
        team2 = self.match_info_arr[2]
        odds_arr = self.run_the_numbers(team1, at_vs, team2)
        return odds_arr
    
    def run_the_numbers(self, team1, at_or_vs, team2):
        team1_data, team2_data = self.get_individual_data(team1, team2)
        match_hist_score = self.check_match_history(team1_data, team2_data)
        hna_score = self.hna_check(at_or_vs)
        # print(f'{team1}: {match_hist_score[0]} | {team2}: {match_hist_score[1] + hna_score[1]}')
        t1_playerMinutes_score = self.TS_and_PlayerMinutes(team1_data, team2_data)
        t2_playerMinutes_score = self.TS_and_PlayerMinutes(team2_data, team1_data)
        if t1_playerMinutes_score == 'Brick' or t2_playerMinutes_score == 'Brick':
            return 'Fail'
        playerMin_score_arr = [t1_playerMinutes_score, t2_playerMinutes_score]
        t2_playerMinutes_score += hna_score[1]
        # print(f'{team1}: {t1_playerMinutes_score:.2f} | {team2}: {t2_playerMinutes_score:.2f}')
        pts = self.calculate_points_final(hna_score, playerMin_score_arr, match_hist_score)
        # print(f'{team1}: {pts[0]:.2f} | {team2}: {pts[1]:.2f}')
        return pts