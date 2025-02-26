import json
import time
import urllib.parse
path_to_path_str = '$HOME/projects/NCAAB_Predictions/database/paths.json'
import reportgen
rg = reportgen
rg.initialize_path(path_to_path_str)
import handledata
hd = handledata
hd.initialize_path(path_to_path_str)
import scrapedata
sd = scrapedata
sd.initialize_path(path_to_path_str)
file_path_arr = hd.CommonFunctions().get_path()
path_to_sched = file_path_arr[2]
sched_data = hd.CommonFunctions().load_json_file(path_to_sched)
import sqlDBmanage
# start_time = time.time()
# rg.CurrentDayScrape().calculate_run_time(start_time, False)
# hd.CommonFunctions().clear_match_hist_stats()
def update_value(key, value):
    path_arr = hd.CommonFunctions().get_path()
    models_path = path_arr[4]
    with open(models_path, 'r') as f:
        data = json.load(f)
    data['Model_OPTIMUS_B']['prevWinner'][key] = value
    with open(models_path, 'w') as f:
        json.dump(data, f, indent=4)

def run_the_nums():
    match_counter = 0
    amh_correct = 0
    prevWinner_correct = 0
    safe_bet_correct = 0
    safe_bet_count = 0
    super_safe_bet_correct = 0
    super_safe_bet_count = 0
    for dataEntry in sched_data:
        for dateStr, matches in dataEntry.items():
            for match in matches:
                try:
                    if '🎯' in match[4]: #filtering emoji in data lol
                        continue
                    t1 = match[0]
                    at_vs = match[1]
                    t2 = match[2]
                    winner = match[3]
                    matchID = f'{dateStr}_{t1}_{t2}'
                    insert_data_arr = []
                    insert_data_arr.append(matchID)
                    ## data = return if optimizing analyze math hist
                    analyzeMH_arr = hd.AnalyzeMatchHist(t1, at_vs, t2, True).return_odds()
                    #
                    risk_arr = hd.AccuracyEstimate(t1, at_vs, t2, True).return_odds()
                    # data = return if optimizing prev winner
                    prevWinner_arr = hd.PrevWinner(t1, at_vs, t2, True).return_odds()
                    prevWinner_prcnt_arr = prevWinner_arr[0]
                    if prevWinner_prcnt_arr[0] == -1 or prevWinner_prcnt_arr[1] == -1:
                        continue
                    #
                    decoded_t1 = urllib.parse.unquote_plus(t1)
                    decoded_t2 = urllib.parse.unquote_plus(t2)
                    
                    if analyzeMH_arr[0] > analyzeMH_arr[1]:
                        AMHwinner = decoded_t1
                        AMHwinner_percent = analyzeMH_arr[0]
                        winner_risk = risk_arr[0]
                        loser_risk = risk_arr[1]
                    else:
                        AMHwinner = decoded_t2
                        AMHwinner_percent = analyzeMH_arr[1]
                        winner_risk = risk_arr[1]
                        loser_risk = risk_arr[0]
                        
                    if prevWinner_prcnt_arr[0] > prevWinner_prcnt_arr[1]:
                        prevWinnerWinner = decoded_t1
                        prevWinnerWinner_percent = prevWinner_prcnt_arr[0]
                    else:
                        prevWinnerWinner = decoded_t2
                        prevWinnerWinner_percent = prevWinner_prcnt_arr[1]
                    
                    if AMHwinner == winner:
                        amh_correct += 1
                        insert_data_arr.append(winner_risk)
                        insert_data_arr.append(loser_risk)
                        insert_data_arr.append(1)
                    else:
                        insert_data_arr.append(loser_risk)
                        insert_data_arr.append(winner_risk)
                        insert_data_arr.append(0)
                    
                    if prevWinnerWinner == winner:
                        insert_data_arr.append(1)
                        prevWinner_correct += 1
                    else:
                        insert_data_arr.append(0)
                    
                    if prevWinnerWinner == AMHwinner:
                        safe_bet_count += 1
                        if AMHwinner == winner:
                            safe_bet_correct += 1
                            insert_data_arr.append(1)
                        else:
                            insert_data_arr.append(0)
                    else:
                        insert_data_arr.append(-1)
                    
                    if prevWinnerWinner == AMHwinner and AMHwinner_percent > 59.99:
                        super_safe_bet_count += 1
                        if AMHwinner == winner:
                            super_safe_bet_correct += 1
                            insert_data_arr.append(1)
                        else:
                            insert_data_arr.append(0)
                    else:
                        insert_data_arr.append(-1)
                    
                    insert_data_arr.append(AMHwinner_percent)
                    insert_data_arr.append(prevWinnerWinner_percent)
                    sqlDBmanage.SQLdbManage(insert_data_array=insert_data_arr)
                    match_counter += 1
                except Exception as e:
                    print(t1, at_vs, t2, '<> had a bug <>')
    # calculations after loop
    AMH_acc = float(amh_correct) / float(match_counter)
    sb_accuracy = float(safe_bet_correct) / float(safe_bet_count)
    percent_of_games_bet_on = float(safe_bet_count) / float(match_counter)
    supa_safe = float(super_safe_bet_correct) / float(super_safe_bet_count)
    percent_games_supa_safe = float(super_safe_bet_count) / float(match_counter)
    prevwinner_accuracy = float(prevWinner_correct) / float(match_counter)
    
    return sb_accuracy, percent_of_games_bet_on, AMH_acc, supa_safe, percent_games_supa_safe, prevwinner_accuracy
 
def optimize_Trank_value():
    accuracy_best = 0.0
    accuracy_best_trank = 0.0
    trank_value = 4.80
    for i in range(0, 35):
        start_time = time.time()
        update_value('TRank', trank_value)
        tranks_accuracy = run_the_nums()
        accuracy_ = float(tranks_accuracy)
        if accuracy_ > accuracy_best:
            accuracy_best = accuracy_
            accuracy_best_trank = trank_value
        end_time = time.time() - start_time
        min, sec = divmod(end_time, 60)
        print(f'Ran in {min:.0f}:{sec:.0f} | TRANK = {trank_value:.2f}, accuracy: {accuracy_} | Best: {accuracy_best:.5f}, TRANK={trank_value:.2f}')
        trank_value += 0.15
    print(f'Finished TRANK Optimization\nBest accuracy = {accuracy_best} with trank equal to: {accuracy_best_trank}')

def optimize_HomeAway_value():
    accuracy_best = 0.7078947368421052
    accuracy_best_homeaway = 0.0
    homeaway_value = 2.90
    for i in range(0, 20):
        start_time = time.time()
        update_value('HomeAway', homeaway_value)
        homeaway_accuracy = run_the_nums()
        accuracy_ = float(homeaway_accuracy)
        if accuracy_ > accuracy_best:
            accuracy_best = accuracy_
            accuracy_best_homeaway = homeaway_value
        end_time = time.time() - start_time
        min, sec = divmod(end_time, 60)
        print(f'Ran in {min:.0f}:{sec:.0f} | HNA = {homeaway_value:.2f}, accuracy: {accuracy_} | Best: {accuracy_best}, HNA={accuracy_best_homeaway:.2f}')
        homeaway_value += 0.15
    print(f'Finished HNA Optimization\nBest accuracy = {accuracy_best} with HNA equal to: {accuracy_best_homeaway}')

def optimize_HomeAway_value():
    accuracy_best = 0.7078947368421052
    accuracy_best_homeaway = 0.0
    homeaway_value = 2.90
    for i in range(0, 20):
        start_time = time.time()
        update_value('HomeAway', homeaway_value)
        homeaway_accuracy = run_the_nums()
        accuracy_ = float(homeaway_accuracy)
        if accuracy_ > accuracy_best:
            accuracy_best = accuracy_
            accuracy_best_homeaway = homeaway_value
        end_time = time.time() - start_time
        min, sec = divmod(end_time, 60)
        print(f'Ran in {min:.0f}:{sec:.0f} | HNA = {homeaway_value:.2f}, accuracy: {accuracy_} | Best: {accuracy_best}, HNA={accuracy_best_homeaway:.2f}')
        homeaway_value += 0.15
    print(f'Finished HNA Optimization\nBest accuracy = {accuracy_best} with HNA equal to: {accuracy_best_homeaway}')

def optimize_MatchHist_value():
    accuracy_best = 0.0
    accuracy_best_matchHist = 0.0
    matchhist_value = 5.0
    for i in range(0, 33):
        start_time = time.time()
        update_value('MatchHist', matchhist_value)
        matchhist_accuracy = run_the_nums()
        accuracy_ = float(matchhist_accuracy)
        if accuracy_ > accuracy_best:
            accuracy_best = accuracy_
            accuracy_best_matchHist = matchhist_value
        end_time = time.time() - start_time
        min, sec = divmod(end_time, 60)
        print(f'Ran in {min:.0f}:{sec:.0f} | MHIST = {matchhist_value:.2f}, accuracy: {accuracy_} | Best: {accuracy_best}, MHIST={accuracy_best_matchHist:.2f}')
        matchhist_value += 0.40
    print(f'Finished MHIS Optimization\nBest accuracy = {accuracy_best} with MHIST equal to: {accuracy_best_matchHist}')

def optimize_PrevWinner_value():
    accuracy_best_percent = 0.0
    accuracy_best_value = 0.0
    prevWinner_value = 0.2
    for i in range(0, 10):
        start_time = time.time()
        update_value('prevPrevYear', prevWinner_value)
        prevwinner_accuracy = run_the_nums()
        accuracy_ = float(prevwinner_accuracy)
        if accuracy_ > accuracy_best_percent:
            accuracy_best_percent = accuracy_
            accuracy_best_value = prevWinner_value
        end_time = time.time() - start_time
        min, sec = divmod(end_time, 60)
        print(f'Ran in {min:.0f}:{sec:.0f} | PRY = {prevWinner_value:.2f}, accuracy: {accuracy_} | Best: {accuracy_best_percent}, PRY={accuracy_best_value:.2f}')
        prevWinner_value += 0.02
    print(f'Finished PrevWinner Optimization\nBest accuracy = {accuracy_best_percent} with PrevYear equal to: {accuracy_best_value}')
    
   
# hd.CommonFunctions().clear_game_sched_file()
# rg.CommonScrapes().game_winners('20250225')
# import time
# time.sleep(2)
# optimize_PrevWinner_value()
sb_acc, pgb_on, amh_acc, supa_safe_Acc, pgb_on_supasafe, prevwinner_acc = run_the_nums()
sb_acc *= 100
pgb_on *=100
amh_acc *= 100
supa_safe_Acc *= 100
pgb_on_supasafe *= 100
prevwinner_acc *= 100
print(f'Safe Bet Accuracy: {sb_acc:.5f}%\nGames considered a safe bet: {pgb_on:.3f}%\nAMH accuracy: {amh_acc:.5f}%\nPrevWinner accuracy: {prevwinner_acc:.5f}%\nSuper safe accuracy: {supa_safe_Acc:.5f}%\nGames considered supa safe: {pgb_on_supasafe:.4f}%')