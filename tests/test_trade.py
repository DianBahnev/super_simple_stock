import unittest

from datetime import datetime
from super_simple_stocks import Trade
from super_simple_stocks import StockType
from super_simple_stocks import BuySellIndicator


class TestTrade(unittest.TestCase):
    symbol = "AMZN"
    quantity_0 = 0
    quantity_1 = 100
    price_per_share_0 = -1
    price_per_share_1 = 150

    def test_total_price(self):
        trade = Trade(self.symbol, StockType.COMMON, datetime.now(),
                      self.quantity_1, self.price_per_share_1, BuySellIndicator.SELL)

        self.assertEquals(trade.total_price, 100*150)

    def test_stock_and_type(self):
        trade = Trade(self.symbol, StockType.COMMON, datetime.now(),
                      self.quantity_1, self.price_per_share_1, BuySellIndicator.SELL)

        self.assertEquals(trade.symbol_and_type(), trade.symbol + "_" + str(trade.stock_type.name))

    def test_wrong_type(self):
        with self.assertRaises(ValueError):
            Trade(self.symbol, "COMMON", datetime.now(),
                  self.quantity_1, self.price_per_share_1, BuySellIndicator.SELL)

    def test_quantity_zero(self):
        with self.assertRaises(ValueError):
            Trade(self.symbol, StockType.COMMON, datetime.now(),
                  self.quantity_0, self.price_per_share_1, BuySellIndicator.SELL)

    def test_price_per_share_below_zero(self):
        with self.assertRaises(ValueError):
            Trade(self.symbol, StockType.COMMON, datetime.now(),
                  self.quantity_1, self.price_per_share_0, BuySellIndicator.SELL)
