import scrapedata
from handledata import MatchFirst500
t=scrapedata
t.initialize_path(path_to_paths='$HOME/projects/NCAAB_Predictions/database/paths.json')
t.LeaderboardScrape('2025').scrape_data()
t.IndividualTeamScrape('Gonzaga', '2025').scrape_data()
t.SpecificMatchStats('Gonzaga', 'Indiana', '11-28', '2025').scrape_data()