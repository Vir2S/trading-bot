import pandas as pd

from td.client import TDClient
from td.utils import milliseconds_since_epoch

from datetime import datetime
from datetime import time
from datetime import timezone

from typing import List
from typing import Dict
from typing import Union


class Robot():
    def __init__(
            self,
            client_id: str,
            redirect_uri: str,
            credentials_path: str = None,
            trading_account: str = None
    ) -> None:

        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.credentials_path = credentials_path
        self.trading_account = trading_account