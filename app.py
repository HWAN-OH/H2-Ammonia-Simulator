
import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="H2-Ammonia Simulator", layout="wide")

st.title("H2-Ammonia Simulator")
st.subheader("Reverse engineering from annual ammonia production target")

st.sidebar.header("Input Parameters")

annual_nh3_ton = st.sidebar.number_input("Annual Ammonia Production Target (tons)", min_value=1000, value=100000, step=1000)
electrolyzer_type = st.sidebar.selectbox("Electrolyzer Type", ["PEM", "AWE (Alkaline)", "SOEC"])
power_source = st.sidebar.selectbox("Power Supply Method", ["Solar + Wind", "Grid", "Solar + ESS"])

st.markdown("### Assumptions")
st.markdown(""" 
- Hydrogen energy density: **33.33 kWh/kg**  
- 1 Nm^3 hydrogen ≈ **0.08988 kg**  
- Minimum operating rate for ammonia plant: **60%**
""")
st.markdown("### Simulation results will appear here")
st.info("This is a placeholder for simulation results.")

st.divider()
st.caption("Generated as part of the MirrorMind project · July 2025")
st.caption("Developed by Seunghwan Oh")
