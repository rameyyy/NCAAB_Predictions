import sqlite3

class MatchOdds:
    def __init__(self, percent, two_star_bool):
        # Connect to the SQLite database
        conn = sqlite3.connect('database/matchtracker.db')
        cursor = conn.cursor()
        
        # Execute a query to select all data from the table
        cursor.execute("SELECT * FROM prediction_history")

        # Fetch all rows from the executed query
        self.rows = cursor.fetchall()
        self.percent = percent
        self.two_star_bool = two_star_bool
    
    def get_match_odds(self):
        percent_float = float(self.percent)
        
        total_matches = 0
        prevwinner_true_matches = 0
        correct_matches_prevwin = 0
        correct_amh_only = 0
        percents_total = 0
        
        
        for row in self.rows:
            match_id = row[0]
            winner_risk = row[1]
            loser_risk = row[2]
            analyze_mh = row[3]
            prevWinner = row[4]
            safe_bet = row[5]
            super_safe_bet = row[6]
            analyze_mh_percent = row[7]
            prevWinner_percent = row[8]
            
            if percent_float < (analyze_mh_percent + 1) and percent_float > (analyze_mh_percent - 1.5):
                # In range!
                total_matches += 1
                percents_total += analyze_mh_percent
                if prevWinner == analyze_mh:
                    prevwinner_true_matches += 1
                    if analyze_mh == 1:
                        correct_matches_prevwin += 1
                if analyze_mh == 1:
                    correct_amh_only += 1
                
        # maths
        results = []
        if total_matches > 0:
            percent_diff = percent_float - (percents_total / total_matches)
            amh_prcnt = (correct_amh_only / total_matches) * 100
            results.append(amh_prcnt)
            results.append(total_matches)
            results.append(percent_diff)
        if prevwinner_true_matches > 0:
            prev_and_amh_prcnt = (correct_matches_prevwin / prevwinner_true_matches) * 100
            results.append(prev_and_amh_prcnt)
            results.append(prevwinner_true_matches)
        return results