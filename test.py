file_path_to_path = '$HOME/projects/NCAAB_Predictions/database/paths.json'
import handledata
hd = handledata
hd.initialize_path(file_path_to_path)
# data = hd.AnalyzeMatchHist2('Auburn', 'at', 'Kentucky', False).return_odds()
# print(data)
import handledata
hd = handledata
hd.initialize_path(file_path_to_path)
commonFuncs = hd.CommonFunctions()
paths_arr = commonFuncs.get_path()
path_to_schedule = paths_arr[2]
schedule_data = commonFuncs.load_json_file(path_to_schedule)
for dateStr, matches in schedule_data.items():
    for match in matches:
            t1 = match[0]
            at_vs = match[1]
            t2 = match[2]
            matchHist_odds_arr = hd.AnalyzeMatchHist2(t1, at_vs, t2, False).return_odds()
            print(f'{t1}: {matchHist_odds_arr[0]:.2f}%, {t2}: {matchHist_odds_arr[1]:.2f}%')