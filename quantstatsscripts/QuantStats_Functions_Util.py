
import pandas as pd
def read_return_csv_file(file_path, header=True):
    if header:
        data_frame = pd.read_csv(file_path)
    else:
        data_frame = pd.read_csv(file_path, header=None)
        data_frame.columns = ['date', 'return']
    data_frame['date'] = pd.to_datetime(data_frame['date'])
    print(data_frame['date'].dtype)  # This should print datetime64[ns]
    data_frame = data_frame.sort_values(by='date')
    return data_frame

def dataframe_to_series(data_frame):
    # Ensure the 'date' column is in datetime format
    data_frame['date'] = pd.to_datetime(data_frame['date'])
    # Set the 'date' column as the index
    data_frame.set_index('date', inplace=True)
    # Convert the DataFrame to a Series
    data_series = data_frame['return']
    return data_series