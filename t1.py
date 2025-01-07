import scrapedata
t=scrapedata
t.initialize_path(path_to_paths='$HOME/projects/NCAAB_Predictions/database/paths.json')
# t.LeaderboardStats('2025').scrape_data()
# t.MatchPlayerStats('Auburn', 'Missouri', '1-4', '2025').scrape_data()
# t1 = 'Auburn'
# # t2 = 'Auburn'
# t.MatchHistory(t1, '2025').scrape_data()
# t.MatchHistory(t2, '2025').scrape_data()
import handledata
t = handledata
t.initialize_path(path_to_paths='$HOME/projects/NCAAB_Predictions/database/paths.json')
# t.AnalyzeMatchHist('Monmouth', 'at', 'Auburn')
t.PointPrediction('Auburn', 'at', 'Missouri')
