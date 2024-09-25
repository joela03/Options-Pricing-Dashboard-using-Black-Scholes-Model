"""This file create's an interactive Web Application using Dash"""

import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import numpy as np
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

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # Tracks the current page's URL
    html.Div(id='page-content')  # This will hold the layout for each page
])


def page_1(sp500_list):
    return dbc.Container([
        html.H1("Option Pricing & Greeks Calculator"),
        html.Label("Select Stock"),
        dcc.Dropdown(
            id='stock-dropdown',
            options=[{'label': stock['name'], 'value': stock['ticker']}
                     for stock in sp500_list],
            value='AAPL',
        ),
        html.Label("Strike Price"),
        dcc.Input(id='strike-price', type='number', value=100, step=0.01),
        html.Label("Time to Maturity (Years)"),
        dcc.Input(id='time-to-maturity', type='number', value=1, step=0.01),
        html.Label("Volatility (σ)"),
        dcc.Input(id='volatility', type='number', value=0.2, step=0.01),
        html.Label("Risk-Free Rate (r)"),
        dcc.Input(id='risk-free-rate', type='number', value=0.05, step=0.01),
        html.Br(),
        html.Br(),
        dcc.Link(dbc.Button("Submit", color="primary"),
                 href='/results')
    ])


app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Option Pricing & Greeks Calculator",
                    className="text-center"),
            html.P("Select a stock and enter option parameters to calculate option prices and Greeks.",
                   className="text-center")
        ], width=12)
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            html.H5("Option Parameters"),
            dbc.Card([
                dbc.CardBody([
                    html.Label("Select Stock"),
                    dcc.Dropdown(
                        id='stock-dropdown',
                        options=[{'label': stock['name'], 'value': stock['ticker']}
                                 for stock in sp500_list],
                        value='AAPL',  # Default value
                    ),
                    html.Label("Strike Price"),
                    dcc.Input(id='strike-price', type='number',
                              value=100, step=0.01),
                    html.Label("Time to Maturity (Years)"),
                    dcc.Input(id='time-to-maturity',
                              type='number', value=1, step=0.01),
                    html.Label("Volatility (σ)"),
                    dcc.Input(id='volatility', type='number',
                              value=0.2, step=0.01),
                    html.Label("Risk-Free Rate (r)"),
                    dcc.Input(id='risk-free-rate', type='number',
                              value=0.05, step=0.01),
                    html.Br(),
                    html.Br(),
                    dbc.Button("Calculate", id='calculate-button',
                               color="primary", n_clicks=0)
                ])
            ], className="mb-4")
        ], width=4),
        dbc.Col([
            html.H5("Results"),
            dbc.Card([
                dbc.CardBody([
                    html.Div(id='results')
                ])
            ])
        ], width=8)
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            html.H5("Option Call Price Over Time"),
            dcc.Graph(id='call-price-over-time')
        ], width=6),
        dbc.Col([
            html.H5("Option Put Price Over Time"),
            dcc.Graph(id='put-price-over-time')
        ], width=6)
    ])
], fluid=True)


@app.callback(
    [Output('results', 'children'),
     Output('call-price-over-time', 'figure'),
     Output('put-price-over-time', 'figure')],
    [Input('calculate-button', 'n_clicks'),
     Input('stock-dropdown', 'value'),
     Input('strike-price', 'value'),
     Input('time-to-maturity', 'value'),
     Input('volatility', 'value')]
)
def calculate_options_and_greeks(n_clicks, ticker, K, T, sigma,):
    if n_clicks == 0:
        return "", go.Figure()

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

    results = html.Div([
        html.P(f"Stock Price (S): {S:.2f}"),
        html.P(f"Call Option Price: {call_price:.2f}"),
        html.P(f"Put Option Price: {put_price:.2f}"),
        html.P(f"Delta (Call): {delta_call:.2f}"),
        html.P(f"Gamma: {gamma_value:.2f}"),
        html.P(f"Theta (Call): {theta_call:.2f}"),
        html.P(f"Vega: {vega_value:.2f}"),
        html.P(f"Rho (Call): {rho_call:.2f}")
    ])

    # Option Price of time graph
    times = np.linspace(0.01, T, 100)
    call_prices_over_time = [black_scholes_call(
        S, K, t, r, sigma) for t in times]
    put_prices_over_time = [black_scholes_put(
        S, K, t, r, sigma) for t in times]

    call_fig = go.Figure()
    call_fig.add_trace(go.Scatter(x=times, y=call_prices_over_time,
                                  mode='lines', name='Call Price'))
    call_fig.update_layout(title="Call Option Prices Over Time to Maturity",
                           xaxis_title="Time to Maturity (Years)",
                           yaxis_title="Call Option Price",
                           template="plotly_dark")

    put_fig = go.Figure()
    put_fig.add_trace(go.Scatter(x=times, y=put_prices_over_time,
                                 mode='lines', name='Put Price'))
    call_fig.update_layout(title="Put Option Prices Over Time to Maturity",
                           xaxis_title="Time to Maturity (Years)",
                           yaxis_title="Put Option Price",
                           template="plotly_dark")

    return results, call_fig, put_fig


if __name__ == "__main__":
    app.run_server(debug=True)
