import copy
import enum
import operator

from datetime import datetime, timedelta
from functools import reduce


@enum.unique
class BuySellIndicator(enum.Enum):
    """Indicator to buy or sell that accompanies each trade"""
    BUY = 1
    SELL = 2


@enum.unique
class StockType(enum.Enum):
    """Indicator for the type of stock"""
    COMMON = 1
    PREFERRED = 2


class Trade:
    """A change of ownership of a collection of shares at a definite price per share"""
    def __init__(self,
                 symbol: str,
                 stock_type: StockType,
                 timestamp: datetime,
                 quantity: int,
                 price_per_share: float,
                 buy_sell_indicator: BuySellIndicator):
        """
        :param symbol: The short name of the stock used in the exchange
        :param stock_type: Indicator for the type of stock
        :param timestamp: The moment when the transaction has taken place
        :param quantity: The amount of shares exchanged
        :param price_per_share: Price for each share
        :param buy_sell_indicator: Indication to buy or sell
        """
        self.symbol = symbol
        self.timestamp = timestamp

        if quantity > 0:
            self.quantity = quantity
        else:
            msg = "The quantity of shares has to be positive."
            raise ValueError(msg)

        if price_per_share >= 0.0:
            self.price_per_share = price_per_share
        else:
            msg = "The price per share can not be negative."
            raise ValueError(msg)

        if type(stock_type) is StockType:
            self.stock_type = stock_type
        else:
            msg = "The type of stock is wrong."
            raise ValueError(msg)

        self.buy_sell_indicator = buy_sell_indicator

    @property
    def total_price(self) -> float:
        """
        :return: The total price of the trade
        """
        return self.quantity * self.price_per_share

    def symbol_and_type(self):
        return self.symbol + "_" + str(self.stock_type.name)


class Stock:
    """
    .. note:: The class variable Stock.price_time_interval serves as a configuration value to
        define the length of the time interval that is significant to calculate the stock
        price.
    """
    price_time_interval = timedelta(minutes=15)

    def __init__(self,
                 symbol: str,
                 stock_type: StockType,
                 par_value: float,
                 last_dividend: float,
                 fixed_dividend: float):
        """
        :param symbol: The short name of the stock used in the exchange
        :param stock_type: Indicator for the type of stock
        :param par_value: The face value per share for this stock
        :param last_dividend: The last dividend paid on the stock
        :param fixed_dividend: In percentage (0.1 == 10%) the on the stock
        .. note:: This initializer also creates the instance variable self.trades,
                  which is to hold a list of recorded instances of Trade.
        .. note :: There is no initial ticker price to be added, as there should be history fo trades on the stock,
                   from it private trades or from the initial public offering.
        """
        self.symbol = symbol
        self.stock_type = stock_type
        self.par_value = par_value
        self._last_dividend = last_dividend
        if self.stock_type is StockType.COMMON and fixed_dividend is not None:
            msg = "Common stock dose not have fixed dividend. It must be None"
            raise ValueError(msg)
        else:
            self._fixed_dividend = fixed_dividend

        self.trades = []

    def symbol_and_type(self):
        return self.symbol + "_" + str(self.stock_type.name)

    @property
    def dividend(self) -> float:
        """
        :return: A ratio that represents the dividend for this stock
        """
        if self.stock_type is StockType.COMMON:
            return float(self._last_dividend)
        else:
            return self._fixed_dividend * self.par_value

    @property
    def dividend_yield(self) -> float:
        return self.dividend / self.ticker_price

    def record_trade(self, trade: Trade):
        """Records a trade for this stock.
        :param trade: The trade to be recorded
        :raise TypeError:
        :raise ValueError:
        """
        if type(trade) is not Trade:
            msg = "Argument trade={trade} must be of type Trade.".format(trade=trade)
            raise TypeError(msg)
        elif self.symbol is not trade.symbol or self.stock_type is not trade.stock_type:
            msg = "Argument trade={trade} does not belong to this stock.".format(trade=trade)
            raise ValueError(msg)
        else:
            my_insort_left(self.trades, trade, keyfunc=lambda v: v.timestamp)

    @property
    def ticker_price(self) -> float:
        """
        :return: The price per share for the last recorded trade for this stock
        :raise AttributeError:
        .. note:: We don't know if the trades will be registered in chronological order.
            That is why self.trades is explicitly sorted.
        """
        if len(self.trades) > 0:
            return float(self.trades[-1].price_per_share)
        else:
            msg = "The last ticker price is not yet available."
            raise AttributeError(msg)

    @property
    def price_earnings_ratio(self) -> float:
        """
        :return: The P/E ratio for this stock
        """
        if self.dividend != 0:
            return self.ticker_price / self.dividend
        else:
            return None

    def price(self, current_time: datetime=datetime.now()) -> float:
        """
        :param current_time: The point of time defined as the current one.
        :return: The average price per share based on trades recorded in the last
            Stock.price_time_interval. None if there are 0 trades that satisfy this
            condition.
        .. note:: The existence of the current_time parameter avoids the inner user
            of datetime.now, thus keeping referential transparency and moving state out.
        """
        separation_index = my_bisect_left(self.trades, current_time - self.price_time_interval,
                                          keyfunc=datetime_extract)
        recent_trades = self.trades[separation_index:]

        if len(recent_trades) > 0:
            summed_price = sum([trade.total_price for trade in recent_trades])
            quantities = sum([trade.quantity for trade in recent_trades])
            return summed_price / float(quantities)
        else:
            return None


class GlobalBeverageCorporationExchange:
    """The whole exchange where the trades take place"""
    def __init__(self, stocks: {Stock, Stock}):
        """
        :param stocks: The stocks traded at this exchange.
        :raise ValueError:
        """
        self.__stocks = stocks

    def add_stock(self, stock):
        if stock not in self.__stocks:
            self.__stocks[stock.symbol_and_type()] = stock

    def stock_in_exchange(self, symbol_and_type: str):
        return symbol_and_type in self.__stocks

    def get_stock(self, symbol_and_type: str):
        return copy.deepcopy(self.__stocks[symbol_and_type])

    def get_all_stocks(self):
        return copy.deepcopy(self.__stocks)

    def record_trade(self, trade: Trade):
        """Records a trade for the proper stock.
        :param trade: The trade to record.
        """
        symbol_and_type = trade.symbol_and_type()
        if not self.stock_in_exchange(symbol_and_type):
            msg = "There is no stock in the exchange symbol: %s, type: %s" % trade.symbol % str(trade.stock_type)
            raise ValueError(msg)
        else:
            self.__stocks[symbol_and_type].record_trade(trade)

    def all_share_index(self, current_time: datetime=datetime.now()) -> float:
        """
        :param current_time: The point of time for which we want to obtain the index.
        :return: The geometric mean of all stock prices. Returns None if any of them is
            None.
        """
        n = len(self.__stocks)
        stock_prices = [stock.price(current_time) for stock in self.__stocks.values()]

        if None in stock_prices:
            return None
        else:
            product = reduce(operator.mul, stock_prices, 1)
            return product**(1/n)


def my_insort_left(a, x, lo=0, hi=None, keyfunc=lambda v: v):
    """
    A slight modification to bisect.insort_left(), so it can get keys.
    https://stackoverflow.com/questions/27672494/how-to-use-bisect-insort-left-with-a-key
    """
    x_key = keyfunc(x)

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if keyfunc(a[mid]) < x_key: lo = mid+1
        else: hi = mid
    a.insert(lo, x)


def my_bisect_left(a, x, lo=0, hi=None, keyfunc=lambda v: v):
    """
    A slight modification to bisect.bisect_left(), so it can get keys.
     https://stackoverflow.com/questions/27672494/how-to-use-bisect-insort-left-with-a-key
    """

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if keyfunc(a[mid]) < keyfunc(x): lo = mid+1
        else: hi = mid
    return lo


def datetime_extract(value):
    if type(value) is Trade:
        return value.timestamp
    elif type(value) is datetime:
        return value
