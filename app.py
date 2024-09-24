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
from black_scholes_functions import (black_scholes_call,
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
            html.Br(),
            html.Button('Calculate', id='calculate-button', n_clicks=0)
        ], width=4),
        dbc.Col([
            html.H3("Results"),
            html.Div(id='results')
        ], width=8)
    ])
])


@app.callback(
    Output('results', 'children'),
    Input('calculate-button', 'n_clicks'),
    Input('stock-dropdown', 'value'),
    Input('strike-price', 'value'),
    Input('time-to-maturity', 'value'),
    Input('volatility', 'value')
)
def calculate_options_and_greeks(n_clicks, ticker, K, T, sigma,):
    if n_clicks == 0:
        return ""

    S = fetch_current_stock_price(ticker)
    api_key = os.environ['ALPHA_VANTAGE_API_KEY']
    r = fetch_risk_free_rate(api_key)

    call_price = black_scholes_call(S, K, T, r, sigma)
    put_price = black_scholes_put(S, K, T, r, sigma)
    delta_call = delta(S, K, T, r, sigma, option_type='call')
    gamma_value = gamma(S, K, T, r, sigma)
    theta_call = theta(S, K, T, r, sigma, option_type='call')
    vega_value = vega(S, K, T, r, sigma)
    rho_call = rho(S, K, T, r, sigma, option_type='call')

    return html.Div([
        html.P(f"Stock Price (S): {S:.2f}"),
        html.P(f"Call Option Price: {call_price:.2f}"),
        html.P(f"Put Option Price: {put_price:.2f}"),
        html.P(f"Delta (Call): {delta_call:.2f}"),
        html.P(f"Gamma: {gamma_value:.2f}"),
        html.P(f"Theta (Call): {theta_call:.2f}"),
        html.P(f"Vega: {vega_value:.2f}"),
        html.P(f"Rho (Call): {rho_call:.2f}")
    ])


if __name__ == "__main__":
    app.run_server(debug=True)
