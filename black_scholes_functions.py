"""Functions that are involved in the implementation of the black-scholes model"""

import numpy as np
from scipy.stats import norm

# The Black-Scholes model is a mathematical model used for pricing
# European-style options. It calculates the theoretical price of an
# option based on the current stock price, the option's strike price,
# time to maturity, volatility of the stock, and the risk-free
# interest rate.

# The Black-Scholes formula for a European call option is :
# C = S0*N(d1)-K*e^(-rT)*N(d2)

# The Black-Scholes formula for a European put option is :
# C = K*e^(-rT)*N(-d2)-S0*N(-d1)

# Where:
# S0 - Current Stock Price
# K = strike price of the option
# T = Time to maturity (in years)
# r = Risk-free interest rate (annual)
# o = Volatility of the stock (annual)
# N = cumulative distribution function of the standard normal distribution
# d1 and d2 are intermediate variables calculated as:
# d1 = (ln(S0/K)+((r+o^2)/2)*T)/(o*sqrt(T))
# d2 = d1-o*sqrt(T)


def calculate_d1_d2(S, K, T, r, sigma):
    """Calculate's the intermediate variables"""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2


def black_scholes_call(S, K, T, r, sigma):
    """Calculate's value of european call option"""
    d1, d2 = calculate_d1_d2(S, K, T, r, sigma)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price


def black_scholes_put(S, K, T, r, sigma):
    """Calculates's value of european put option"""
    d1, d2 = calculate_d1_d2(S, K, T, r, sigma)
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return put_price

# The "Greeks" are a set of financial metrics that describe how the price of
# an option changes in response to various factors. They are essential tools
# in options trading and risk management. Each Greek measures the sensitivity
# of the option's price to a different underlying variable.

# Delta: Sensitivity to price changes of the underlying asset.
# Gamma: Sensitivity of Delta to price changes of the underlying asset.
# Theta: Sensitivity to time decay.
# Vega: Sensitivity to volatility changes.
# Rho: Sensitivity to interest rate changes.


def delta(S, K, T, r, sigma, option_type='call'):
    """Calculate's the greek delta value"""
    d1, _ = calculate_d1_d2(S, K, T, r, sigma)
    if option_type == 'call':
        return norm.cdf(d1)
    elif option_type == 'put':
        return norm.cdf(d1) - 1


def gamma(S, K, T, r, sigma):
    """Calculate's the greek gamma value"""
    d1, _ = calculate_d1_d2(S, K, T, r, sigma)
    return norm.pdf(d1) / (S * sigma * np.sqrt(T))


def theta(S, K, T, r, sigma, option_type='call'):
    d1, d2 = calculate_d1_d2(S, K, T, r, sigma)
    first_term = -S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
    if option_type == 'call':
        second_term = r * K * np.exp(-r * T) * norm.cdf(d2)
        return first_term - second_term
    elif option_type == 'put':
        second_term = r * K * np.exp(-r * T) * norm.cdf(-d2)
        return first_term + second_term


def vega(S, K, T, r, sigma):
    d1, _ = calculate_d1_d2(S, K, T, r, sigma)
    return S * norm.pdf(d1) * np.sqrt(T)


def rho(S, K, T, r, sigma, option_type='call'):
    _, d2 = calculate_d1_d2(S, K, T, r, sigma)
    if option_type == 'call':
        return K * T * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        return -K * T * np.exp(-r * T) * norm.cdf(-d2)
