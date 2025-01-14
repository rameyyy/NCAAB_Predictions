# modules for class
# scraping from NCAAB Barttorvik stats
import requests
from bs4 import BeautifulSoup
import json
import re

class LeaderboardStats:
	def __init__(self, year:str):
		self.year = year
		self.url = f'https://barttorvik.com/trank.php?year={year}#'

	def __get_path(self):
		from . import get_paths
		paths_arr = get_paths()
		return paths_arr		# path to leaderboard str in [1]

	def __put_in_json(self, data):
		file_path_arr = self.__get_path()
		file_path = file_path_arr[1]
		file_p, dot_json = file_path.split('.')
		file_path = file_p + f'_{self.year}.' + dot_json
		with open(file_path, 'w') as json_file:
			json.dump(data, json_file, indent=4)
	
	def __format_number(self, num):
		# disgusting try block, simply returns str to correct num format
		try:
			new_num = int(num[0])
			return new_num
		except Exception:
			try:
				new_num = float(num[0])
				return new_num
			except Exception:
				return num
	
	def __get_team_name(self, url:str):
		query_start = url.find('?') + 1

		params = url[query_start:].split('&')

		for param in params:
			key_val = param.split('=')
			if key_val[0] == 'team':
				return key_val[1]
		return None
			
	def scrape_data(self):
		# grabs data and stores into html format in 'html' var
		response = requests.get(self.url)
		html = response.text

		# parsing
		soup = BeautifulSoup(html, 'html.parser')
		table_row = soup.find('tr', class_ = 'seedrow')

		# Initialize a list to hold the data 
		dct_items = ['Rank', 'G', 'WLrecord', 'ADJOE', 'ADJDE', 'EFG%', 
			   'EFGD%', 'TOR', 'TORD', 'ORB', 'DRB', 'FTR', 'FTRD', '2P%',
			   '2P%D', '3P%', '3P%D', '3PR', '3PRD', 'ADJ T', 'WAB']
		all_data = []
		team_names = [] 

		table = soup.find('table')
		tbody = table.find('tbody')
		team_data = tbody.select('tr td a[href^="team.php"]')

		for data in team_data:
				team_names.append(self.__get_team_name(data['href']))
		
		# Iterate through each <tr> with class 'seedrow'
		loop = 0 
		while table_row: 

			# Get the team name from the id attribute 
			team_name = table_row['id'] 

			# Initialize a dictionary to hold the team's data
			team_data = {'team_name': team_names[loop]}

			# Find all 'td' tags within the table row 
			td_tags = table_row.find_all('td')

			# Iterate loop var
			loop += 1

			# Extract the numeric data from each 'td' tag 
			count = 0
			index = 0
			for td in td_tags: 
				# Find all numbers using regex
				if count != 1 and count != 2 and count != 7: # Useless data bit
					num = re.findall(r'[+-]?\d+(?:\.\d+)?', td.get_text())
					if count == 4:
						formatted_num = []
						for i in num: formatted_num.append(int(i))
					else:
						formatted_num = self.__format_number(num)
					team_data[dct_items[index]] = formatted_num
					index += 1
				count += 1

			# Append the team's data to the list 
			all_data.append(team_data)
			# Move to the next <tr> with class 'seedrow' 
			table_row = table_row.find_next_sibling('tr', class_='seedrow') 

		# put the data into json file
		self.__put_in_json(all_data)