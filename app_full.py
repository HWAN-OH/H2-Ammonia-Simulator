
import streamlit as st
import numpy as np

# -----------------------
# Title and Introduction
# -----------------------
st.title("🌱 H2-Ammonia Reverse Simulator")
st.markdown("""
This simulator estimates the required capacity of solar/wind power generation, electrolyzers, hydrogen tanks, and total investment to produce a **target annual ammonia (NH₃) output**.

The model is reverse-engineered from ammonia demand → hydrogen → power input.
""")

# -----------------------
# User Inputs
# -----------------------
st.sidebar.header("📥 Input Parameters")

target_nh3_ton = st.sidebar.number_input("Target NH₃ production (tons/year)", 10000, 1000000, 100000, step=10000)
electrolyzer_type = st.sidebar.selectbox("Electrolyzer Type", ["PEM", "AWE", "SOEC"])
power_source = st.sidebar.selectbox("Power Supply Type", ["Grid", "Solar + Wind", "Solar + ESS"])
elec_price = st.sidebar.number_input("Electricity price ($/kWh)", 0.01, 1.00, 0.08, step=0.01)

# Tech specs per electrolyzer type
electrolyzer_eff = {"PEM": 53, "AWE": 49, "SOEC": 39}  # kWh/kg-H2
capex_per_kw = {"PEM": 900, "AWE": 700, "SOEC": 1200}  # USD/kW
eff = electrolyzer_eff[electrolyzer_type]
capex = capex_per_kw[electrolyzer_type]

# -----------------------
# Constants
# -----------------------
NH3_H2_RATIO = 0.178  # 1 ton NH3 requires 0.178 ton H2
H2_LHV = 33.33  # kWh/kg
NH3_YEAR = target_nh3_ton
H2_YEAR = NH3_YEAR * NH3_H2_RATIO
H2_KG = H2_YEAR * 1000

# -----------------------
# Core Calculations
# -----------------------
energy_needed_kwh = H2_KG * eff  # total electricity needed
annual_hours = 8760

# Case 1: Grid → Assume 100% uptime
if power_source == "Grid":
    required_power_kw = energy_needed_kwh / annual_hours
    buffer_h2 = 0
    uptime = 1.0

# Case 2: Solar + Wind → Assume 60% uptime → Add buffer
elif power_source == "Solar + Wind":
    uptime = 0.6
    required_power_kw = energy_needed_kwh / (annual_hours * uptime)
    daily_h2 = H2_KG / 365
    buffer_h2 = daily_h2 * (1 - uptime) * 3  # 3일치 여유분

# Case 3: Solar + ESS → 100% uptime 가정, ESS는 LCOA 고려에만 반영
else:
    uptime = 1.0
    required_power_kw = energy_needed_kwh / annual_hours
    buffer_h2 = 0

total_capex = required_power_kw * capex
lcoa = (energy_needed_kwh * elec_price) / NH3_YEAR + (total_capex / (NH3_YEAR * 20))  # simple LCOA

# -----------------------
# Results
# -----------------------
st.subheader("📊 Results Summary")

st.markdown(f"**Electrolyzer type:** {electrolyzer_type}")
st.markdown(f"**Target NH₃ production:** {target_nh3_ton:,} tons/year")
st.markdown(f"**Hydrogen required:** {H2_KG:,.0f} kg/year")
st.markdown(f"**Electricity needed:** {energy_needed_kwh:,.0f} kWh/year")
st.markdown(f"**Required power capacity:** {required_power_kw:,.0f} kW")
st.markdown(f"**Estimated hydrogen tank buffer:** {buffer_h2:,.0f} kg")
st.markdown(f"**Estimated total CAPEX:** ${total_capex/1e6:,.2f} M")
st.markdown(f"**Estimated LCOA:** ${lcoa:,.2f} /ton")

# Footer
st.markdown("---")
st.caption("Created by Seunghwan Oh • MirrorMind Project • July 2025")
