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
    
    def american_to_decimal(self, american_odds):
        try:
            odds = int(american_odds)
        except ValueError:
            return None  # Handle invalid input

        if odds > 0:
            return (odds / 100) + 1
        elif odds < 0:
            return (100 / abs(odds)) + 1
        else:
            return 1.0  # Even odds
    
    def calculate_expected_value(self, odds, stake, probability):
        potential_profit = (odds - 1) * stake
        expected_value = (probability * potential_profit) - ((1 - probability) * stake)
        return expected_value
    
    def find_lowest_return_positive_EV(self, percent):
        american_odds = -505
        for i in range(0,80): # -500 to -105
            decimal_odds = self.american_to_decimal(american_odds)
            percent /= 100
            EV = self.calculate_expected_value(decimal_odds, 1, percent)
            if EV > .09:
                print(f'decimal_odds, EV {self.percent}')
                print(f'+EV if greater than or equal to {american_odds}')
                break
            american_odds += 5
        print('not + EV')
