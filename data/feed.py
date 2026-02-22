import numpy as np
import pandas as pd
import time
from core.pricer import black_scholes_price

class LiveOptionChain:
    def __init__(self, initial_spot=100.0):
        self.spot = initial_spot
        self.strikes = np.arange(80, 125, 5)
        self.dtes = np.array([7, 14, 30, 60, 90]) 
        self.r = 0.05
    
    def _base_volatility_smile(self, K, S, T):
        moneyness = K / S
        vol = 0.20 - 0.15 * (moneyness - 1.0) + 0.10 * (moneyness - 1.0)**2
        vol = vol * (1 + 0.1 * np.exp(-T*5)) 
        return max(0.05, vol) 

    def fetch_live_chain(self):
        self.spot *= np.exp(np.random.normal(0, 0.005)) 
        
        data = []
        for dte in self.dtes:
            T = dte / 365.0
            for K in self.strikes:
                true_iv = self._base_volatility_smile(K, self.spot, T)

                noise_c = np.random.uniform(-0.02, 0.02)
                noise_p = np.random.uniform(-0.02, 0.02)
                
                c_mid = black_scholes_price(self.spot, K, T, self.r, true_iv, 'C') + noise_c
                p_mid = black_scholes_price(self.spot, K, T, self.r, true_iv, 'P') + noise_p

                c_mid, p_mid = max(0.01, c_mid), max(0.01, p_mid)

                data.append({'underlying_price': self.spot, 'strike': K, 'dte': dte, 'type': 'C', 'mid_price': c_mid})
                data.append({'underlying_price': self.spot, 'strike': K, 'dte': dte, 'type': 'P', 'mid_price': p_mid})
                
        df = pd.DataFrame(data)
        return df, self.spot