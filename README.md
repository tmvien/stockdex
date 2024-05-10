[![Publish Python Package to PyPI](https://github.com/ahnazary/stockdex/actions/workflows/publish-package.yaml/badge.svg)](https://github.com/ahnazary/stockdex/actions/workflows/publish-package.yaml)
[![PyPI version](https://badge.fury.io/py/stockdex.svg)](https://badge.fury.io/py/stockdex)

![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
![Code style: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)
![flake8](https://img.shields.io/badge/flake8-checked-blue)

[![Documentation Status](https://readthedocs.org/projects/stockdex/badge/?version=latest)](https://ahnazary.github.io/stockdex/)

# Stockdex

Stockdex is a Python package that provides a simple interface to access financial data from Yahoo Finance. Data is returned as a pandas DataFrame.

# Installation 

Install the package using pip:

```bash
pip install stockdex -U
``` 

# Usage

To access main functions, use `ticker`property from `TickerFactory` class. The `Ticker` class is used to access data from Various data sources. The `TickerFactory` class requires a data source to be passed to it. Here is an example of how to begin using the package:
```python
from stockdex import TickerFactory

ticker = TickerFactory(ticker="AAPL", data_source="yahoo_api").ticker
```

After creating the `Ticker` object, you can access functions defined for each data source. Below are some examples of how to access data from supported data sources.

## Data from `Yahoo Finance` API (fast queries through Yahoo Finance API):
```python
from stockdex import TickerFactory

ticker = TickerFactory(ticker="AAPL", data_source="yahoo_api").ticker

# Price data (use range and dataGranularity to make range and granularity more specific)
price = ticker.price(range='1y', dataGranularity='1d')

# Current trading period of the stock (pre-market, regular, post-market trading periods)
current_trading_period = ticker.current_trading_period

# Fundamental data (use frequency, format, period1 and period2 to fine-tune the returned data)
income_statement = ticker.income_statement(frequency='quarterly')
cash_flow = ticker.cash_flow(format='raw')
balance_sheet = ticker.balance_sheet(period1=datetime(2020, 1, 1))
financials = ticker.financials(period1=datetime(2022, 1, 1), period2=datetime.today())
```


## Data from `Yahoo Finance` website (web scraping):
```python
from stockdex import TickerFactory

ticker = TickerFactory(ticker="AAPL", data_source="yahoo_web").ticker

# Summary including general financial information
summary = ticker.summary

# Financial data as it is seen in the yahoo finance website
income_stmt_web = ticker.income_stmt_web
balance_sheet = ticker.balance_sheet_web
cash_flow = ticker.cashflow_web

# Analysts and estimates
analysis = ticker.analysis

# Data about options
calls = ticker.calls
puts = ticker.puts

# Profile data 
key_executives = ticker.key_executives
description = ticker.description
corporate_governance = ticker.corporate_governance

# Data about shareholders
major_holders = ticker.major_holders
top_institutional_holders = ticker.top_institutional_holders
top_mutual_fund_holders = ticker.top_mutual_fund_holders

# Statistics
valuation_measures = ticker.valuation_measures
financial_highlights = ticker.financial_highlights
trading_information = ticker.trading_information
```

<!-- ## NASDAQ data from `NASDAQ` website (web scraping):

Data on NASDAQ website gets updated more frequently than Yahoo Finance data. Below are some of the data that can be retrieved from the NASDAQ website.

```python
# Data about quarterly and yearly earnings, updated on the same day as the earnings release (yahoo finance data is updated after a few days)

quarterly_earnings_surprise = ticker.quarterly_earnings_surprise
yearly_earnings_forecast = ticker.yearly_earnings_forecast
quarterly_earnings_forecast = ticker.quarterly_earnings_forecast

price_to_earnings_ratio = ticker.price_to_earnings_ratio
forecast_price_to_earnings__growth_rates = ticker.forecast_peg_rate
``` -->

## Stocks data from `Digrin` (web scraping):

Data on Digrin website includes all historical data of the stock in certain categories, unlike Yahoo Finance which only provides the last 5 years of data at most.

```python
from stockdex import TickerFactory

ticker = TickerFactory(ticker="AAPL", data_source="digrin").ticker

# Complete historical data of the stock in certain categories
dividend = ticker.dividend
payout_ratio = ticker.payout_ratio
stock_splits = ticker.stock_splits
```

## EU ETF data from `justETF` (web scraping):

For EU ETFS, the `isin` and `security_type` should be passed to the `Ticker` object. The `isin` is the International Securities Identification Number of the ETF and the `security_type` should be set to `etf`.

```python
from stockdex import TickerFactory

etf = TickerFactory(isin="IE00B4L5Y983", security_type="etf", data_source="justetf").ticker

etf_general_info = etf.etf_general_info
etf_wkn = etf.etf_wkn
etf_description = etf.etf_description

# Basic data about the ETF
etf_basics = etf.etf_basics

# Holdings of the ETF by company, country and sector
etf_holdings_companies = etf.etf_holdings_companies
etf_holdings_countries = etf.etf_holdings_countries
etf_holdings_sectors = etf.etf_holdings_sectors
```

<br />

---

Check out sphinx documentation [here](https://ahnazary.github.io/stockdex/) for more information about the package.