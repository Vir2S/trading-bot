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

# Check to see if the regular market is open
if robo_trade.regular_market_open:
    print('Regular Market Open')
else:
    print('Regular Market Not Open')

# Check to see if the pre market is open
if robo_trade.pre_market_open:
    print('Pre Market Open')
else:
    print('Pre Market Not Open')

# Check to see if the post market is open
if robo_trade.post_market_open:
    print('Post Market Open')
else:
    print('Post Market Not Open')

# Grab the current quotes in portfolio
current_quotes = robo_trade.grab_current_quotes()
pprint.pprint(current_quotes)

# Define date range
end_date = datetime.today()
start_date = end_date - timedelta(days=30)

# Grab the historical prices
historical_prices = robo_trade.grab_historical_prices(
    start=start_date,
    end=end_date,
    bar_size=1,
    bar_type='minute'
)
