"""This file contains functions that load data from API's"""

import pandas as pd
import yfinance as yf


def read_sp500_table():
    """Extracts list of tickers and names of S&P 500 stocks"""
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    table = pd.read_html(url)
    sp500_df = table[0]

    sp500_list = sp500_df.apply(
        lambda row: {'name': row['Security'], 'ticker': row['Symbol']}, axis=1).tolist()

    return sp500_list


def fetch_current_stock_price(ticker):
    """Fetches most accurate stock price from yfinance library"""
    stock = yf.Ticker(ticker)

    recent_data = stock.history(period='1d')

    if not recent_data.empty:
        current_price = recent_data['Close'].iloc[-1]
        return current_price
    else:
        raise ValueError(f"No data found for ticker {ticker}")


if __name__ == "__main__":
    price = fetch_current_stock_price('MM')
    print(price)
