import scrapedata
t=scrapedata
t.initialize_path(path_to_paths='$HOME/projects/NCAAB_Predictions/database/paths.json')

def reformat_date(date_str):
    month,day = date_str.split('-')
    day = str(int(day))
    return f'{month}-{day}'
# t.LeaderboardStats('2025').scrape_data()
# t.MatchPlayerStats('Auburn', 'Texas', '1-7', '2025').scrape_data()
# t2 = 'Texas'
# t.MatchHistory(t1, '2025').scrape_data()
# t.MatchHistory(t2, '2025').scrape_data()
def get_matches_with_match_hist():
    t1 = 'Texas'
    import handledata
    t = handledata
    t.initialize_path(path_to_paths='$HOME/projects/NCAAB_Predictions/database/paths.json')
    cf = t.CommonFunctions()
    data = cf.load_json_file('database/match_history_stats.json')
    teams_data = cf.get_team_data(data,t1)
    teams_data.pop('Rank')
    teams_data.pop('team_name')
    for match, stats in teams_data.items():
        date = stats.get('Date')
        date_formatted = reformat_date(date)
        import scrapedata
        t=scrapedata
        t.initialize_path(path_to_paths='$HOME/projects/NCAAB_Predictions/database/paths.json')
        t.MatchPlayerStats(t1, match, date_formatted, '2025').scrape_data()
        print('done')
import handledata
t = handledata
t.initialize_path(path_to_paths='$HOME/projects/NCAAB_Predictions/database/paths.json')
# t.AnalyzeMatchHist(t1, 'at', t2)
t.PointPrediction('Auburn', 'at', 'Texas', True)
t.AnalyzeMatchHist('Auburn', 'at', 'Texas')
# ttest
