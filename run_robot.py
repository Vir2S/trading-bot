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

# Convert the data into a StockFrame
stock_frame = robo_trade.create_stock_frame(data=historical_prices['aggregated'])

# Print the head of StockFrame
pprint.pprint(stock_frame.frame.head(n=20))

# Create a new Trade Object.
new_trade = robo_trade.create_trade(
    trade_id='long_msft',
    enter_or_exit='enter',
    long_or_short='long',
    order_type='lmt',
    price=150.00
)

# Make it Good Till Cancel.
new_trade.good_till_cancel(cancel_time=datetime.now() + timedelta(minutes=90))

# Change the session
new_trade.modify_session(session='am')

# Add an Order Leg.
new_trade.instrument(
    symbol='MSFT',
    quantity=2,
    asset_type='EQUITY'
)

# Add a Stop Loss Order with the Main Order.
new_trade.add_stop_loss(
    stop_size=.10,
    percentage=False
)

# Print out the order.
pprint.pprint(new_trade.order)

# Create a new indicator client
indicator_client = Indicators(price_data_frame=stock_frame)

# Add the RSI indicator
indicator_client.rsi(period=14)

# Add a 200-day simple moving average
indicator_client.sma(period=200)

# Add a 50-day exponential moving average
indicator_client.ema(period=50)

# Add a signal to check for
indicator_client.set_indicator_signals(
    indicator='rsi',
    buy=40.0,
    sell=20.0,
    condition_buy=operator.ge,
    condition_sell=operator.le
)

# Define a trade dictionary
trades_dict = {
    'MSFT': {
        'trade_frame': robo_trade.trades['long_msft'],
        'trade_id': robo_trade.trades['long_msft'].trade_id
    }
}

while True:

    # Grab the latest bar
    latest_bar = robo_trade.get_latest_bar()

    # Add those bars to the StockFrame
    stock_frame.add_rows(data=latest_bar)

    # Refresh the indicators
    indicator_client.refresh()

    # Check for signals
    signals = indicator_client.get_indicator_signals()

    # Grab the last bar, keep in mind this is after adding the new rows
    last_bar_timestamp = robo_trade.stock_frame.frame.tail(1).get_level_values(1)

    # Wait till the next bar
    robo_trade.wait_till_next_bar(last_bar_timestamp=last_bar_timestamp)
