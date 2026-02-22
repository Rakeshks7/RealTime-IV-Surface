import numpy as np
from scipy.interpolate import Rbf
import pandas as pd

def fit_volatility_surface(df):
    df_calls = df[(df['type'] == 'C') & (df['strike'] >= df['underlying_price'])]
    df_puts = df[(df['type'] == 'P') & (df['strike'] < df['underlying_price'])]
    df_otm = pd.concat([df_puts, df_calls])
    
    if len(df_otm) < 10:
         return None, None, None 

    x = df_otm['strike'].values
    y = df_otm['dte'].values
    z = df_otm['iv'].values

    try:
        rbf = Rbf(x, y, z, function='thin_plate', smooth=0.1)
    except np.linalg.LinAlgError:
         return None, None, None

    strike_grid = np.linspace(x.min(), x.max(), 50)
    dte_grid = np.linspace(y.min(), y.max(), 50)
    X, Y = np.meshgrid(strike_grid, dte_grid)
    Z = rbf(X, Y)

    return X, Y, Z