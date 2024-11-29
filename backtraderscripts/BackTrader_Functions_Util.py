import numpy as np
import pandas as pd
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def pre_minus_current(array):
    return np.abs(np.diff(array, prepend=np.nan))

def write_trades_to_csv(trades, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=trades[0].keys())
        writer.writeheader()
        for trade in trades:
            writer.writerow(trade)
def read_csv_file(file_path, header=True):
    if header:
        data_frame = pd.read_csv(file_path)
    else:
        data_frame = pd.read_csv(file_path, header=None)
        data_frame.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    data_frame['date'] = pd.to_datetime(data_frame['date'])
    print(data_frame['date'].dtype)  # This should print datetime64[ns]
    data_frame = data_frame.sort_values(by='date')
    return data_frame

def display_dict(d, indent=0, logger=None):
    if d is None:
        if logger:
            logger.warning('display_dict: d is None')
        else:
            print('display_dict: d is None')
        return

    for key, value in d.items():
        if isinstance(value, dict):
            if logger:
                logger.info('  ' * indent + str(key))
            else:
                print('  ' * indent + str(key))
            display_dict(value, indent+1, logger = logger)
        else:
            if logger:
                logger.info('  ' * indent + str(key) + ': ' + str(value))
            else:
                print('  ' * indent + str(key) + ': ' + str(value))

def extract_and_print_daily_return(results, product_strategy_name, timestamp):
    daily_returns = results[0].analyzers.daily_return.get_analysis()
    print("Daily Returns:")
    for date, return_value in daily_returns.items():
        print(f"{date}: {return_value}")
    daily_returns_df = pd.DataFrame(list(daily_returns.items()), columns=['date', 'return'])
    daily_returns_df['date'] = pd.to_datetime(daily_returns_df['date'])
    daily_returns_df.set_index('date', inplace=True)

    daily_return_file_name = f"results/{product_strategy_name}_daily_return"
    daily_return_file_name_timestamp = f'{daily_return_file_name}_{timestamp}.csv'
    daily_returns_df.to_csv(daily_return_file_name_timestamp)

def extract_and_print_monthly_return(results, product_strategy_name, timestamp):
    # Extract and print monthly returns
    monthly_returns = results[0].analyzers.monthly_return.get_analysis()
    print("Monthly Returns:")
    for date, return_value in monthly_returns.items():
        print(f"{date}: {return_value}")
    monthly_returns_df = pd.DataFrame(list(monthly_returns.items()), columns=['date', 'return'])
    monthly_returns_df['date'] = pd.to_datetime(monthly_returns_df['date'])
    monthly_returns_df.set_index('date', inplace=True)

    monthly_return_file_name = f"results/{product_strategy_name}_monthly_return"
    monthly_return_file_name_timestamp = f'{monthly_return_file_name}_{timestamp}.csv'
    monthly_returns_df.to_csv(monthly_return_file_name_timestamp)

def send_email(subject, body):
    sender_email = "bo.zhang@icloud.com"
    receiver_email = "bozhang.ox@gmail.com"
    # Please note this is App Specific Password:
    # Steps to Find App-Specific Passwords:
    # On iCloud.com (via a browser):
    # Go to appleid.apple.com.
    # Sign in with your Apple ID.
    # In the Security section, you'll see an option for App-Specific Passwords.
    # Click Generate Password to create one.
    password = "****-****-****"        # Your email password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.mail.me.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
    except Exception as e:
        print(f"Failed to send email: {e}")