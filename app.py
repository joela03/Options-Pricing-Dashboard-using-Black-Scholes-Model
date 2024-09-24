"""This file create's an interactive Web Application using Dash"""

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import yfinance as yf
from dotenv import load_dotenv
import os

from load_financial_data import (read_sp500_table, fetch_current_stock_price,
                                 fetch_risk_free_rate)
from black_scholes_functions import (calculate_d1_d2, black_scholes_call,
                                     black_scholes_put, delta, gamma, theta, vega, rho)

# Fetch list of stocks
sp500_list = read_sp500_table()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Black-Scholes Option Pricing & Greeks Calculator"),
            html.Label("Select Stock"),
            dcc.Dropdown(
                id='stock-dropdown',
                options=[{'label': stock['name'], 'value': stock['ticker']}
                         for stock in sp500_list],
                value='AAPL'),
            html.Label("Strike Price"),
            dcc.Input(id='strike-price', type='number', value=100, step=0.01),
            html.Label("Time to Maturity (Years)"),
            dcc.Input(id='time-to-maturity',
                      type='number', value=1, step=0.01),
            html.Label("Volatility (σ)"),
            dcc.Input(id='volatility', type='number', value=0.2, step=0.01),
            html.Label("Risk-Free Rate (r)"),
            dcc.Input(id='risk-free-rate', type='number',
                      value=0.05, step=0.01),
            html.Br()
        ], width=4)
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True)
