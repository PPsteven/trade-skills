---
name: akshare-skill
description: Reference documentation for AKShare financial data APIs. Use when working with AKShare to access Chinese financial market data including stocks, futures, funds, bonds, forex, macroeconomic indicators, and other asset classes. Contains comprehensive API parameter documentation, output schemas, and code examples for all data categories supported by AKShare.
---

# AKShare Data API Reference

AKShare is a Python package providing access to Chinese financial market data. This skill contains complete API documentation organized by asset class and data category.

## Quick Start

To use AKShare in Python:

```python
import akshare as ak

# Example: Get stock data
stock_df = ak.stock_zh_a_hist(symbol="000001", start_date="20200101", end_date="20210101")
print(stock_df)
```

## Data Categories

Browse API documentation by asset class:

### **Equities & Indices**
- **[Stock Data](stock.md)** - A/B shares, history, daily snapshots, sector data, board listings
- **[Index Data](index.md)** - Stock indices, index components, performance data

### **Fixed Income & Rates**
- **[Bonds](bond.md)** - Government bonds, corporate bonds, municipal bonds
- **[Interest Rates](interest_rate.md)** - LPR rates, deposit/loan rates, yield curves

### **Derivatives & Futures**
- **[Futures](futures.md)** - Futures contracts, open interest, delivery data
- **[Options](option.md)** - Options contracts, Greeks, implied volatility

### **Alternative Assets**
- **[Funds](fund/)** - Public funds (mutual funds), private funds (hedge funds), fund ratings
- **[QDII](qdii.md)** - Qualified Domestic Institutional Investor products
- **[Commodities & Spot Trading](spot.md)** - Commodity futures, spot market data

### **Forex & International**
- **[Foreign Exchange (FX)](fx.md)** - Currency pairs, exchange rates
- **[Hong Kong/Singapore Data (QHKC)](qhkc/)** - Hong Kong stocks, Singapore data, commodity analysis

### **Macro & Economics**
- **[Macroeconomic Data](macro.md)** - GDP, CPI, industrial production, consumer spending
- **[Currency & FX Markets](currency.md)** - Currency data, forex indicators
- **[Energy Data](energy.md)** - Oil, coal, natural gas prices and data
- **[Interest Rates](interest_rate.md)** - Central bank rates, yield curves

### **Specialized Data**
- **[Bank Data](bank.md)** - Bank regulatory data, administrative penalties
- **[Data Center (DC)](dc.md)** - Data center services and infrastructure
- **[Digital Currency](dc.md)** - Cryptocurrency and digital asset data
- **[Events & News](event.md)** - Market events, corporate actions, news events
- **[Natural Language Processing](nlp.md)** - Text analysis, sentiment analysis
- **[Technical Indicators & Tools](tool.md)** - Technical analysis tools, indicators
- **[Financial Articles](article.md)** - Financial research articles and reports
- **[Others](others.md)** - Additional specialized data sources

## API Documentation Structure

Each reference file contains:

- **API name** - The function name (e.g., `stock_zh_a_hist`)
- **Target URL** - Data source web address
- **Description** - What the API provides
- **Rate limits** - Data return limits per request
- **Input parameters** - Function parameters with types and descriptions
- **Output parameters** - DataFrame columns returned by the API
- **Code example** - Working Python example
- **Data sample** - Sample output rows

## Parameter Conventions

Common parameter patterns across AKShare APIs:

- **`symbol`** - Stock symbol (e.g., "000001" for SZZF)
- **`start_date` / `end_date`** - Date strings in format "YYYYMMDD" (e.g., "20200101")
- **`period`** - Time period ("daily", "weekly", "monthly")
- **`page`** / **`limit`** - Pagination parameters for large datasets
- **Date output** - Most APIs return datetime columns in format "YYYY-MM-DD HH:MM:SS"

## Multi-Part Categories

Some data categories have multiple sub-APIs:

- **[Funds (fund/)](fund/)** - Public funds vs. private funds documentation
- **[QHKC (qhkc/)](qhkc/)** - Hong Kong stocks, fundamentals, brokers, commodities, analysis tools

## Finding What You Need

**By asset class:** Start with the category above that matches your market focus

**By function:** If you know the AKShare function name, search within the corresponding reference file using grep patterns:
- Stock functions: `stock_`
- Fund functions: `fund_`
- Futures functions: `futures_` or `future_`
- Forex functions: `fx_` or `exchange_`

**By data type:** All APIs include parameter tables and examples. Look for "Input parameters" and "Output parameters" sections.

## Example Usage Patterns

### Get historical stock data:
See [stock.md](stock.md) - use `stock_zh_a_hist()` function

### Access futures data:
See [futures.md](futures.md) - functions like `futures_open_interest()`, `futures_delivery()`

### Query fund performance:
See [fund/fund_public.md](fund/fund_public.md) for mutual funds or [fund/fund_private.md](fund/fund_private.md) for private funds

### Macroeconomic indicators:
See [macro.md](macro.md) - GDP, inflation, industrial production

### Hong Kong/Singapore market data:
See [qhkc/](qhkc/) subdirectory for index data, fundamentals, and analysis tools
