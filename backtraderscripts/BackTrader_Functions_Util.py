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
    password = "xsfb-yhzc-yxfd-wrrq"        # Your email password

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