import sqlite3
import matplotlib.pyplot as plt
import numpy as np

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

# Separate the data based on prediction outcomes
winner_risk_correct = [winner_risk[i] for i in range(len(analyze_mh)) if analyze_mh[i] == 1]
loser_risk_correct = [loser_risk[i] for i in range(len(analyze_mh)) if analyze_mh[i] == 1]
winner_risk_incorrect = [winner_risk[i] for i in range(len(analyze_mh)) if analyze_mh[i] == 0]
loser_risk_incorrect = [loser_risk[i] for i in range(len(analyze_mh)) if analyze_mh[i] == 0]


# Calculate averages
average_winner_risk_correct = sum(winner_risk_correct) / len(winner_risk_correct)
average_loser_risk_correct = sum(loser_risk_correct) / len(loser_risk_correct)
average_winner_risk_incorrect = sum(winner_risk_incorrect) / len(winner_risk_incorrect)
average_loser_risk_incorrect = sum(loser_risk_incorrect) / len(loser_risk_incorrect)

# Print averages
print(f"Average Winner Risk (Correct Prediction): {average_winner_risk_correct:.2f}")
print(f"Average Loser Risk (Correct Prediction): {average_loser_risk_correct:.2f}")
print(f"Average Winner Risk (Incorrect Prediction): {average_winner_risk_incorrect:.2f}")
print(f"Average Loser Risk (Incorrect Prediction): {average_loser_risk_incorrect:.2f}")

# Create line graphs
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Line graph: Winner Risk - Correct Predictions
axes[0, 0].plot(range(len(winner_risk_correct)), winner_risk_correct, label='Winner Risk (Correct Prediction)', color='green', marker='o')
axes[0, 0].set_title('Winner Risk (Correct Prediction)')
axes[0, 0].set_xlabel('Match Index')
axes[0, 0].set_ylabel('Winner Risk')

# Line graph: Loser Risk - Correct Predictions
axes[0, 1].plot(range(len(loser_risk_correct)), loser_risk_correct, label='Loser Risk (Correct Prediction)', color='blue', marker='o')
axes[0, 1].set_title('Loser Risk (Correct Prediction)')
axes[0, 1].set_xlabel('Match Index')
axes[0, 1].set_ylabel('Loser Risk')

# Line graph: Winner Risk - Incorrect Predictions
axes[1, 0].plot(range(len(winner_risk_incorrect)), winner_risk_incorrect, label='Winner Risk (Incorrect Prediction)', color='red', marker='x')
axes[1, 0].set_title('Winner Risk (Incorrect Prediction)')
axes[1, 0].set_xlabel('Match Index')
axes[1, 0].set_ylabel('Winner Risk')

# Line graph: Loser Risk - Incorrect Predictions
axes[1, 1].plot(range(len(loser_risk_incorrect)), loser_risk_incorrect, label='Loser Risk (Incorrect Prediction)', color='orange', marker='x')
axes[1, 1].set_title('Loser Risk (Incorrect Prediction)')
axes[1, 1].set_xlabel('Match Index')
axes[1, 1].set_ylabel('Loser Risk')

import numpy as np
import scipy.stats as stats

def calculate_and_explain_statistics(data):
    data = np.array(data)
    # Calculate statistics
    mean = np.mean(data)
    median = np.median(data)
    # mode = stats.mode(data)[0][0] if len(data) > 0 else np.nan
    std_dev = np.std(data)
    variance = np.var(data)
    data_range = np.ptp(data)
    skewness = stats.skew(data)
    kurtosis = stats.kurtosis(data)
    percentiles = np.percentile(data, [25, 50, 75])
    
    # Print statistics with explanations
    print(f"Mean: {mean:.2f}")
    print(f" - The mean is the average of the data set. It is significant as it gives a central value to the data.")
    
    print(f"Median: {median:.2f}")
    print(f" - The median is the middle value of the data set when it is ordered. It is significant because it is less affected by outliers and skewed data.")
    
    # print(f"Mode: {mode:.2f}")
    # print(f" - The mode is the value that appears most frequently in the data set. It is significant in understanding the most common value.")
    
    print(f"Standard Deviation: {std_dev:.2f}")
    print(f" - The standard deviation measures the amount of variation or dispersion in the data set. It is significant as it shows how spread out the data points are.")
    
    print(f"Variance: {variance:.2f}")
    print(f" - The variance is the square of the standard deviation. It indicates the degree of spread in the data set.")
    
    print(f"Range: {data_range:.2f}")
    print(f" - The range is the difference between the maximum and minimum values in the data set. It gives a quick sense of the spread of the data.")
    
    print(f"Skewness: {skewness:.2f}")
    print(f" - Skewness measures the asymmetry of the data distribution. Positive skewness indicates a long right tail, while negative skewness indicates a long left tail.")
    
    print(f"Kurtosis: {kurtosis:.2f}")
    print(f" - Kurtosis measures the tailedness of the data distribution. High kurtosis indicates heavy tails (outliers), while low kurtosis indicates light tails.")
    
    print(f"25th Percentile: {percentiles[0]:.2f}")
    print(f" - The 25th percentile (first quartile) is the value below which 25% of the data falls.")
    
    print(f"50th Percentile: {percentiles[1]:.2f}")
    print(f" - The 50th percentile (median) is the value below which 50% of the data falls.")
    
    print(f"75th Percentile: {percentiles[2]:.2f}")
    print(f" - The 75th percentile (third quartile) is the value below which 75% of the data falls.")

print(f'Winner Risk, Prediction Correct!')    
calculate_and_explain_statistics(winner_risk_correct)
print('\n\n')
print(f'Loser Risk, Prediction Correct!')    
calculate_and_explain_statistics(loser_risk_correct)
print('\n\n')
print(f'Winner Risk, Prediction Incorrect!')    
calculate_and_explain_statistics(winner_risk_incorrect)
print('\n\n')
print(f'Loser Risk, Prediction Incorrect!')    
calculate_and_explain_statistics(loser_risk_incorrect)
print('\n\n')

plt.tight_layout()
plt.show()
# Close the connection
conn.close()