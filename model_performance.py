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
    
    
# Get %s
amh_percent = (amh_correct / total_games) * 100
prev_percent = (prevwinner_correct / total_games) * 100
twostar_percent = (twostar_correct / twostar_total) * 100
threestar_percent = (threestar_correct / threestar_total) * 100
twostar_totalgames_percent = (twostar_total / total_games) * 100
threestar_totalgames_percent = (threestar_total / total_games) * 100

# print data
print(f'1 Star Accuracy (AMH Model): {amh_percent:.2f}%')
print(f'Prev Winner Model Accuracy: {prev_percent:.2f}%')
print(f'2 Star Accuracy: {twostar_percent:.2f}%')
print(f'% of games considered "2 Star": {twostar_totalgames_percent:.2f}%')
print(f'3 Star Accuracy: {threestar_percent:.2f}%')
print(f'% of games considered "3 Star": {threestar_totalgames_percent:.2f}%')
print(f'Total games in data: {total_games}')

# Close the connection
conn.close()