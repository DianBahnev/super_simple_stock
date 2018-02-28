# Super Simple Stocks

This code is submitted as an answer to the assignment _Super Simple Stocks_ concerning J.P.Morgan.
The instructions may be found in the document `doc/SuperSimpleDocs.docx`.

## Requirements

The application has been developed using Python 3 (3.4), and uses only standard libraries. 

## Code structure and usage

The application is fully contained in the single top-level module `super_simple_stocks`. It is to be used by packing a set of
instances of `Stock` in a dictionary {symbol_and_type: Stock} and pass it as the only argument to `GlobalBeverageCorporationExchange` initializer, or add stocks one by one. Trades can be added to the stocks before being added to the exchnage or after that. 
The resulting instance is to be used a a representation of the complete GBCE. 

- For a given instance of `Stock`:
  - _Calculate the dividend yield_: `Stock.dividend_yield`
  - _Calculate the P/E Ratio_: `Stock.price_earnings_ratio`
  - _Record a trade, with timestamp, quantity of shares, buy or sell indicator and price_: Create an instance of `Trade` and supply it to an instance of`GlobalBeverageCorporationExchange` that contains the proper stock my means of `record_trade`
  - _Calculate Stock Price based on trades recorded in past 15 minutes_: `Stock.price`
- _Calculate the GBCE All Share Index using the geometric mean of prices for all stocks_: `GlobalBeverageCorporationExchange.all_share_index`.

Type hints are present in all relevant signatures and basic documentation is included in the code itself.


## Tests

A moderately extensive (although my no means exhaustive) suite of tests is included in `tests/`.

---

Thanks to Armand Adroher (https://github.com/aadroher/super_simple_stocks) for his helpful implementation, implementation.

- Main differences in Trade:
  - Adding type of stock, so we can differentiate between trades for the same symbol but different stock type (Common/Preferred)
  - Adding method to extract symbol and stock type, so we can use it as key easly when adding new trade to the stock exchange.
 
- Main differences in Stock: 
  - Using composition instead of inheritance for implementing Preferred stock and Common Stock.
  - The list of trades in each stock is sorted, each new trade is inserted considering it's timestamp.
  Using slightly modified version of bisect.insort_left(). For more efficient price calculation.
  - When calculating the price using slightly modified version of bisect.bisect_left(), to filter out old trades,
  and increase the efficiency of the calculation.
  - Adding method to extract symbol and stock type, so we can use it as key easly when adding new stock to the stock exchange.
I've chose this approach instead of overriding __hash__ and __eq__, as I'm using a dictionary to store stocks in the exchange and a key value is needed, and both Stock and Trade would have to have the same implementation for this approach to work. Having two different classes having the same __hash__ and __eq__ would brake the equality rules/contract.
 
- Main differences in GlobalBeverageCorporationExchange:
  - Using dictionary instead of a list for storing stocks
  - Encapsulating the dictionary containing stocks
  - Adding functionality to record trade
