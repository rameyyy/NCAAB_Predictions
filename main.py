file_path_to_path = '$HOME/projects/NCAAB_Predictions/database/paths.json'
import reportgen
rg = reportgen
rg.initialize_path(file_path_to_path)
rg.CurrentDayScrape().scrape_all(True)
rg.CurrentDayReport().generate_report(True, True, '02-13-2025_match_predictions.txt', True)