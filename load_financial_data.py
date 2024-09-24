"""This file contains functions that load data from API's"""

import pandas as pd


def read_sp500_table():
    """Extracts list of tickers and names of S&P 500 stocks"""
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

    table = pd.read_html(url)
    sp500_df = table[0]

    sp500_list = sp500_df.apply(
        lambda row: {'name': row['Security'], 'ticker': row['Symbol']}, axis=1).tolist()

    return sp500_list


if __name__ == "__main__":
    table = read_sp500_table()
    print(table)
