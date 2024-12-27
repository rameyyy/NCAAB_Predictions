import handledata.analysis_part1
import handledata.common_functions
import handledata.point_predict
import scrapedata
# __all__ = ['IndividualTeamScrape', 'LeaderboardScrape', 'DateSchedule'] #
import handledata

# cf = common_functions.GrabData()
# date = cf.get_formatted_date()
# DateSchedule('20241225').scrape_data()
import json
import traceback
# date = '20241228'
cf = handledata.common_functions.GrabData()
date1 = cf.get_formatted_date()
year1 = cf.get_ncaa_season_year(date1)
ScrapeData = scrapedata
ScrapeData.initialize_path(path_to_paths='$HOME/projects/NCAAB_Predictions/database/paths.json')
ScrapeData.DateSchedule(date=date1).scrape_data()
paths = ScrapeData.get_paths()
with open(paths[2], 'r') as f:
    data = json.load(f)

ScrapeData.LeaderboardScrape(year1).scrape_data()
data2=data.get(f'{date1}')
for i in data2:
        try:
            t1 = i[0]
            v = i[1]
            t2 = i[2]
            c1 = ScrapeData.IndividualTeamScrape(t1, year1).scrape_data()
            c2 = ScrapeData.IndividualTeamScrape(t2, year1).scrape_data()
            if c1 != -1 and c2 != -1:
                handledata.analysis_part1.MatchFirst500(t1, v, t2)
                handledata.point_predict.PointPrediction(t1, v, t2)
        except Exception as e:
            trb = traceback.print_exc()
            with open('errors.txt', 'a') as f:
                  f.write(f'{e}\n{trb}\n\n')
#     c+=1
# t2 = 'Dayton'
# t1 = 'Marquette'
# vs = 'at'
# handledata.analysis_part1.MatchFirst500(t1, vs, t2)
# handledata.point_predict.PointPrediction(t1, vs, t2)
# IndividualTeamScrape('Dayton', '2025').scrape_data()

# top30 = []
# def load_json_file(path):
#     with open(path, 'r') as f:
#         data = json.load(f)
#     return data
# dataset2 = load_json_file('data/leaderboard_data_2025.json')
# for data in dataset2:
#     rank = int(data.get('Rank'))
#     if rank < 31:
#         team = data.get('team_name')
#         top30.append(team)
# print(top30)
# for i in top30:
#     team = IndividualTeamScrape(i, '2025')
#     team.scrape_data()