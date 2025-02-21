import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('database/matchtracker.db')
cursor = conn.cursor()

# Execute a query to select all data from the table
cursor.execute("SELECT * FROM prediction_history")

# Fetch all rows from the executed query
rows = cursor.fetchall()

#vars
total_games = 0
amh_correct = 0
prevwinner_correct = 0
twostar_total = 0
twostar_correct = 0
threestar_total = 0
threestar_correct = 0


arr = [0] * 100
def append_to_range(value, mh_val):
    for i in range(51, 101):
        num = float(i)
        if value < num:
            print(value, i)
            arr[i-51] = arr[i-51] + mh_val
            arr[i-1] = arr[i-1] + 1
            break
            
arr_m = [0] * 20
def do_math(val, mh_val):
    for i in range(51, 101):
        num = float(i)
        if i % 5 == 0:
            if val < num:
                append_val = i-50
                append_val /= 5
                append_val -= 1
                append_val_win_loss = int(append_val)
                append_val_total = append_val_win_loss + 10
                arr_m[append_val_win_loss] = arr_m[append_val_win_loss] + mh_val
                arr_m[append_val_total] += 1
                break

# Loop through each row and get each value
for row in rows:
    match_id = row[0]
    winner_risk = row[1]
    loser_risk = row[2]
    analyze_mh = row[3]
    prevWinner = row[4]
    safe_bet = row[5]
    super_safe_bet = row[6]
    analyze_mh_percent = row[7]
    prevWinner_percent = row[8]
    
    # Logic
    if analyze_mh == 1:
        amh_correct += 1
    
    if prevWinner == 1:
        prevwinner_correct += 1
    
    if safe_bet != -1:
        twostar_total += 1
        if safe_bet == 1:
            twostar_correct += 1
    
    if super_safe_bet != -1:
        threestar_total += 1
        if super_safe_bet == 1:
            threestar_correct += 1
    
    # Increment total
    total_games += 1
    do_math(analyze_mh_percent, analyze_mh)

def every_five_prcnt_accuracy():
    prcnt = 50
    prcnt2 = 55
    for i in range(0, len(arr_m)):
        if i < 10:
            wins = float(arr_m[i])
            total = float(arr_m[i+10])
            accuracy = (wins / total) * 100
            print(f'{prcnt}%-{prcnt2}% - {wins:.0f} / {total:.0f} = {accuracy:.3f}%')
            prcnt2 += 5
            prcnt += 5
    
def check_percent():
    percent = input('what are winners odds %: ')
    percent_float = float(percent)
    
    total_matches = 0
    prevwinner_true_matches = 0
    correct_matches_prevwin = 0
    correct_amh_only = 0
    
    
    for row in rows:
        match_id = row[0]
        winner_risk = row[1]
        loser_risk = row[2]
        analyze_mh = row[3]
        prevWinner = row[4]
        safe_bet = row[5]
        super_safe_bet = row[6]
        analyze_mh_percent = row[7]
        prevWinner_percent = row[8]
        
        if percent_float < (analyze_mh_percent + 1.51) and percent_float > (analyze_mh_percent - 1.51):
            # In range!
            total_matches += 1
            if prevWinner == analyze_mh:
                prevwinner_true_matches += 1
                if analyze_mh == 1:
                    correct_matches_prevwin += 1
            if analyze_mh == 1:
                correct_amh_only += 1
            
    # maths
    prev_and_amh_prcnt = (correct_matches_prevwin / prevwinner_true_matches) * 100
    amh_prcnt = (correct_amh_only / total_matches) * 100
    print(f'If PWM == AMHM Prediction, Odds = {prev_and_amh_prcnt:.3f}%, Sample={prevwinner_true_matches}')
    print(f'AMHM Accuracy is {amh_prcnt:.3f}%, Sample={total_matches}')
    
   
# Get %s
amh_percent = (amh_correct / total_games) * 100
prev_percent = (prevwinner_correct / total_games) * 100
twostar_percent = (twostar_correct / twostar_total) * 100
threestar_percent = (threestar_correct / threestar_total) * 100
twostar_totalgames_percent = (twostar_total / total_games) * 100
threestar_totalgames_percent = (threestar_total / total_games) * 100

# print data
def print_123_star():
    print(f'1 Star Accuracy (AMH Model): {amh_percent:.2f}%')
    print(f'Prev Winner Model Accuracy: {prev_percent:.2f}%')
    print(f'2 Star Accuracy: {twostar_percent:.2f}%')
    print(f'% of games considered "2 Star": {twostar_totalgames_percent:.2f}%')
    print(f'3 Star Accuracy: {threestar_percent:.2f}%')
    print(f'% of games considered "3 Star": {threestar_totalgames_percent:.2f}%')
    print(f'Total games in data: {total_games}')

# Close the connection
conn.close()

# Choose methods you want to run!
# print_123_star()
# every_five_prcnt_accuracy()
check_percent()
