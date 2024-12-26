try:
    from . import common_functions
except Exception:
    pass
try:
    import common_functions
except Exception:
    pass

class PointPrediction:
    def __init__(self, team1:str, at_or_vs:str, team2:str):
        self.run_the_numbers(team1, at_or_vs, team2)

    def get_individual_data(self, team1, team2):
        cf = common_functions.GrabData()
        dataset = cf.load_json_file('data/individual_data.json')
        team1_data = cf.get_team_data(data_set=dataset, team_name=team1)
        team2_data = cf.get_team_data(data_set=dataset, team_name=team2)
        return team1_data, team2_data
    
    def __sort_team_closest_rank(self, teams_arr, ranks_arr, target_rank):
        team_rank_dict = dict(zip(teams_arr, ranks_arr))
        sorted_team_rank_items = sorted(team_rank_dict.items(), key=lambda item: abs(item[1] - target_rank))
        sorted_teams = [teams_arr for teams_arr, ranks_arr in sorted_team_rank_items]
        return sorted_teams
    
    def __analyze_closest_matchups(self, teams_data, teams_arr):
        teams_arr_len = len(teams_arr)
        check_4 = teams_arr_len-4
        loop_range = 0
        if check_4 == -4: #no matches recorded
            return None
        elif check_4 < 0: #less than 3 matches recorded
            loop_range = abs(check_4)
        else:
            loop_range = 4
        team_scored = 0
        op_scored = 0
        for i in range(0, loop_range):
            for match, match_data in teams_data.items():
                if match == teams_arr[i]:
                    win_loss = match_data[3]
                    points = match_data[4]
                    if win_loss == 1:
                        team_scored += points[0]
                        op_scored += points[1]
                    else:
                        team_scored += points[1]
                        op_scored += points[0]
        team_scored_avg = team_scored / loop_range
        op_scored_avg = op_scored / loop_range
        print(team_scored_avg, op_scored_avg)    
    
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
                op_rank = match_data[0]
                if op_rank == None:
                    op_rank = 365
                rank_arr.append(op_rank)          
            sorted_rank_list = self.__sort_team_closest_rank(match_arr, rank_arr, target_rank)
            self.__analyze_closest_matchups(data, sorted_rank_list)
    
    def hna_check(self, at_vs:str):
        # if at, then that team is home and gets 100% of home/away pts
         # else neither team gets points
        if at_vs == 'at':
            return 0, 1
        else:
            return 0, 0

    def add_points(self, trank_scores, match_hist_scores, hna_scores):
        t1_total = 0
        t2_total = 0
        for i in range(0, 2):
            if i % 2 == 0:
                t1_total += (trank_scores[i] * 3.5)
                t1_total += (match_hist_scores[i] * 20)
                t1_total += (hna_scores[i] * .8)
            else:
                t2_total += (trank_scores[i] * 3.5)
                t2_total += (match_hist_scores[i] * 20)
                t2_total += (hna_scores[i] * .8)
        return t1_total, t2_total

    def run_the_numbers(self, team1, at_or_vs, team2):
        team1_data, team2_data = self.get_individual_data(team1, team2)
        match_hist_score = self.check_match_history(team1_data, team2_data)
        # hna_score = self.hna_check(at_or_vs)
        # scores = self.add_points(trank_score, match_hist_score, hna_score)
        # data1 = (scores[0] / (scores[0] + scores[1])) * 100
        # data2 = (scores[1] / (scores[0] + scores[1])) * 100
        # if data1 > data2:
        #     print(f'{team1}, W, {data1:.2f}% | {team2}, L, {data2:.2f}%')
        # else:
        #     print(f'{team1}, L, {data1:.2f}% | {team2}, W, {data2:.2f}%')