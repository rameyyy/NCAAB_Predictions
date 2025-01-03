from . import common_functions

class MatchFirst500:
    def __init__(self, team1:str, at_or_vs:str, team2:str):
        self.run_the_numbers(team1, at_or_vs, team2)


    def get_individual_data(self, team1, team2):
        cf = common_functions.GrabData()
        dataset = cf.load_json_file('database/individual_data.json')
        team1_data = cf.get_team_data(data_set=dataset, team_name=team1)
        team2_data = cf.get_team_data(data_set=dataset, team_name=team2)
        return team1_data, team2_data
    
    def check_match_history(self, team1_data, team2_data):
        for i in range(0, 2):
            if i == 0:
                data = team1_data.copy()    # Create a copy of the data to work with
            else:
                data = team2_data.copy()    # Create a copy of the data to work with
            rank = data.pop('Rank', None)
            data.pop('team_name', None)
            match_score = 0
            match_count = 0
            for match, match_data in data.items():
                ops_rank = match_data[0]
                ops_diff = match_data[5]
                if ops_rank is None:
                    ops_rank = 365

                x = (ops_rank/ops_diff/364)
                if x < 0:
                    x = x*-1.5
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
        t1_rank =team1_datas.get('Rank')
        t2_rank =team2_datas.get('Rank')
        t1 = t1_rank/364
        t2 = t2_rank/364
        t1_prcnt = t2 / (t1 + t2)
        t2_prcnt = t1 / (t1 + t2)
        return t1_prcnt, t2_prcnt

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
        trank_score = self.trank_comparison(team1_data, team2_data)
        hna_score = self.hna_check(at_or_vs)
        scores = self.add_points(trank_score, match_hist_score, hna_score)
        data1 = (scores[0] / (scores[0] + scores[1])) * 100
        data2 = (scores[1] / (scores[0] + scores[1])) * 100
        if data1 > data2:
            print(f'{team1}, W, {data1:.2f}% | {team2}, L, {data2:.2f}%')
        else:
            print(f'{team1}, L, {data1:.2f}% | {team2}, W, {data2:.2f}%')