import sqlite3
import numpy as np
import scipy.stats as stats

# Define the function to calculate statistics
def calculate_statistics(data):
    data = np.array(data)
    mean = np.mean(data)
    median = np.median(data)
    try:
        mode = stats.mode(data)[0][0]
    except IndexError:
        mode = stats.mode(data)[0]
    std_dev = np.std(data)
    variance = np.var(data)
    data_range = np.ptp(data)
    skewness = stats.skew(data)
    kurtosis = stats.kurtosis(data)
    percentiles = np.percentile(data, [25, 50, 75])
    
    statistics = {
        'Mean': mean,
        'Median': median,
        'Mode': mode,
        'Standard Deviation': std_dev,
        'Variance': variance,
        'Range': data_range,
        'Skewness': skewness,
        'Kurtosis': kurtosis,
        '25th Percentile': percentiles[0],
        '50th Percentile': percentiles[1],
        '75th Percentile': percentiles[2],
    }
    return statistics

# Connect to the SQLite database
conn = sqlite3.connect('database/matchtracker.db')
cursor = conn.cursor()

# Execute a query to select all data from the table
cursor.execute("SELECT * FROM prediction_history")

# Fetch all rows from the executed query
rows = cursor.fetchall()

# Define lists to store the columns separately
match_id = []
winner_risk = []
loser_risk = []
analyze_mh = []
prevWinner = []
safe_bet = []
super_safe_bet = []
analyze_mh_percent = []
prevWinner_percent = []

# Loop through the rows and append the values to the lists
for row in rows:
    match_id.append(row[0])
    winner_risk.append(row[1])
    loser_risk.append(row[2])
    analyze_mh.append(row[3])
    prevWinner.append(row[4])
    safe_bet.append(row[5])
    super_safe_bet.append(row[6])
    analyze_mh_percent.append(row[7])
    prevWinner_percent.append(row[8])

# Define a function to separate data based on prediction outcomes
def separate_data_based_on_prediction_outcomes(risk_values, predictions):
    correct_risk = [risk_values[i] for i in range(len(predictions)) if predictions[i] == 1]
    incorrect_risk = [risk_values[i] for i in range(len(predictions)) if predictions[i] == 0]
    na_risk = [risk_values[i] for i in range(len(predictions)) if predictions[i] == -1]
    return correct_risk, incorrect_risk, na_risk

# Separate data and calculate statistics for each prediction model
prediction_models = {
    'Analyze MH': analyze_mh,
    'Prev Winner': prevWinner,
    'Safe Bet': safe_bet,
    'Super Safe Bet': super_safe_bet
}

for model_name, predictions in prediction_models.items():
    print(f"\n{model_name} Predictions:")
    
    winner_correct, winner_incorrect, winner_na = separate_data_based_on_prediction_outcomes(winner_risk, predictions)
    loser_correct, loser_incorrect, loser_na = separate_data_based_on_prediction_outcomes(loser_risk, predictions)
    
    print("\nWinner Risk (Correct Predictions):")
    print(calculate_statistics(winner_correct))
    print("\nWinner Risk (Incorrect Predictions):")
    print(calculate_statistics(winner_incorrect))
    print("\nWinner Risk (N/A Predictions):")
    print(calculate_statistics(winner_na))
    
    print("\nLoser Risk (Correct Predictions):")
    print(calculate_statistics(loser_correct))
    print("\nLoser Risk (Incorrect Predictions):")
    print(calculate_statistics(loser_incorrect))
    print("\nLoser Risk (N/A Predictions):")
    print(calculate_statistics(loser_na))

# Close the connection
conn.close()