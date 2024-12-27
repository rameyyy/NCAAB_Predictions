# modules for class
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

class DateSchedule:
	def __init__(self, date:str):
		self.date = date
		self.url = f'https://barttorvik.com/schedule.php?date={date}'
  
	def __get_path(self):
		from . import get_paths
		paths_arr = get_paths()
		return paths_arr		# path to schedule str in [2]
	
	def __put_in_json(self, data):
		file_path = self.__get_path()
		with open(file_path[2], 'w') as json_file:
			json.dump(data, json_file, indent=4)

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
		all_data = {self.date: []}
		teams = []
		at_n = []

		# parsing
		soup = BeautifulSoup(html, 'html.parser')
		table = soup.find('table')
		tbody = table.find('tbody')
		home_away = tbody.find_all('td')
		teams_data = tbody.select('tr td a[href^="team.php"]')

		lc=0
		for td in home_away:
			data = str(td.text)
			if ' at ' in data:
				at_n.append('at')
			elif ' vs ' in data:
				at_n.append('vs')

		for data in teams_data:
			team_name_ = self.__get_team_name(data['href'])
			teams.append(team_name_)

		teams_count = len(teams)
        # makes sure you pulled an even number of teams
		if teams_count % 2 != 0:
			teams.pop()
		
		lc = 0
		for i in range(0, teams_count):
			if i%2 == 0:
				data = [teams[i], at_n[lc], teams[i+1]]
				all_data[self.date].append(data)
				lc+=1
		
		self.__put_in_json(all_data)