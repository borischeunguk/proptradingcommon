import datetime
import os

from eodhdscripts.Eodhd_Functions_Util import process_json_with_path, reformat_json

print(os.getcwd())
product_code = 'AAPL'

# Specify the JSON file path and JSON path expression,
# use reformat_json function or https://jsonformatter.org/ to reformat the JSON file
json_path_expr = 'Earnings.History'

# Save the DataFrame to a CSV file
now = datetime.datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")  # e.g., 20240203_123456

# Specify the input and output file paths
input_file_path = os.path.join(os.getcwd(), f'../resources/fundamental/{product_code}.json')
output_file_path = os.path.join(os.getcwd(), f'../resources/fundamental/{product_code}_Nice_Format_{timestamp}.json')

# Reformat the JSON file
reformat_json(input_file_path, output_file_path)

# Process the JSON file with the specified JSON path
earnings_df = process_json_with_path(output_file_path, json_path_expr)

json_path_expr = json_path_expr.replace('.', '_')
csv_file_name = f"results/{product_code}_{json_path_expr}_{timestamp}.csv"
earnings_df.to_csv(csv_file_name)