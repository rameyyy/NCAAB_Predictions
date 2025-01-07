from . import commonFunctions

class PointPrediction:
    def __init__(self, team1:str, at_or_vs:str, team2:str):
        self.commonFuncObj = commonFunctions.CommonFunctions()
        self.run_the_numbers(team1, at_or_vs, team2)

    def get_individual_data(self, team1, team2):
        paths_arr = self.commonFuncObj.get_path()
        file_path = paths_arr[0]
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
        check_4 = teams_arr_len-4
        loop_range = 0
        if check_4 == -4: #no matches recorded
            return None
        elif check_4 < 0: #less than 4 matches recorded
            loop_range = abs(check_4)
        else:
            loop_range = 4
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
    
    def get_sorted_rank_list(self, teams_data, target_rank):
        data = teams_data.copy()
        rank = data.pop('Rank', None)
        rank = int(rank)
        data.pop('team_name', None)
        match_arr = []
        rank_arr = []
        for match, match_data in data.items():
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
            else:
                data = team2_data.copy()    # Create a copy of the data to work with
                target_rank = team1_data.get('Rank')
            rank = data.pop('Rank', None)
            rank = int(rank)
            data.pop('team_name', None)
            match_arr = []
            rank_arr = []
            for match, match_data in data.items():
                match_arr.append(match)
                op_rank = match_data.get("Rank")
                if op_rank == None:
                    op_rank = self.commonFuncObj.get_lowest_rank()
                rank_arr.append(op_rank)          
            sorted_rank_list = self.__sort_team_closest_rank(match_arr, rank_arr, target_rank)
            return_result = self.__analyze_closest_matchups(data, sorted_rank_list)
            if i == 0:
                t1_point_avg = return_result
            else:
                t2_point_avg = return_result
        t1_points = (t1_point_avg[0] + t2_point_avg[1]) / 2
        t2_points = (t1_point_avg[1] + t2_point_avg[0]) / 2
        return t1_points, t2_points
    
    def TS_and_PlayerMinutes(self, team1_data, team2_data):
        target_ranking = team2_data.get("Rank")
        team_name = team1_data.get('team_name')
        paths_arr = self.commonFuncObj.get_path()
        dataset = self.commonFuncObj.load_json_file(paths_arr[3])
        sorted_rank_list = self.get_sorted_rank_list(team1_data, target_ranking)
        if len(sorted_rank_list) < 4:
            return None
        else:
            for i in range(0, 4):
                match = f'{team_name}-{sorted_rank_list[i]}'
                print(match)
                matchup_data = self.commonFuncObj.get_player_matchup_data(dataset, match)
                for team, players in matchup_data.items():
                    for player, players_stats in players.items():
                        minutes = players_stats.get('Min')
                        points = players_stats.get('Pts')
                        print(f'{player}, pts: {points}, mins: {minutes}')

    def run_the_numbers(self, team1, at_or_vs, team2):
        team1_data, team2_data = self.get_individual_data(team1, team2)
        match_hist_score = self.check_match_history(team1_data, team2_data)
        print(f'{team1}: {match_hist_score[0]} | {team2}: {match_hist_score[1]}')
        self.TS_and_PlayerMinutes(team1_data, team2_data)
        # hna_score = self.hna_check(at_or_vs)
        # scores = self.add_points(trank_score, match_hist_score, hna_score)
        # data1 = (scores[0] / (scores[0] + scores[1])) * 100
        # data2 = (scores[1] / (scores[0] + scores[1])) * 100
        # if data1 > data2:
        #     print(f'{team1}, W, {data1:.2f}% | {team2}, L, {data2:.2f}%')
        # else:
        #     print(f'{team1}, L, {data1:.2f}% | {team2}, W, {data2:.2f}%')