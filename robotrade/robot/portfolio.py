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

    def add_position(self, symbol: str, asset_type: str, purchase_date: Optional[str], quantity: int = 0, purchase_price: float = 0.0) -> dict:

        self.positions[symbol] = {}
        self.positions[symbol]['symbol'] = symbol
        self.positions[symbol]['quantity'] = quantity
        self.positions[symbol]['purchase_price'] = purchase_price
        self.positions[symbol]['purchase_date'] = purchase_date
        self.positions[symbol]['asset_type'] = asset_type

        return self.positions
