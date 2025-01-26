import os
import zipfile
import pandas as pd

# Define the directory containing the zip files
data_dir_str = '../resources/'
market_data_type = 'china_csi_500_stock_future_202410_202411_1min'
product_name = 'IC'
product_name = 'IF'
product_name = 'IH'
product_name = 'T'
product_name = 'TF'
product_name = 'TS'
product_name = 'TL'
zip_dir = os.path.join(os.getcwd(), data_dir_str, market_data_type, product_name)
combined_csv_path = os.path.join(zip_dir, 'combined_data.csv')

# Create a list to hold dataframes
dataframes = []

# Unzip all files in the directory
for item in os.listdir(zip_dir):
    if item.endswith('.zip'):
        zip_path = os.path.join(zip_dir, item)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(zip_dir)

# Read all CSV files and append to the list of dataframes
for item in os.listdir(zip_dir):
    if item.endswith('.csv'):
        print("csv file: " + str(item))
        csv_path = os.path.join(zip_dir, item)
        df = pd.read_csv(csv_path)
        dataframes.append(df)

# Concatenate all dataframes into one
combined_df = pd.concat(dataframes, ignore_index=True)

# Remove duplicate rows
combined_df.drop_duplicates(inplace=True)

sorted_combined_df = combined_df.sort_values(by='trade_timestamp')

# Save the combined dataframe to a CSV file
# Define the output file name
combined_output_file = f"{market_data_type}_{product_name}_combined.csv"
sorted_combined_df.to_csv(combined_output_file, index=False)
print(f"Combined data saved to {combined_output_file}")

# Group by 'instrument_id'
grouped = sorted_combined_df.groupby('instrument_id')

# Process each group
for instrument_id, group in grouped:
    # Sort the group by 'trade_timestamp'
    sorted_group = group.sort_values(by='trade_timestamp')

    # Define the output file name
    output_file = f"{market_data_type}_{product_name}_{instrument_id}.csv"

    # Save the sorted group to a CSV file
    sorted_group.to_csv(output_file, index=False)
    print(f"Data for {market_data_type} {product_name} {instrument_id} saved to {output_file}")