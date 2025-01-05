# modules for class
# scraping from NCAAB Barttorvik stats
import requests
from bs4 import BeautifulSoup
import json
import os

class MatchHistory:
	def __init__(self, team:str, year:str):
		self.team = team
		self.year = year
		self.url = f'https://barttorvik.com/team.php?team={team}&year={year}'

	def __get_path(self):
		from . import get_paths
		paths_arr = get_paths()
		return paths_arr		# path to match hist str in [0]

	def __get_differential(self, date_string:str):
		values = date_string.split('-')

		val1_len = len(values[0])
		if val1_len > 3:
			val1 = int(values[0][:3])
		else:
			val1 = int(values[0])

		val2_len = len(values[1])
		if val2_len > 3:
			val2 = int(values[1][:3])
		else:
			val2 = int(values[1])
		
		return abs(val1-val2)

	def __get_teams_ranks(self, team_name:str):
		file_path = self.__get_path()
		try:
			with open(file_path[1], 'r') as json_file:
				data = json.load(json_file)
		except FileNotFoundError:
			print(f'File not found: {file_path}')
			return None
		
		for team in data:
			if team['team_name'] == team_name:
				return team['Rank']
		return None
	
	def __get_scores(self, date_string:str):
		values = date_string.split('-')

		val1_len = len(values[0])
		if val1_len > 3:
			val1 = int(values[0][:3])
		else:
			val1 = int(values[0])

		val2_len = len(values[1])
		if val2_len > 3:
			val2 = int(values[1][:3])
		else:
			val2 = int(values[1])

		return [val1, val2]

	def __update_json_file(self, new_data):
		file_path = self.__get_path()
		try:
			if os.path.getsize(file_path[0]) != 0:
				try:
					with open(file_path[0], 'r') as file:
						existing_data = json.load(file)
					existing_data = [entry for entry in existing_data if entry.get('team_name') != new_data.get('team_name')]
					existing_data.append(new_data)
				except Exception:
					existing_data = []
			else:
				existing_data = new_data
		except FileNotFoundError:
			existing_data = new_data

		with open(file_path[0], 'w') as file:
			json.dump(existing_data, file, indent=4)
	
	def __get_team_name(self, url:str):
		query_start = url.find('?') + 1

		params = url[query_start:].split('&')

		for param in params:
			key_val = param.split('=')
			if key_val[0] == 'team':
				return key_val[1]
		return None

	def __format_data(self, data):
		try:
			new_data = float(data)
			return new_data
		except Exception:
			return data
			
	def scrape_data(self):
		# scraping
		response = requests.get(self.url)
		html = response.text

		# initialize arrays
		header_arr = ['Tempo', 'Record', 'WAB', 'ADJO', 'ADJD', 'OF-EFF', 'OF-EFG%', 
                'OF-TO%', 'OF-OR%', 'OF-FTR', 'OF-2P', 'OF-3P', 'DF-EFF', 'DF-EFG%', 'DF-TO%',
                'DF-OR%', 'DF-FTR', 'DF-2P', 'DF-3P', 'G-SC', '+/-', 'HNA']
		all_data = {}
		data_load = []
		ops = []
		wl = []
		diff = []
		dates = []
		score_arr = []
		rank_arr = []

		# parsing
		soup = BeautifulSoup(html, 'html.parser')
		table = soup.find('table', class_='skedtable')
		if table is None: # no individ data for team:
			return -1
		tbody = table.find('tbody')
		ops_data = tbody.select('tr td.mobileout a[href^="team.php"]')
		allTD_data = tbody.select('tr td')
		WL_data = tbody.select('tr td a[href^="box.php"]')
		date_data = tbody.select('tr td a[href^="schedule.php"] span.mobileonly')

		for data in ops_data:
			team_name_ = self.__get_team_name(data['href'])
			rank_arr.append(self.__get_teams_ranks(team_name_))
			ops.append(team_name_)

		formatted_data = []
		loop_count = 0
		for data in allTD_data:
			data_ = data.text
			if '\n' not in data_ and data_ != '':
				if '•' not in data_:
					if loop_count > 4:
						data_str = f'{data_}'
						if 'W' in data_:
							pass
						elif 'L' in data_:
							pass
						elif '(' in data_:
							pass
						elif ')' in data_:
							pass
						else:
							formatted_data.append(data_str)
					if data_ in ['H', 'N', 'A']:
						if len(formatted_data) > 10:
							data_load.append(formatted_data)
						loop_count = 0
						formatted_data=[]
					else:
						loop_count += 1
      
		for data in WL_data:
			str_data = str(data.text)
			winloss = str_data[0]
			differential_str = str_data[3:]
			differential = self.__get_differential(differential_str)
			scores = self.__get_scores(differential_str)
			if winloss == 'L':
				differential *= -1
				wl.append(0)
			else:
				wl.append(1)
			diff.append(differential)
			score_arr.append(scores)

		for data in date_data:
			dates.append(data.text)

		temp_dict = {}
		teams_rank = self.__get_teams_ranks(self.team)
		all_data['team_name'] = self.team
		all_data['Rank'] = teams_rank

		op_counter = 0


		for data in data_load:
			for i in range(0, len(header_arr)):
				format_data_ = self.__format_data(data[i])
				temp_dict[header_arr[i]] = format_data_
			temp_dict['Rank'] = rank_arr[op_counter]
			temp_dict['Date'] = dates[op_counter]
			temp_dict['W/L'] = wl[op_counter]
			temp_dict['Score'] = score_arr[op_counter]
			temp_dict['Diff'] = diff[op_counter]
			all_data[ops[op_counter]] = temp_dict
			op_counter += 1

		self.__update_json_file(all_data)