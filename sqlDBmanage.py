import sqlite3

class SQLdbManage:
    def __init__(self, insert_data_array):
        self.insert_to_sql(insert_data_array)
    
    def insert_to_sql(self, insert_data_arr):
        conn = sqlite3.connect('database/matchtracker.db')
        cursor = conn.cursor()
        insert_sql = f'''
        INSERT INTO "prediction_history" ("match_id", "winner_risk", "loser_risk",
            "analyze_mh", "prevWinner", "safe_bet", "super_safe_bet",
            "analyze_mh_percent", "prevWinner_percent") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        conn.execute(insert_sql, insert_data_arr)
        conn.commit()
        conn.close()