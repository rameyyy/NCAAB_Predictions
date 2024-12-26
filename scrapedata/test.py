# import pull_data as bd
from barttorvik_leaderboard import LeaderboardScrape
from barttorvik_schedule import IndividualTeamScrape
import json
def load_json_data():
	with open('leaderboard_data.json', 'r') as json_file:
		json_data = json.load(json_file)
	return json_data
	
def get_teams_data(teams_name:str, data_set:json):
	team_name_to_query = '_'+teams_name
	for data in data_set:
		if data['team_name'] == team_name_to_query:
			return data
	return f"Could not find team '{teams_name}' in the dataset"

def create_team_sched_file(data_set:json):
	team_names = [entry['team_name'] for entry in data_set if 'team_name' in entry]
	return team_names

# LeaderboardScrape('2025').scrape_data()
# dataset = load_json_data()
# teams = create_team_sched_file(dataset)
# for team1 in teams:
# 	try:
# 		IndividualTeamScrape(team=team1, year='2025').scrape_data()
# 	except Exception as e:
# 		pass

# teams_info = get_teams_data('Tennessee', dataset)
# print(teams_info)


LeaderboardScrape('2025').scrape_data()
