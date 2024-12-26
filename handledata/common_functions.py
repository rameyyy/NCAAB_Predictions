import json
from datetime import datetime

class GrabData:
    def __init__(self):
        pass

    def load_json_file(self, path):
        with open(path, 'r') as f:
            data = json.load(f)
        return data

    def get_team_data(self, data_set, team_name): 
        for data in data_set:
            if data['team_name'] == team_name:
                return data
        print(f"Could not find team '{team_name}' in the dataset")
        return None

    def get_schedule_data(self, data_set, date_key): 
        matchups = data_set.get(date_key, [])
        return matchups
    
    def get_ncaa_season_year(self, date_str): 
        # Parse the input date string 
        date = datetime.strptime(date_str, '%Y%m%d')

        # Get the month and year of the date 
        month = date.month 
        year = date.year 
        
        # Determine the season year 
        if month >= 11: 
            # If the month is November or December 
            season_year = year + 1 
        else: 
            # If the month is January to October 
            season_year = year 
        return season_year
    
    def get_formatted_date(self):
        current_date = datetime.now()
        formatted_date = current_date.strftime('%Y%m%d')
        return formatted_date

# m = GrabData()
# dataset = m.load_json_file('data/20241228_games.json')
# t = m.get_formatted_date()
# m2 = GrabData()
# top30 = []
# dataset2 = m2.load_json_file('data/leaderboard_data_2025.json')
# for data in dataset2:
#     rank = int(data.get('Rank'))
#     if rank < 31:
#         team = data.get('team_name')
#         top30.append(team)

# prcnts = []
# dataset1 = m.load_json_file('data/individual_data.json')
# for teamn in top30:
#     data = m.get_team_data(dataset1, f'{teamn}_2025')
#     team = data['team_name']
#     x=0
#     len_var = len(data.items())
#     count = 0
#     for op,details in data.items():
#         if count > 0:
#             x += details[0]
#         count+=1
#     percent_data = x/len_var/364
#     match_diff_prcent = 1-percent_data
#     prcnts.append(match_diff_prcent)

# paired = list(zip(top30, prcnts))
# paired.sort(key=lambda x: x[1])

# sorted_t, sorted_p = zip(*paired)
# top30.reverse()
# for i in range(0, len(sorted_t)):
#     print(f'{sorted_t[i]}, {sorted_p[i]:.3f}, {top30[i]}')


# data = m.get_team_data(dataset, 'Gonzaga_2025')
# data.pop('team_name', None)
# x=0
# len_var = len(data.items())
# for op,details in data.items():
#     x += details[0]
# percent_data = x/len_var/364
# match_diff_prcent = 1-percent_data
# print(match_diff_prcent)