file_path_to_path = '$HOME/projects/NCAAB_Predictions/database/paths.json'
date_str_ = '20250306'
date_for_txt_file = '03-06-2025'
import reportgen
rg = reportgen
rg.initialize_path(file_path_to_path)
rg.CommonScrapes().get_schedule_set_date(date_str_)
rg.CurrentDayScrape(date_str_).scrape_all(True)
rg.CurrentDayReport().generate_report(False, True, f'{date_for_txt_file}_match_predictions.txt', True)