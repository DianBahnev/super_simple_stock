import unittest

from datetime import datetime, timedelta
from super_simple_stocks import Stock, StockType, Trade, BuySellIndicator


class TestStock(unittest.TestCase):
    symbol_1 = "AMZN"
    symbol_2 = "JPM"
    par_value_1 = 25
    par_value_2 = 50
    last_dividend_0 = 0.0
    last_dividend_1 = 1.0
    last_dividend_2 = 2.0
    fixed_dividend_0 = None
    fixed_dividend_1 = 0.02
    quantity_1 = 100
    quantity_2 = 300
    price_per_share_1 = 150
    price_per_share_2 = 200
    timestamp_now = datetime.now()

    def test_common_stock_with_fixed_dividend(self):
        with self.assertRaises(ValueError):
            stock = Stock(self.symbol_1, StockType.COMMON, self.par_value_1, self.last_dividend_1, self.fixed_dividend_1)

    def test_dividend(self):
        stock_common = Stock(self.symbol_1, StockType.COMMON, self.par_value_1, self.last_dividend_1, self.fixed_dividend_0)
        stock_preferred = Stock(self.symbol_2, StockType.PREFERRED, self.par_value_2, self.last_dividend_2, self.fixed_dividend_1)

        self.assertEqual(stock_common.dividend, self.last_dividend_1)
        self.assertEqual(stock_preferred.dividend, self.fixed_dividend_1 * self.par_value_2)

    def test_record_trade_wrong_type(self):
        stock = Stock(self.symbol_1, StockType.COMMON, self.par_value_1, self.last_dividend_1, self.fixed_dividend_0)
        false_trade = "a new trade"

        with self.assertRaises(TypeError):
            stock.record_trade(false_trade)

    def test_record_trade_wrong_symbol_and_stock_type(self):
        stock = Stock(self.symbol_1, StockType.COMMON, self.par_value_1, self.last_dividend_1, self.fixed_dividend_0)

        trade_1 = Trade(self.symbol_2, StockType.COMMON, datetime.now(),
                        self.quantity_1, self.price_per_share_1, BuySellIndicator.SELL)
        trade_2 = Trade(self.symbol_1, StockType.PREFERRED, datetime.now(),
                        self.quantity_1, self.price_per_share_1, BuySellIndicator.SELL)
        trade_3 = Trade(self.symbol_2, StockType.PREFERRED, datetime.now(),
                        self.quantity_1, self.price_per_share_1, BuySellIndicator.SELL)

        with self.assertRaises(ValueError):
            stock.record_trade(trade_1)

        with self.assertRaises(ValueError):
            stock.record_trade(trade_2)

        with self.assertRaises(ValueError):
            stock.record_trade(trade_3)

    def test_record_trade_sorting(self):
        stock = Stock(self.symbol_1, StockType.COMMON, self.par_value_1, self.last_dividend_1, self.fixed_dividend_0)

        trade_1 = Trade(self.symbol_1, StockType.COMMON, self.timestamp_now,
                        self.quantity_1, self.price_per_share_1, BuySellIndicator.SELL)
        trade_2 = Trade(self.symbol_1, StockType.COMMON, self.timestamp_now - timedelta(minutes=10),
                        self.quantity_1, self.price_per_share_1, BuySellIndicator.SELL)
        trade_3 = Trade(self.symbol_1, StockType.COMMON, self.timestamp_now - timedelta(minutes=20),
                        self.quantity_1, self.price_per_share_1, BuySellIndicator.SELL)

        stock.record_trade(trade_1)
        stock.record_trade(trade_2)
        stock.record_trade(trade_3)

        self.assertTrue(stock.trades[-1].timestamp, self.timestamp_now)

    def test_ticker_price_no_trades(self):
        stock = Stock(self.symbol_1, StockType.COMMON, self.par_value_1, self.last_dividend_1, self.fixed_dividend_0)

        with self.assertRaises(AttributeError):
            stock.ticker_price

    def test_ticker_price(self):
        stock = Stock(self.symbol_1, StockType.COMMON, self.par_value_1, self.last_dividend_1, self.fixed_dividend_0)
        trade = Trade(self.symbol_1, StockType.COMMON, self.timestamp_now,
                      self.quantity_1, self.price_per_share_1, BuySellIndicator.SELL)

        stock.record_trade(trade)

        self.assertEqual(stock.ticker_price, self.price_per_share_1)

    def test_price_earning_ratio_dividend_zero(self):
        stock = Stock(self.symbol_1, StockType.COMMON, self.par_value_1, self.last_dividend_0, self.fixed_dividend_0)
        trade = Trade(self.symbol_1, StockType.COMMON, self.timestamp_now,
                      self.quantity_1, self.price_per_share_1, BuySellIndicator.SELL)

        stock.record_trade(trade)

        self.assertEqual(stock.price_earnings_ratio, None)

    def test_price_earning_ratio(self):
        stock = Stock(self.symbol_1, StockType.COMMON, self.par_value_1, self.last_dividend_2, self.fixed_dividend_0)
        trade = Trade(self.symbol_1, StockType.COMMON, self.timestamp_now,
                      self.quantity_1, self.price_per_share_1, BuySellIndicator.SELL)

        stock.record_trade(trade)

        self.assertEqual(stock.price_earnings_ratio, 75.0)

    def test_price_no_recent_trades(self):
        stock = Stock(self.symbol_1, StockType.COMMON, self.par_value_1, self.last_dividend_1, self.fixed_dividend_0)
        trade = Trade(self.symbol_1, StockType.COMMON, self.timestamp_now - timedelta(minutes=20),
                      self.quantity_1, self.price_per_share_1, BuySellIndicator.SELL)

        stock.record_trade(trade)

        self.assertEqual(stock.price(self.timestamp_now), None)

    def test_price_use_only_recent_trades(self):
        stock = Stock(self.symbol_1, StockType.COMMON, self.par_value_1, self.last_dividend_1, self.fixed_dividend_0)

        trade_1 = Trade(self.symbol_1, StockType.COMMON, self.timestamp_now,
                        self.quantity_1, self.price_per_share_1, BuySellIndicator.SELL)
        trade_2 = Trade(self.symbol_1, StockType.COMMON, self.timestamp_now - timedelta(minutes=10),
                        self.quantity_1, self.price_per_share_2, BuySellIndicator.SELL)
        trade_3 = Trade(self.symbol_1, StockType.COMMON, self.timestamp_now - timedelta(minutes=30),
                        self.quantity_2, self.price_per_share_2, BuySellIndicator.SELL)

        stock.record_trade(trade_1)
        stock.record_trade(trade_2)
        stock.record_trade(trade_3)

        self.assertEqual(stock.price(), 175)
