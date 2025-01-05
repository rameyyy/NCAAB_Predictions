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
		if self.__first_in_alphabet(team1, team2) == team1:
			self.url = f'https://www.barttorvik.com/box.php?muid={team1}{team2}{date}&year={year}'
		else:
			self.url = f'https://www.barttorvik.com/box.php?muid={team2}{team1}{date}&year={year}'
  
	def __first_in_alphabet(self, t1, t2):
		if t1 < t2:
			return t1
		else:
			return t2

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
		return paths_arr[3]		# path to match player stats in str 3
	
	def __put_in_json(self, data):
		file_path = self.__get_path()
		if os.path.exists(file_path):
			with open(file_path, 'r') as json_file:
				existing_data = json.load(json_file)
		else:
			existing_data = []

		existing_data.append(data)
		with open(file_path, 'w') as f:
			json.dump(existing_data, f, indent=4)
			
	def scrape_data(self): 
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
		self.__put_in_json(full_formatted_dict)