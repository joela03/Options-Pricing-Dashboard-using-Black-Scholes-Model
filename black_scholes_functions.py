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
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2
