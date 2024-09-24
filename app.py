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
