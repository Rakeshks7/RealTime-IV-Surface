import streamlit as st
import plotly.graph_objects as go
import time
from data.feed import LiveOptionChain
from core.pricer import calculate_chain_iv
from core.fitter import fit_volatility_surface

st.set_page_config(page_title="Live IV Surface Streamer", layout="wide")

def main():
    st.title("Live Implied Volatility Surface")
    st.markdown("Streaming Option Chain $\\rightarrow$ Root-Finding Inversion $\\rightarrow$ Cubic Spline Interpolation")

    col1, col2, col3 = st.columns(3)
    spot_metric = col1.empty()
    time_metric = col2.empty()
    status_metric = col3.empty()

    chart_placeholder = st.empty()

    feed = LiveOptionChain(initial_spot=4500.0) # E.g., SPX level

    while True:
        try:
            raw_chain, current_spot = feed.fetch_live_chain()

            chain_with_iv = calculate_chain_iv(raw_chain, current_spot, r=0.05)

            X, Y, Z = fit_volatility_surface(chain_with_iv)

            if X is not None:
                fig = go.Figure(data=[go.Surface(
                    x=X, y=Y, z=Z, 
                    colorscale='Viridis',
                    opacity=0.9,
                    contours={
                        "z": {"show": True, "start": 0.05, "end": 0.8, "size": 0.05}
                    }
                )])
                
                fig.update_layout(
                    title="Dynamic Volatility Smile",
                    scene=dict(
                        xaxis_title='Strike Price (K)',
                        yaxis_title='Days to Expiration (T)',
                        zaxis_title='Implied Volatility ($\sigma$)',
                        camera=dict(eye=dict(x=1.5, y=-1.5, z=1.2))
                    ),
                    height=700,
                    margin=dict(l=0, r=0, b=0, t=40)
                )

                spot_metric.metric("Underlying Spot", f"{current_spot:.2f}")
                time_metric.metric("Last Update", time.strftime('%H:%M:%S'))
                status_metric.success("Streaming Active")
                chart_placeholder.plotly_chart(fig, use_container_width=True)
            else:
                status_metric.warning("Insufficient data to fit surface. Awaiting next tick...")

            time.sleep(5.0)
            
        except Exception as e:
            st.error(f"Stream interrupted: {e}")
            break

if __name__ == "__main__":
    main()