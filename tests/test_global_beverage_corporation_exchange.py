import unittest

from datetime import datetime
from super_simple_stocks import Stock, StockType, GlobalBeverageCorporationExchange, BuySellIndicator, Trade


class TestGlobalBeverageCorporationExchange(unittest.TestCase):
    symbol_1 = "AMZN"
    symbol_2 = "JPM"
    par_value_1 = 25
    last_dividend_0 = 0.0
    last_dividend_1 = 1.0
    fixed_dividend_0 = None
    fixed_dividend_1 = 0.02
    quantity_1 = 100
    quantity_2 = 300
    price_per_share_1 = 150
    price_per_share_2 = 200
    timestamp_now = datetime.now()

    def test_add_stock(self):
        exchange = GlobalBeverageCorporationExchange(dict())

        stock_1 = Stock(self.symbol_1, StockType.COMMON, self.par_value_1, self.last_dividend_1, self.fixed_dividend_0)
        stock_2 = Stock(self.symbol_1, StockType.PREFERRED, self.par_value_1, self.last_dividend_0, self.fixed_dividend_1)

        exchange.add_stock(stock_1)
        exchange.add_stock(stock_2)

        stocks = exchange.get_all_stocks()

        self.assertEqual(len(stocks), 2)

        self.assertEqual(stocks[stock_1.symbol_and_type()].symbol, stock_1.symbol)
        self.assertEqual(stocks[stock_1.symbol_and_type()].stock_type, stock_1.stock_type)

        self.assertEqual(stocks[stock_2.symbol_and_type()].symbol, stock_2.symbol)
        self.assertEqual(stocks[stock_2.symbol_and_type()].stock_type, stock_2.stock_type)

    def test_record_trade(self):
        exchange = GlobalBeverageCorporationExchange(dict())
        stock_1 = Stock(self.symbol_1, StockType.COMMON, self.par_value_1, self.last_dividend_1, self.fixed_dividend_0)
        stock_2 = Stock(self.symbol_1, StockType.PREFERRED, self.par_value_1, self.last_dividend_0, self.fixed_dividend_1)

        exchange.add_stock(stock_1)
        exchange.add_stock(stock_2)

        trade_1 = Trade(self.symbol_1, StockType.COMMON, self.timestamp_now,
                        self.quantity_1, self.price_per_share_1, BuySellIndicator.SELL)
        trade_2 = Trade(self.symbol_1, StockType.PREFERRED, self.timestamp_now,
                        self.quantity_2, self.price_per_share_2, BuySellIndicator.SELL)

        exchange.record_trade(trade_1)
        exchange.record_trade(trade_2)

        stocks = exchange.get_all_stocks()

        self.assertEqual(len(stocks[stock_1.symbol_and_type()].trades), 1)
        self.assertEqual(len(stocks[stock_2.symbol_and_type()].trades), 1)

    def test_all_share_index(self):
        exchange = GlobalBeverageCorporationExchange(dict())
        stock_1 = Stock(self.symbol_1, StockType.COMMON, self.par_value_1, self.last_dividend_1, self.fixed_dividend_0)
        stock_2 = Stock(self.symbol_1, StockType.PREFERRED, self.par_value_1, self.last_dividend_0, self.fixed_dividend_1)
        stock_3 = Stock(self.symbol_2, StockType.PREFERRED, self.par_value_1, self.last_dividend_0, self.fixed_dividend_1)

        exchange.add_stock(stock_1)
        exchange.add_stock(stock_2)
        exchange.add_stock(stock_3)

        trade_1 = Trade(self.symbol_1, StockType.COMMON, self.timestamp_now,
                        self.quantity_1, 90, BuySellIndicator.SELL)
        trade_2 = Trade(self.symbol_1, StockType.PREFERRED, self.timestamp_now,
                        self.quantity_2, 100, BuySellIndicator.SELL)
        trade_3 = Trade(self.symbol_2, StockType.PREFERRED, self.timestamp_now,
                        self.quantity_2, 30, BuySellIndicator.SELL)

        exchange.record_trade(trade_1)
        exchange.record_trade(trade_2)
        exchange.record_trade(trade_3)

        self.assertEqual(int(exchange.all_share_index()), 64)



