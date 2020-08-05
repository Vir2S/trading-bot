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
