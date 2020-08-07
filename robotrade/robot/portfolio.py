from typing import List
from typing import Dict
from typing import Union
from typing import Optional
from typing import Tuple

from td.client import TDClient


class Portfolio():

    def __init__(self, account_number: Optional[str]):

        self.positions = {}
        self.positions_count = 0
        self.market_value = 0.0
        self.profit_loss = 0.0
        self.risk_tolerance = 0.0
        self.account_number = account_number
        self._td_client: TDClient = None

    def add_position(
            self,
            symbol: str,
            asset_type: str,
            purchase_date: Optional[str],
            quantity: int = 0,
            purchase_price: float = 0.0
    ) -> Dict:

        self.positions[symbol] = {}
        self.positions[symbol]['symbol'] = symbol
        self.positions[symbol]['quantity'] = quantity
        self.positions[symbol]['purchase_price'] = purchase_price
        self.positions[symbol]['purchase_date'] = purchase_date
        self.positions[symbol]['asset_type'] = asset_type

        return self.positions

    def add_positions(self, positions: List[dict]) -> dict:

        if isinstance(positions, list):

            for position in positions:
                self.add_position(
                    symbol=position['symbol'],
                    asset_type=position['asset_type'],
                    purchase_date=position.get('purchase_date', None),
                    quantity=position.get('quantity', 0),
                    purchase_price=position.get('purchase_price', 0.0),
                )

            return self.positions

        else:
            raise TypeError('Positions must be a list of dictionaries.')

    def remove_position(self, symbol: str) -> Tuple[bool, str]:

        if symbol in self.positions:
            del self.positions[symbol]
            return (True, '{Symbol} was successfully removed.'.format(symbol=symbol))
        else:
            return (False, '{Symbol} did not exists in portfolio.'.format(symbol=symbol))

    def in_portfolio(self, symbol: str) -> bool:

        if symbol in self.positions:
            return True
        else:
            return False

    def is_profitable(self, symbol: str, current_price: float) -> bool:

        # Grab the purchase_price
        purchase_price = self.positions[symbol]['purchase_price']

        if purchase_price <= current_price:
            return True
        elif purchase_price > current_price:
            return False

    @property
    def td_client(self) -> TDClient:
        """
            Gets the TDClient object for the Portfolio

            Returns:
            ----
            {TDClient} -- An authenticated session with the TD API
        """

        return self._td_client

    @td_client.setter
    def td_client(self, td_client: TDClient) -> None:
        """
            Sets the TDClient object for the Portfolio

            Arguments:
            ----
            td_client {TDClient} -- An authenticated session with the TD API
        """

        self._td_client = td_client

    def total_allocation(self):
        pass

    def risk_exposure(self):
        pass

    def total_market_value(self):
        pass

