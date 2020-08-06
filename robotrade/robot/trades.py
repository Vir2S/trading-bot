from datetime import datetime

from typing import List, Dict, Union, Optional


class Trades():

    def __init__(self):

        self.order = {}
        self.trade_id = ''

        self.side = ''
        self.side_opposite = ''
        self.enter_or_exit = ''
        self.enter_or_exit_opposite = ''

        self.order_response = {}
        self.triggered_added = False
        self.multi_leg = False

    def new_trade(
            self,
            trade_id: str,
            order_type: str,
            side: str,
            enter_or_exit: str,
            price: float = 0.00,
            stop_limit_price: float = 0.00
    ) -> Dict:

        self.trade_id = trade_id

        self.order_types = {
            'mkt': 'MARKET',
            'lmt': 'LIMIT',
            'stop': 'STOP',
            'stop_lmt': 'STOP_LIMIT',
            'trailing_stop': 'TRAILING_STOP'
        }

        self.order_instructions = {
            'enter': {
                'long': 'BUY',
                'short': 'SELL_SHORT'
            },
            'exit': {
                'long': 'SELL',
                'short': 'BUY_TO_COVER'
            }
        }

        self.order = {
            'orderStrategyType': 'SINGLE',
            'orderType': self.order_types[order_type],
            'session': 'NORMAL',
            'duration': 'DAY',
            'orderLegCollection': [
                {
                    'instruction': self.order_instructions[enter_or_exit][side],
                    'quantity': 0,
                    'instrument': {
                        'symbol': None,
                        'assetType': None
                    }
                }
            ]
        }

        if self.order['orderType'] == 'STOP':
            self.order['stopPrice'] = price

        elif self.order['orderType'] == 'LIMIT':
            self.order['price'] = price

        elif self.order['orderType'] == 'STOP_LIMIT':
            self.order['stopPrice'] = price
            self.order['price'] = stop_limit_price

        elif self.order['orderType'] == 'TRAILING_STOP':
            self.order['stopPriceLinkBasis'] = ''
            self.order['stopPriceLinkType'] = ''
            self.order['stopPriceOffset'] = 0.00
            self.order['stopType'] = 'STANDARD'

        self.enter_or_exit = enter_or_exit
        self.side = side
        self.order_type = order_type
        self.price = price

        # Store important info for later use
        if order_type == 'stop':
            self.stop_price = price
        elif order_type == 'stop_lmt':
            self.stop_price = price
            self.stop_limit_price = stop_limit_price
        else:
            self.stop_price = 0.00

        if self.enter_or_exit == 'enter':
            self.enter_or_exit_opposite = 'exit'
        elif self.enter_or_exit == 'exit':
            self.enter_or_exit_opposite = 'enter'

        if self.side == 'long':
            self.side_opposite = 'short'
        elif self.side == 'short':
            self.side_opposite = 'long'

        return self.order

    def instrument(
            self,
            symbol: str,
            quantity: int,
            asset_type: str,
            sub_asset_type: str = None,
            order_leg_id: int = 0
    ) -> Dict:

        leg = self.order['orderLegCollection'][order_leg_id]

        leg['instrument']['symbol'] = symbol
        leg['instrument']['assetType'] = asset_type
        leg['quantity'] = quantity

        self.order_size = quantity
        self.symbol = symbol
        self.asset_type = asset_type

        return leg

    def good_till_cancel(self, cancel_time: datetime) -> None:

        self.order['duration'] = 'GOOD_TILL_CANCEL'
        self.order['cancelTime'] = cancel_time.isoformat()

    def modify_side(self, side: Optional[str], order_leg_id: int = 0) -> None:

        if side and side not in ['buy', 'sell', 'buy_to_cover', 'sell_short']:
            raise ValueError('You passed through an invalid side')

        if side:
            self.side['orderLegCollection'][order_leg_id]['instructions'] = side.upper()
        else:
            self.side['orderLegCollection'][order_leg_id]['instructions'] = \
                self.order_instructions[self.enter_or_exit][self.side_opposite]

    def add_box_range(self, profit_size: float = 0.00, percentage: bool = False, stop_limit: bool = False):

        if not self._triggered_added:
            self._convert_to_trigger()

        self.add_take_profit(profit_size=profit_size, percentage=percentage)

        if not stop_limit:
            self.add_stop_loss(stop_size=profit_size, percentage=percentage)

    def add_stop_loss(self, stop_size: float, percentage: bool = False) -> bool:

        if not self._triggered_added:
            self._convert_to_trigger()

        if self.order_type == 'mkt':
            pass
        elif self.order_type == 'lmt':
            price = self.price

        if percentage:
            adjustment = 1.0 - stop_size
            new_price = self._calculate_new_price(price=price, adjustment=adjustment, percentage=True)
        else:
            adjustment = -stop_size
            new_price = self._calculate_new_price(price=price, adjustment=adjustment, percentage=False)

        # Biuld the order
        stop_loss_order = {
            "orderType": "STOP",
            "session": "NORMAL",
            "duration": "DAY",
            "stopPrice": new_price,
            "orderStrategyType": "SINGLE",
            "orderLegCollection": [
                {
                    "instruction": self.order_instructions[self.enter_or_exit_opposite][self.side],
                    "quantity": self.order_size,
                    "instrument": {
                        "symbol": self.symbol,
                        "assetType": self.asset_type
                    }
                }
            ]
        }

        # Add the order
        self.stop_loss_order = stop_loss_order
        self.order['childOrderStrategies'].append(self.stop_loss_order)

        return True

    def add_stop_limit(
            self,
            stop_size: float,
            limit_size: float,
            stop_percentage: bool = False,
            limit_percentage: bool = False
    ) -> bool:

        if not self._triggered_added:
            self._convert_to_trigger()

        if self.order_type == 'mkt':
            pass
        elif self.order_type == 'lmt':
            price = self.price

        if stop_percentage:
            adjustment = 1.0 - stop_size
            stop_price = self._calculate_new_price(price=price, adjustment=adjustment, percentage=True)
        else:
            adjustment = -stop_size
            stop_price = self._calculate_new_price(price=price, adjustment=adjustment, percentage=False)

        if limit_percentage:
            adjustment = 1.0 - limit_size
            limit_price = self._calculate_new_price(price=price, adjustment=adjustment, percentage=True)
        else:
            adjustment = -limit_size
            limit_price = self._calculate_new_price(price=price, adjustment=adjustment, percentage=False)

            # Build the order
            stop_limit_order = {
            "orderType": "STOP_LIMIT",
            "session": "NORMAL",
            "duration": "DAY",
            "limitPrice": limit_price,
            "stopPrice": stop_price,
            "orderStrategyType": "SINGLE",
            "orderLegCollection": [
                {
                    "instruction": self.order_instructions[self.enter_or_exit_opposite][self.side],
                    "quantity": self.order_size,
                    "instrument": {
                        "symbol": self.symbol,
                        "assetType": self.asset_type
                    }
                }
            ]
        }

        # Add the order
        self.stop_limit_order = stop_limit_order
        self.order['childOrderStrategies'].append(self.stop_limit_order)

        return True

    def _calculate_new_price(self, price: float, adjustment: float, percentage: bool) -> float:

        if percentage:
            new_price = price * adjustment
        else:
            new_price = price + adjustment

        if new_price < 1:
            new_price = round(new_price, 4)
        else:
            new_price = round(new_price, 2)

        return new_price

    def add_take_profit(self, profit_size: float, percentage: bool = False) -> bool:

        if not self._triggered_added:
            self._convert_to_trigger()

        if self.order_type == 'mkt':
            pass
        elif self.order_type == 'lmt':
            price = self.price

        if percentage:
            adjustment = 1.0 - profit_size
            profit_price = self._calculate_new_price(price=price, adjustment=adjustment, percentage=True)
        else:
            adjustment = -profit_size
            profit_price = self._calculate_new_price(price=price, adjustment=adjustment, percentage=False)

        # Build the order
        take_profit_order = {
            "orderType": "LIMIT",
            "session": "NORMAL",
            "price": profit_price,
            "duration": "DAY",
            "orderStrategyType": "SINGLE",
            "orderLegCollection": [
                {
                    "instruction": self.order_instructions[self.enter_or_exit_opposite][self.side],
                    "quantity": self.order_size,
                    "instrument": {
                        "symbol": self.symbol,
                        "assetType": self.asset_type
                    }
                }
            ]
        }

        # Add the order
        self.take_profit_order = take_profit_order
        self.order['childOrderStrategies'].append(self.take_profit_order)

        return True

    def _convert_to_trigger(self):

        if self.order and self._triggered_added == False:
            self.order['orderStrategyType'] = 'TRIGGER'
            self.order['childOrderStrategies'] = []
            self._triggered_added = True

