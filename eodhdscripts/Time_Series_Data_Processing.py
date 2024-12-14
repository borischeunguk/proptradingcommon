import datetime
import os

from eodhdscripts.Eodhd_Functions_Util import process_json_with_path

# Specify the JSON file path and JSON path expression, use https://jsonformatter.org/ to reformat the JSON file
json_path_expr = 'Earnings.History'

# Load the JSON file
print(os.getcwd())
product_code = 'AAPL'
fundamental_file_path = f"{product_code}.json"
json_file_path = os.getcwd() + '/../resources/fundamental/' + fundamental_file_path

# Process the JSON file with the specified JSON path
earnings_df = process_json_with_path(json_file_path, json_path_expr)

# Save the DataFrame to a CSV file
now = datetime.datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")  # e.g., 20240203_123456
json_path_expr = json_path_expr.replace('.', '_')
csv_file_name = f"results/{product_code}_{json_path_expr}_{timestamp}.csv"
earnings_df.to_csv(csv_file_name)