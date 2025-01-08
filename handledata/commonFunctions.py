import json
from datetime import datetime

class CommonFunctions:
    def __init__(self):
        pass
    
    def get_path(self):
        from . import get_paths
        paths_arr = get_paths()
        return paths_arr

    def load_json_file(self, path):
        with open(path, 'r') as f:
            data = json.load(f)
        return data

    def get_player_matchup_data(self, data_set, team1_dash_team2):
        for game in data_set:
            if team1_dash_team2 in game:
                return game[team1_dash_team2]
        return None
    
    def get_team_data(self, data_set, team_name): 
        for data in data_set:
            if data['team_name'] == team_name:
                return data
        print(f"Could not find team '{team_name}' in the dataset")
        return None
    
    def reformat_date(self, date_str):
        month,day = date_str.split('-')
        day = str(int(day))
        return f'{month}-{day}'

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
    
    def get_function_weight(self, class_key:str, function_key:str):
        file_path_arr = self.get_path()
        file_path = file_path_arr[4]
        with open(file_path, 'r') as json_f:
            json_data = json.load(json_f)
        active_model = json_data.get("ActiveModel")
        function_weight_value = json_data[active_model][class_key][function_key]
        return function_weight_value
    
    def get_lowest_rank(self):
        file_path_arr = self.get_path()
        file_path = file_path_arr[1] #Leaderboard file path
        with open(file_path, 'r') as f:
            json_data = json.load(f)
        last_team = json_data[-1]
        last_team_rank = last_team.get("Rank")
        return last_team_rank