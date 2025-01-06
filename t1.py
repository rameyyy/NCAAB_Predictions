import scrapedata
t=scrapedata
t.initialize_path(path_to_paths='$HOME/projects/NCAAB_Predictions/database/paths.json')
# # t.LeaderboardStats('2025').scrape_data()
t.MatchHistory('Missouri', '2025').scrape_data()
# t.MatchHistory('Auburn', '2025').scrape_data()
import handledata
t = handledata
t.initialize_path(path_to_paths='$HOME/projects/NCAAB_Predictions/database/paths.json')
t.AnalyzeMatchHist('Kansas', 'at', 'Missouri')
