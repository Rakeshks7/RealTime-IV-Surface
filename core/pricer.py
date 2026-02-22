import numpy as np
from scipy.stats import norm
from scipy.optimize import brentq
import pandas as pd

def black_scholes_price(S, K, T, r, sigma, option_type='C'):
    T = np.maximum(T, 1e-5)
    sigma = np.maximum(sigma, 1e-5)
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'C':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return price

def implied_volatility(price, S, K, T, r, option_type='C'):
    def objective_func(sigma):
        return black_scholes_price(S, K, T, r, sigma, option_type) - price

    if option_type == 'C' and price < max(0, S - K * np.exp(-r*T)):
        return np.nan
    if option_type == 'P' and price < max(0, K * np.exp(-r*T) - S):
        return np.nan

    try:
        iv = brentq(objective_func, 1e-4, 5.0, xtol=1e-5, maxiter=100)
        return iv
    except ValueError:
        return np.nan

def calculate_chain_iv(df, S, r=0.0):
    ivs = []
    for _, row in df.iterrows():
        iv = implied_volatility(
            price=row['mid_price'],
            S=S,
            K=row['strike'],
            T=row['dte'] / 365.0, 
            r=r,
            option_type=row['type']
        )
        ivs.append(iv)
    
    df['iv'] = ivs
    return df.dropna(subset=['iv'])