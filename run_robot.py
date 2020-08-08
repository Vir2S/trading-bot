import time as true_time
import pprint
import pathlib
import operator
import pandas as pd

from datetime import datetime, timedelta
from configparser import ConfigParser

from robotrade.robot import Robot
from robotrade.indicators import Indicators

# Grab the config file values
config = ConfigParser()
config.read('robotrade/configs/config.ini')

CLIENT_ID = config.get('main', 'CLIENT_ID')
REDIRECT_URI = config.get('main', 'REDIRECT_URI')
CREDENTIALS_PATH = config.get('main', 'JSON_PATH')
ACCOUNT_NUMBER = config.get('main', 'ACCOUNT_NUMBER')

# Initialize the robot
robo_trade = Robot(
    client_id=CLIENT_ID,
    redirect_uri=REDIRECT_URI,
    credentials_path=CREDENTIALS_PATH,
    trading_account=ACCOUNT_NUMBER,
    paper_trading=True
)

# Create a new portfolio
robo_trade_portfolio = robo_trade.create_portfolio()

# Add multiple positions to portfolio
multi_position = {
    {
        'asset_type': 'equity',
        'quantity': 2,
        'purchase_price': 4.00,
        'symbol': 'TSLA',
        'purchase_date': '2020-08-08'
    },
    {
        'asset_type': 'equity',
        'quantity': 2,
        'purchase_price': 4.00,
        'symbol': 'SQ',
        'purchase_date': '2020-08-08'
    }
}

# Add those positions to the Portfolio
new_positions = robo_trade.portfolio.add_positions(positions=multi_position)
pprint.pprint(new_positions)

# Add a single position to the portfolio
robo_trade.portfolio.add_position(
    symbol='MSFT',
    quantity=10,
    purchase_price=10.00,
    purchase_date='2020-08-08',
    asset_type='equity'
)

pprint.pprint(robo_trade.portfolio.positions)

