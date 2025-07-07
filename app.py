
import streamlit as st
import numpy as np

st.set_page_config(page_title="H2-Ammonia Simulator", layout="wide")

st.title("💧 H2-Ammonia LCOA Simulator")

# Sidebar inputs
st.sidebar.header("Simulation Inputs")
nh3_production = st.sidebar.number_input("Target NH₃ Production (tons/year)", min_value=10000, value=100000, step=10000)
electrolyzer_type = st.sidebar.selectbox("Electrolyzer Type", ["PEM", "AWE", "SOEC"])
power_source = st.sidebar.selectbox("Power Source", ["Grid", "Solar + Wind", "Solar + ESS"])

solar_capex = st.sidebar.number_input("Solar CAPEX ($/kW)", value=800)
wind_capex = st.sidebar.number_input("Wind CAPEX ($/kW)", value=1300)
ess_price = st.sidebar.number_input("ESS Price ($/kWh)", value=400)
grid_price = st.sidebar.number_input("Grid electricity price ($/kWh)", value=0.12)

if st.button("Run Simulation"):
    st.subheader("Simulation Results")

    # Placeholder simulation logic
    st.write(f"Electrolyzer: **{electrolyzer_type}**")
    st.write(f"Power Source: **{power_source}**")
    st.write(f"Target NH₃ Production: **{nh3_production:,} tons/year**")

    # Dummy calculation for LCOA
    base_cost = 600  # Base $/ton
    adjustment = 0
    if electrolyzer_type == "SOEC":
        adjustment += 100
    if power_source == "Solar + ESS":
        adjustment += 200
    elif power_source == "Solar + Wind":
        adjustment += 100

    lcoa = base_cost + adjustment + (solar_capex + wind_capex) * 0.01
    st.metric("Estimated LCOA", f"${lcoa:.2f} / ton")

else:
    st.info("⬅️ Adjust simulation parameters and press **Run Simulation**.")

st.caption("Created by HWAN-OH | MirrorMind Project")
