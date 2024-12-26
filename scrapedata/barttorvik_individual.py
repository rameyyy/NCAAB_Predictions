# modules for class
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from . import schema
import re

class IndividualTeamScrape:
	def __init__(self, team:str, year:str):
		self.team = team
		self.year = year
		self.url = f'https://barttorvik.com/team.php?team={team}&year={year}'

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

	@staticmethod
	def clear_individ_data_file():
		with open(f'{schema.BARTTORVIK_DATA_DIREC}individual_data.json', 'w') as f:
			pass

	def __get_teams_ranks(self, team_name:str):
		file_path = f'{schema.BARTTORVIK_DATA_DIREC}leaderboard_data_{self.year}.json'
		try:
			with open(file_path, 'r') as json_file:
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
		try:
			with open(f'{schema.BARTTORVIK_DATA_DIREC}individual_data.json', 'r') as file:
				existing_data = json.load(file)
		except FileNotFoundError:
			existing_data = []
		existing_data = [entry for entry in existing_data if entry.get('team_name') != new_data.get('team_name')]
		existing_data.append(new_data)

		with open(f'{schema.BARTTORVIK_DATA_DIREC}individual_data.json', 'w') as file:
			json.dump(existing_data, file, indent=4)
	
	def __get_team_name(self, url:str):
		query_start = url.find('?') + 1

		params = url[query_start:].split('&')

		for param in params:
			key_val = param.split('=')
			if key_val[0] == 'team':
				return key_val[1]
		return None
			
	def scrape_data(self):
		# scraping
		response = requests.get(self.url)
		html = response.text

		# initialize arrays
		all_data = {}
		ops = []
		hna = []
		wl = []
		diff = []
		dates = []
		score_arr = []
		rank_arr = []

		# parsing
		soup = BeautifulSoup(html, 'html.parser')
		table = soup.find('table', class_='skedtable')
		tbody = table.find('tbody')
		ops_data = tbody.select('tr td.mobileout a[href^="team.php"]')
		allTD_data = tbody.select('tr td')
		WL_data = tbody.select('tr td a[href^="box.php"]')
		date_data = tbody.select('tr td a[href^="schedule.php"] span.mobileonly')

		for data in ops_data:
			team_name_ = self.__get_team_name(data['href'])
			rank_arr.append(self.__get_teams_ranks(team_name_))
			ops.append(team_name_)

		
		for data in allTD_data:
			if data.text in ['H', 'N', 'A']:
				hna.append(data.text)
		
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

		teams_rank = self.__get_teams_ranks(self.team)
		all_data['team_name'] = self.team
		all_data['Rank'] = teams_rank
		for i in range(0, len(ops)):
			if i < len(wl):
				all_data[ops[i]] = [rank_arr[i], dates[i], hna[i], wl[i], score_arr[i], diff[i]]
			# elif len(hna) == len(ops):
			# 	all_data[ops[i]] = [dates[i], hna[i], '', '']
			# elif len(dates) == len(ops):
			# 	all_data[ops[i]] = [dates[i], '', '', '']
			# else:
			# 	all_data[ops[i]] = ['', '', '', '']
		self.__update_json_file(all_data)