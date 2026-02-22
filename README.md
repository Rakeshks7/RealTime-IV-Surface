# RealTime-IV-Surface 

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Framework: Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Domain: Quant Finance](https://img.shields.io/badge/Domain-Quant_Finance-success.svg)](#)

A real-time streaming dashboard that ingests live option chain data, computes Implied Volatility (IV) on the fly, and fits a continuous 3D volatility surface using radial basis function interpolation. Built for applications in options market making, derivatives pricing, and volatility arbitrage.

##  The Quantitative Engine

Option market makers track Implied Volatility rather than raw premium prices. This engine performs the necessary transformations in real-time:

1. **Data Ingestion:** Simulates a live data feed of bid/ask/mid prices across strikes and maturities, featuring stochastic underlying spot movements and market microstructure noise.
2. **Numerical Inversion:** Options are priced using the standard Black-Scholes-Merton model. Because the formula cannot be inverted algebraically for volatility, the engine uses Brent's method (a robust hybrid root-finding algorithm) to solve for the implied volatility $\sigma$ that satisfies:
   
   $$f(\sigma) = V_{BS}(S, K, T, r, \sigma) - V_{Market} = 0$$

3. **Surface Fitting:** A discrete smile is smoothed into a continuous 3D surface across strikes ($K$) and time to maturity ($T$) using Thin-Plate Spline interpolation via `scipy.interpolate.Rbf`.

##  Architecture

* core/pricer.py: Vectorized option pricing and latency-optimized Brent-q root-finding inversion.

* core/fitter.py: Mathematical smoothing of the discrete volatility points into a dense 3D grid.

* data/feed.py: Highly realistic synthetic order book generator with dynamic volatility skew and term structure logic.

* app.py: Asynchronous execution loop and dynamic Plotly rendering.

##  Disclaimer

This repository is built for educational and portfolio demonstration purposes. The models and code provided do not constitute financial advice, investment recommendations, or a production-ready live trading system. Trading options involves significant risk.