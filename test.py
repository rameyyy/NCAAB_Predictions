path_to_path_str = '$HOME/projects/NCAAB_Predictions/database/paths.json'
import reportgen
rg = reportgen
rg.initialize_path(path_to_paths='$HOME/projects/NCAAB_Predictions/database/paths.json')
# rg.CurrentDayScrape().scrape_all()
# rg.CurrentDayReport().generate_report(False, True, '01-10-2025_match_predictions.txt')
import handledata
hd = handledata
hd.initialize_path(path_to_path_str)
hd.CommonFunctions().clear_game_sched_file()
rg.CommonScrapes().game_winners('20250217')

# import handledata
# hd = handledata
# hd.initialize_path(path_to_paths='$HOME/projects/NCAAB_Predictions/database/paths.json')
# t1 = 'UCLA'
# t2 = 'Maryland'
# data = hd.AnalyzeMatchHist(t1, 'at', t2, False).return_odds()
# data2 = hd.PrevWinner(t1, 'at', t2, False).return_odds()
# data3 = hd.AccuracyEstimate(t1, 'at', t2, False).return_odds()
# data4 = hd.PointPrediction(t1, 'at', t2, True).return_odds()
# print(f'{data[0]:.2f}, {data[1]:.2f}')
# print(f'{data2[0]:.2f}, {data2[1]:.2f}')
# print(f'winstreak {data[2]}')
# print(data3)
# print(data4)

# import scrapedata
# sd = scrapedata
# sd.initialize_path(path_to_path_str)
# sd.LeaderboardStats('2024').scrape_data()
# sd.MatchHistory('Tarleton+St.', '2025').scrape_data()
# sd.MatchHistory('Southern+Utah', '2025').scrape_data()