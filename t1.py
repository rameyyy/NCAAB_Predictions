import scrapedata
t=scrapedata
t.initialize_path(path_to_paths='$HOME/projects/NCAAB_Predictions/database/paths.json')
# t.LeaderboardStats('2025').scrape_data()
# t.MatchHistory('Auburn', '2025').scrape_data()
# t.MatchHistory('Texas', '2025').scrape_data()
import handledata
d = handledata
d.initialize_path(path_to_paths='$HOME/projects/NCAAB_Predictions/database/paths.json')
# date = d.CommonFunctions().get_formatted_date()
# t.GameWinners('20250106').scrape_data()

def reformat_date(date_str):
    month,day = date_str.split('-')
    day = str(int(day))
    return f'{month}-{day}'

def get_score_from_str(score_str):
        pt1, pt2 = score_str.split('-')
        pt1 = int(pt1)
        pt2 = int(pt2)
        arr = [pt1, pt2]
        return arr
# t.LeaderboardStats('2025').scrape_data()
# t.MatchPlayerStats('Auburn', 'Texas', '1-7', '2025').scrape_data()
# t2 = 'Texas'
# t1= 'Auburn'
# t.GameWinners('20250107').scrape_data()
# t.MatchHistory(t1, '2025').scrape_data()
# t.MatchHistory(t2, '2025').scrape_data()
def get_matches_with_match_hist(t1):
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
# import handledata
# t = handledata
# t.initialize_path(path_to_paths='$HOME/projects/NCAAB_Predictions/database/paths.json')
# # t.AnalyzeMatchHist(t1, 'at', t2)
# t.PointPrediction('Auburn', 'at', 'Texas', True)
# t.AnalyzeMatchHist('Auburn', 'at', 'Texas')
# ttest
def test_run():
    import handledata
    hd = handledata
    hd.initialize_path(path_to_paths='$HOME/projects/NCAAB_Predictions/database/paths.json')
    cf = hd.CommonFunctions()
    data = cf.load_json_file('database/game_schedule.json')
    game_counter = 0
    matchwinner_acc = 0
    pointwinner_acc = 0
    t1_point_accuracy = 0
    t2_point_accuracy = 0
    both_hit = 0
    finalStr = ''
    for date, games in data.items():
        for game_data in games:
            t1 = game_data[0]
            at_or_vs = game_data[1]
            t2 = game_data[2]
            winner = game_data[3]
            score_not_int = game_data[4]
            score_arr = get_score_from_str(score_not_int)
            odds1 = hd.AnalyzeMatchHist(t1, at_or_vs, t2, True).return_odds()
            odds2 = hd.PointPrediction(t1, at_or_vs, t2, True).return_odds()
            if odds2 == 'Fail':
                continue
            accuracy_pred = hd.AccuracyEstimate(t1, at_or_vs, t2, True).return_odds()
            printStr = f'{t1} {at_or_vs} {t2}\n'
            printStr += f'\tWinner: {winner}\n\tScore: {score_arr}\n'
            printStr += f'\t{t1}: {odds1[0]:.2f}% | {t2}: {odds1[1]:.2f}%\n'
            printStr += f'\t{t1}: {odds2[0]:.2f} | {t2}: {odds2[1]:.2f}\n'
            if odds2[0] > odds2[1]:
                pointWinner = t1
            else:
                pointWinner = t2
            if odds1[0] > odds1[1]:
                matchWinner = t1
            else:
                matchWinner = t2
            printStr += f'\tPrediction Accuracy: {accuracy_pred}\n'
            if matchWinner == winner:
                printStr += '\tAMH: HIT\n'
                matchwinner_acc += 1
            else:
                printStr += '\tAMH: MISS\n'
            if pointWinner == winner:
                printStr += '\tPPM: HIT\n'
                pointwinner_acc += 1
            else:
                printStr += '\tPPM: MISS\n'
            
            if pointWinner == winner and matchWinner == winner:
                both_hit += 1
                
            if pointWinner == t1:
                t1_scored = odds2[0]
                t2_scored = odds2[1]
            else:
                t1_scored = odds2[1]
                t2_scored = odds2[0]
            temp_accuracy1 = t1_scored / float(score_arr[0])
            temp_accuracy1*=100
            temp_accuracy2 = t2_scored / float(score_arr[1])
            temp_accuracy2*=100
            if temp_accuracy1 > 100.0:
                temp_accuracy1 -= 100
                final_acc1 = 100 - temp_accuracy1
            else: final_acc1 = temp_accuracy1
            if temp_accuracy2 > 100.0:
                temp_accuracy2 -= 100
                final_acc2 = 100 - temp_accuracy2
            else: final_acc2 = temp_accuracy2
            
            printStr += f'\t{t1} ptAcc: {final_acc1:.2f}%\n\t{t2} ptAcc: {final_acc2:.2f}%\n\n'
            finalStr += printStr
            printStr = ''
            game_counter += 1
            t1_point_accuracy += final_acc1
            t2_point_accuracy += final_acc2


    t1_overall_pt_acc = t1_point_accuracy / float(game_counter)
    t2_overall_pt_acc = t2_point_accuracy / float(game_counter)
    both_hit_prcnt = both_hit / float(game_counter)
    point_hit_prcnt = pointwinner_acc / float(game_counter)
    match_hit_prcnt = matchwinner_acc / float(game_counter)
    both_hit_prcnt *= 100
    point_hit_prcnt *= 100
    match_hit_prcnt *= 100
    finalStr += f'\nBoth Hit = {both_hit_prcnt:.2f}%\n'
    finalStr += f'Point Hit = {point_hit_prcnt:.2f}%\n'
    finalStr += f'Match Hit = {match_hit_prcnt:.2f}%\n'
    finalStr += f'Winner Pt Predict Accuracy {t1_overall_pt_acc:.2f}%\n'
    finalStr += f'Loser Pt Predict Accuracy {t2_overall_pt_acc:.2f}%\n'
    print(finalStr)
    with open('beta_model_test_run.txt', 'w') as f:
        f.write(finalStr)

        
            # t.MatchHistory(t1, '2025').scrape_data()
            # t.MatchHistory(t2, '2025').scrape_data()
            # get_matches_with_match_hist(t1=t1)
            # get_matches_with_match_hist(t1=t2)
            # print(f'finished... {t1} {at_or_vs} {t2}')
            
test_run()