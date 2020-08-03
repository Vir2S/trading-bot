from typing import List
from typing import Dict
from typing import Union
from typing import Optional


class Portfolio():

    def __init__(self, account_number: Optional[str]):

        self.positions = {}
        self.positions_count = 0
        self.market_value = 0.0
        self.profit_loss = 0.0
        self.risk_tolerance = 0.0
        self.account_number = account_number

