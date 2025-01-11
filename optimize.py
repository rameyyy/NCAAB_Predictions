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
    predicted_correct = 0 
    match_counter = 0
    safe_bets = 0
    risk_avg_yes = 0
    risk_avg_no = 0
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
                    ## data = return if optimizing analyze math hist
                    analyzeMH_arr = hd.AnalyzeMatchHist(t1, at_vs, t2, True).return_odds()
                    #
                    risk_arr = hd.AccuracyEstimate(t1, at_vs, t2, True).return_odds()
                    # data = return if optimizing prev winner
                    prevWinner_arr = hd.PrevWinner(t1, at_vs, t2, True).return_odds()
                    data = prevWinner_arr[0]
                    if data[0] == -1 or data[1] == -1:
                        continue
                    #

                    matchHistWinner = ''
                    decoded_t1 = urllib.parse.unquote_plus(t1)
                    decoded_t2 = urllib.parse.unquote_plus(t2)
                    ## MH Part
                    if analyzeMH_arr[0] > analyzeMH_arr[1]:
                        AMH_winner = decoded_t1
                    else:
                        AMH_winner = decoded_t2
                    ##
                    if data[0] > data[1]:
                        matchHistWinner = decoded_t1
                    else:
                        matchHistWinner = decoded_t2
                    ## safe bet feature ##
                    risk_value = risk_arr[0] + risk_arr[1]
                    if AMH_winner == matchHistWinner and risk_value > 2:
                        safe_bets += 1
                        safe_bet_bool = True
                    else: safe_bet_bool = False
                    if safe_bet_bool == True:
                        if winner == matchHistWinner:
                            predicted_correct += 1
                    match_counter += 1
                except Exception as e:
                    pass
    sb_accuracy = float(predicted_correct) / float(safe_bets)
    percent_of_games_bet_on = float(safe_bets) / float(match_counter)
    
    return sb_accuracy, percent_of_games_bet_on
 
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
    
# optimize_PrevWinner_value()
sb_acc, pgb_on = run_the_nums()
sb_acc *= 100
pgb_on *=100
print(f'Safe Bet Accuracy: {sb_acc:.5f}%\nGames considered a safe bet: {pgb_on:.3f}%')