import operator
import numpy as np
import pandas as pd

from typing import List, Dict, Union, Optional, Tuple, Any

from stock_frame import StockFrame


class Indicators():

    def __init__(self, price_data_frame: StockFrame) -> None:

        self._stock_frame: StockFrame = price_data_frame
        self._price_groups = price_data_frame.symbol_groups
        self._current_indicators = {}
        self._indicator_signals = {}
        self._frame = self._stock_frame.frame

    def set_indicator_signals(self, indicator: str, buy: float, sell: float, condition_buy: Any, condition_sell: Any) -> None:

        # If there is no signal for that indicator set a template
        if indicator not in self._indicator_signals:
            self._indicator_signals[indicator] = {}

        # Modify the signal
        self._indicator_signals[indicator]['buy'] = buy
        self._indicator_signals[indicator]['sell'] = sell
        self._indicator_signals[indicator]['buy_operator'] = condition_buy
        self._indicator_signals[indicator]['sell_operator'] = condition_sell

