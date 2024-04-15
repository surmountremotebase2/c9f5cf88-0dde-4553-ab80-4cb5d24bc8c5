from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the asset(s) that the strategy will target
        self.tickers = ["SPY"]

    @property
    def interval(self):
        # Define the data interval to use for the strategy
        return "1day"

    @property
    def assets(self):
        # Return the list of asset tickers
        return self.tickers

    @property
    def data(self):
        # No additional data sources are needed for this strategy
        return []

    def run(self, data):
        # Implement the trading logic
        spy_data = data["ohlcv"]
        
        # Check if there are enough data points to calculate the SMAs
        if len(spy_data) >= 200:
            # Calculate the 50-day and 200-day SMAs for SPY
            sma50 = SMA("SPY", spy_data, 50)[-1]
            sma200 = SMA("SPY", spy_data, 200)[-1]
            
            # If the 50-day SMA is above the 200-day SMA, allocate 100% to SPY, otherwise stay in cash
            if sma50 > sma200:
                allocation_dict = {"SPY": 1.0}
            else:
                allocation_dict = {"SPY": 0}
        else:
            # Not enough data to make a decision, stay in cash
            allocation_dict = {"SPY": 0}
        
        # Return the target allocation
        return TargetAllocation(allocation_dict)