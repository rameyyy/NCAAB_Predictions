# modules for class
# scraping from NCAAB Barttorvik stats
import requests
from bs4 import BeautifulSoup
import json
import os

class MatchPlayerStats:
	def __init__(self, team1:str, team2:str, date:str, year:str):
		self.team1 = team1
		self.team2 = team2
		self.url1 = f'https://www.barttorvik.com/box.php?muid={team1}{team2}{date}&year={year}'
		self.url2 = f'https://www.barttorvik.com/box.php?muid={team2}{team1}{date}&year={year}'
		self.url = self.url1

	def __check_data(self, data:str): 
		if data[0] == '+' or data[0] == '-':
			return False
		try:
			int_test = int(data[0])
			return False
		except Exception:
			return True
  
	def __get_path(self):
		from . import get_paths
		paths_arr = get_paths()
		return paths_arr		# path to match player stats in str 3
	
	def __put_in_json(self, data):
		file_path_arr = self.__get_path()
		file_path = file_path_arr[3]
		try:
			if os.path.exists(file_path):
				with open(file_path, 'r') as json_file:
					existing_data = json.load(json_file)
			else:
				existing_data = []
		except Exception:
			existing_data = []

		existing_data.append(data)
		with open(file_path, 'w') as f:
			json.dump(existing_data, f, indent=4)
	
	def __correct_team_in_dict(self, t1_dataset, team1):
		file_path_arr = self.__get_path()
		file_path = file_path_arr[0]
		with open(file_path, 'r') as f:
			dataset_matchHist = json.load(f)
		for data in dataset_matchHist:
			if data['team_name'] == team1:
				data_copy = data.copy()
				break
		data_copy.pop("Rank")
		data_copy.pop("team_name")
		for match, match_data in data_copy.items():
			if match == self.team2:
				who_won = match_data.get('W/L')
				points_arr = match_data.get("Score")
				if who_won == 1:
					winner = team1
					t1_points = points_arr[0]
					break
				else:
					winner = self.team2
					t1_points = points_arr[1]
					break
		for player, player_stats in t1_dataset.items():
			if player == 'Totals':
				t1_points_recorded = player_stats.get('Pts')
				break
		if t1_points == t1_points_recorded:
			return True
		else:
			return False
		
			
	def scrape_data(self):
		try:
			# scraping
			response = requests.get(self.url)
			html = response.text

			# initialize arrays
			stat_headers_arr = []
			players_stats_extended_arr = []
			match_dictionary = {
				self.team1: {},
				self.team2: {}
			}

			# parsing
			soup = BeautifulSoup(html, 'html.parser')
			table = soup.find('table')
			stat_header = table.select('tr th')
			player_stats = table.select('tr td')
			
			record_data = False
			for data in stat_header:
				if record_data == True:
					stat_headers_arr.append(data.text)
				if data.text == 'Player':
					record_data = True
				if data.text == 'Pts':
					record_data = False

			players_stats_arr = []
			for data in player_stats:
				data_ = data.text
				if data_ != '':
					if self.__check_data(data_):
						if len(players_stats_arr) > 0:
							players_stats_extended_arr.append(players_stats_arr)
						players_stats_arr = []
						players_stats_arr.append(data_)
					else:
						players_stats_arr.append(data_)
			players_stats_extended_arr.append(players_stats_arr)

			team2_bool = False
			temp_dict_1 = {}
			temp_dict_2 = {}
			for array in players_stats_extended_arr:
				for i in range(0, len(array)):
					if i == 0:	# The player
						player = array[i]
					elif player == 'Totals':
						if i < 3:
							temp_dict_2[stat_headers_arr[i-1]] = array[i]
						elif i < 24:
							temp_dict_2[stat_headers_arr[i]] = array[i]
						elif i >= 24:
							temp_dict_2[stat_headers_arr[i+3]] = array[i]
					else:
						temp_dict_2[stat_headers_arr[i-1]] = array[i]
				temp_dict_1[player] = temp_dict_2
				if team2_bool == False:
					match_dictionary[self.team1].update(temp_dict_1)
				else:
					match_dictionary[self.team2].update(temp_dict_1)
				if player == 'Totals':
					team2_bool = True
				temp_dict_1 = {}
				temp_dict_2 = {}
			full_formatted_dict = {
				f'{self.team1}-{self.team2}': match_dictionary
			}
			correct_dict_bool = self.__correct_team_in_dict(match_dictionary[self.team1], self.team1)
			if correct_dict_bool == False:
				t1_data = match_dictionary.pop(self.team2)
				t2_data = match_dictionary.pop(self.team1)
				match_dictionary[self.team1] = t1_data
				match_dictionary[self.team2] = t2_data
			full_formatted_dict = {
				f'{self.team1}-{self.team2}': match_dictionary
			}
			self.__put_in_json(full_formatted_dict)
		except Exception:
			if self.url == self.url1:
				self.url = self.url2
				self.scrape_data()
			else:
				print('Failed to scrape match player stats data')
				return None