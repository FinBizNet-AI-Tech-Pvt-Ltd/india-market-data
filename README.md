# India market data (FinBizNet)

> **No longer updated (24 Nov 2026).** The weekly refresh has stopped and the files below are frozen at their last version. The pages on finbiznet.com/data remain readable but no longer offer downloads.


Free, citable CSV datasets on Indian markets and the economy: FII/FPI flows, FII and DII daily cash-market activity, order books (defence and capital goods / infrastructure), official macro indicators, and sector index performance by year.

The files are the public tables published on [finbiznet.com/data](https://finbiznet.com/data). A scheduled job refreshes them every Monday, so this repository's commit history is a dated record of every version.

**Licence:** [CC BY 4.0](LICENSE). Free to use, including in research, journalism and teaching, with credit to FinBizNet and a link to the page listed for each file.

## Datasets

| File | What it is | Source of the figures | Page |
|---|---|---|---|
| [`fii-flows-by-month.csv`](data/fii-flows-by-month.csv) | Monthly net FPI investment in Indian equities, Feb 2021 to date, ₹ crore | NSDL FPI daily trends, summed by reporting month | [FII flows by month](https://finbiznet.com/data/fii-flows-by-month) |
| [`fii-dii-daily.csv`](data/fii-dii-daily.csv) | FII and DII buy, sell and net in the cash market, by session, ₹ crore | NSE's daily FII/DII provisional figures | [FII & DII activity](https://finbiznet.com/data/fii-dii-activity) |
| [`defence-order-books.csv`](data/defence-order-books.csv) | Order book and order inflow for listed Indian defence companies, ₹ crore | Order books from earnings-call disclosures; inflow from BSE Reg-30 "Receipt of Order" filings | [Defence order books](https://finbiznet.com/data/defence-order-books) |
| [`order-books.csv`](data/order-books.csv) | Latest order book of listed Indian capital goods, EPC, power, rail and infrastructure companies, with the previous disclosure, ₹ crore | Management disclosures on earnings calls and in investor presentations | [Order books](https://finbiznet.com/data/order-books) |
| [`india-economic-indicators.csv`](data/india-economic-indicators.csv) | CPI, WPI, IIP, RBI policy and market rates, forex reserves and more, each with its period and previous value | MOSPI, DPIIT, RBI | [India economic indicators](https://finbiznet.com/data/india-economic-indicators) |
| [`india-market-2026-indices.csv`](data/india-market-2026-indices.csv) | Nifty 50 and sector indices: 2026 change to date, P/E, closing high and low | NSE daily index close file | [India market 2026](https://finbiznet.com/data/india-market-2026) |
| [`india-market-2025-indices.csv`](data/india-market-2025-indices.csv) | The same for calendar 2025 | NSE daily index close file | [India market 2025](https://finbiznet.com/data/india-market-2025) |

### Columns

**fii-flows-by-month.csv**
- `month`: `YYYY-MM`, the NSDL reporting month.
- `net_equity_cr`: net FPI investment in equity, ₹ crore. Negative means net selling.
- `stock_exchange_cr`: the part routed through the stock exchanges.
- `primary_and_others_cr`: the part through the primary market and other routes (IPOs, QIPs and similar).
- `reporting_days`: NSDL reporting days in the month.
- `month_in_progress`: `yes` for the current, incomplete month.

**fii-dii-daily.csv**
- `date`, then `fii_buy_cr`, `fii_sell_cr`, `fii_net_cr`, `dii_buy_cr`, `dii_sell_cr`, `dii_net_cr`, all ₹ crore.
- The site publishes the latest 30 sessions. This repository merges each week's file into the one before it, so it keeps every session it has collected since it started.

**defence-order-books.csv**
- `company`.
- `order_book_cr`: the latest order book the company disclosed, ₹ crore.
- `order_book_as_of`: the quarter of that disclosure.
- `fy_inflow_disclosed_cr`: order inflow this financial year from Reg-30 filings that stated a value.
- `ttm_order_wins`: the count of order-win filings in the trailing 12 months.

**order-books.csv**
- `company`.
- `order_book_cr`: the latest order book the company disclosed, ₹ crore.
- `order_book_as_of`: the date of that disclosure; `period`: its quarter.
- `previous_order_book_cr`, `previous_period`: the disclosure before it.
- Each figure is the company's own definition (some include L1 orders) and is not adjusted to one standard. Defence companies are in `defence-order-books.csv`.

**india-economic-indicators.csv**
- `section`, `indicator`, `value`, `unit`, `period`, `previous_value`, `source`.
- Each row carries its own `period`. Policy rates and reserve ratios have no publication date of their own, because they hold until the RBI changes them.

**india-market-YYYY-indices.csv**
- `index`, `base_date`, `base_close`, `latest_date`, `latest_close`, `change_pct`, `pe_base`, `pe_latest`, `year_high_close`, `year_high_date`, `year_low_close`, `year_low_date`.
- Highs and lows are closing levels, not intraday extremes. P/E is as NSE publishes it.

## Notes on method

- **NSDL and NSE measure FII activity differently.** NSDL's figures cover FPIs only, and a reporting date carries the previous session's trades. NSE's daily FII/DII numbers are provisional exchange figures. Compare each with itself, not with the other.
- **CPI and WPI were rebased** (CPI to 2024, WPI to 2022-23). A year-on-year rate is never computed across a base change.
- The method notes on each linked page give more detail.

These are descriptive figures from public filings and official statistics. Nothing here is investment advice or a recommendation to buy or sell any security.

## How to cite

> FinBizNet (2026). *India market data*. https://finbiznet.com/data. Retrieved from https://github.com/FinBizNet-AI-Tech-Pvt-Ltd/india-market-data

GitHub's **"Cite this repository"** button (from [`CITATION.cff`](CITATION.cff)) gives APA and BibTeX. Please credit the original publishers too (NSDL, NSE, MOSPI, DPIIT, RBI, BSE). Their own terms apply to their underlying data.

## Updating

`scripts/update.py` uses the standard library only. It downloads each CSV from finbiznet.com and checks it is a real, non-empty CSV. A file is written only when it has changed, so a failed download never replaces good data. To run it by hand:

```bash
python scripts/update.py
```

Found an error? Open an issue, or write via [finbiznet.com](https://finbiznet.com).
