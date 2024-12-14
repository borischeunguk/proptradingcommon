import json
import pandas as pd
from jsonpath_ng import parse

def process_json_with_path(json_file_path, json_path_expr):
    # Load the JSON data
    with open(json_file_path) as f:
        data = json.load(f)

    # Parse the JSON path expression
    jsonpath_expr = parse(json_path_expr)

    # Extract data using the JSON path
    extracted_data = [match.value for match in jsonpath_expr.find(data)]

    # Convert the extracted data to a DataFrame
    earnings_df = pd.DataFrame.from_dict(extracted_data[0], orient='index')

    # Convert index to datetime
    earnings_df.index = pd.to_datetime(earnings_df.index)
    earnings_df.sort_index(inplace=True)

    return earnings_df