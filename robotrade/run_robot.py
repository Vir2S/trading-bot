import time as true_time
import pprint
import pathlib
import operator
import pandas as pd

from datetime import datetime, timedelta
from configparser import ConfigParser

from robot.robot import Robot
from robot.indicators import Indicators

# Grab the config file values
config = ConfigParser()
config.read('config/config.ini')

CLIENT_ID = config.get('main', 'CLIENT_ID')
REDIRECT_URI = config.get('main', 'REDIRECT_URI')
CREDENTIALS_PATH = config.get('main', 'JSON_PATH')
ACCOUNT_NUMBER = config.get('main', 'ACCOUNT_NUMBER')

# Initialize the robot
robotrade = Robot(
    client_id=CLIENT_ID,
    redirect_uri=REDIRECT_URI,
    credentials_path=CREDENTIALS_PATH,
    trading_account=ACCOUNT_NUMBER,
    paper_trading=True
)
