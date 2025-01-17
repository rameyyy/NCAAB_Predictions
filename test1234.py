import sqlite3

conn = sqlite3.connect('matchtracker.db')
cursor = conn.cursor()

data1 = 'test123'
data2 = 60.231
data3 = 39.861

insert_sql = f'''
INSERT INTO "prediction_history" ("match_id", "winner_risk", "loser_risk",
    "analyze_mh", "prevWinner", "safe_bet", "super_safe_bet",
    "analyze_mh_percent", "prevWinner_percent") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
'''
data_insert = ['test', 21.2, 121.22, 1, 0, 0, 0, 1, 1]

conn.execute(insert_sql, data_insert)

conn.commit()
conn.close()