import streamlit as st
import pandas as pd
import numpy as np
import calculator

# --- Page Configuration ---
st.set_page_config(
    page_title="Ammonia Value Chain Analyzer",
    page_icon="🔗",
    layout="wide"
)

# --- Sidebar ---
with st.sidebar:
    st.image("https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/link.svg", width=80)
    st.title("🔗 Simulation Scenario")
    st.markdown("---")

    st.header("1. Set Production Target")
    target_ammonia_tonne = st.number_input(
        "Annual Ammonia Production Target (tonnes/year)",
        min_value=10000, max_value=10000000, value=180000, step=10000,
        help="Enter the target annual ammonia production, which is the primary goal of this simulation."
    )
    st.markdown("---")

    st.header("2. Configure Energy Supply")
    st.subheader("Renewable Energy")
    solar_cf = st.slider("Solar Capacity Factor (%)", 10.0, 30.0, 18.0, 0.5, help="The average annual capacity factor of the solar PV plant.") / 100
    wind_cf = st.slider("Wind Capacity Factor (%)", 20.0, 50.0, 35.0, 0.5, help="The average annual capacity factor of the wind power plant.") / 100
    solar_wind_ratio = st.slider(
        "Solar vs. Wind Generation Mix (%)", 0, 100, 50, 5,
        help="The percentage of total renewable generation supplied by solar. The remainder will be from wind."
    )

    st.subheader("Grid Power")
    grid_price = st.number_input("Grid Electricity Price ($/kWh)", 0.01, 0.5, 0.15, 0.01, help="The price of electricity from the grid, used when renewable generation is insufficient.")
    st.markdown("---")

    st.header("3. Financial Assumptions")
    discount_rate = st.slider("Discount Rate (%)", 1.0, 15.0, 8.0, 0.1) / 100
    plant_lifetime = st.slider("Plant Lifetime (years)", 10, 40, 25, 1)
    
    st.markdown("---")
    st.info("© 2024, HWAN-OH. All rights reserved.")

# --- Main Page ---
st.title("🔗 Ammonia Value Chain Analyzer")
st.markdown("Define a **production target** and **energy supply conditions** to analyze the LCOA and required infrastructure for the entire value chain.")
st.markdown("---")

# --- Project Vision ---
with st.expander("View Project Vision & Info"):
    st.markdown("""
    #### **The Project's Essence**
    The core vision of this application is to serve as a **"Comprehensive Economic Analyzer for the Ammonia Value Chain."** Beyond simple cost calculation, it aims to be a strategic decision-making tool that determines the optimal scale of renewable energy sources, electrolyzers, and synthesis plants required to meet a production target. Future versions will incorporate ammonia utilization scenarios (e.g., SOFC, hydrogen engines, co-firing).

    #### **About the Creator: [HWAN-OH](https://github.com/HWAN-OH)**
    The developer is focused on building digital systems that model and solve complex, real-world challenges. 
    This project shares its philosophy with his core vision, the **[MirrorMind Identity Protocol](https://github.com/HWAN-OH/MirrorMind-Identity-Protocol)**, and acts as a tangible, specialized digital persona with deep expertise in energy economics.
    """)

if st.button("🚀 Run Analysis", use_container_width=True):
    # --- 1. Reverse Calculation Logic ---
    total_kwh_needed = calculator.calculate_required_kwh(target_ammonia_tonne)
    required_re_capacity_kw = calculator.calculate_required_re_capacity(total_kwh_needed, solar_cf, wind_cf, solar_wind_ratio / 100)
    electrolyzer_capacity_kw = required_re_capacity_kw
    electrolyzer_utilization = calculator.calculate_electrolyzer_utilization(total_kwh_needed, electrolyzer_capacity_kw)

    # --- 2. Reconstruct config for LCOA calculation ---
    user_config = {
        'ELECTROLYZER_CAPACITY_KW': electrolyzer_capacity_kw,
        'SOLAR_CAPACITY_KW': required_re_capacity_kw * (solar_wind_ratio / 100),
        'WIND_CAPACITY_KW': required_re_capacity_kw * (1 - solar_wind_ratio / 100),
        'DISCOUNT_RATE': discount_rate,
        'PLANT_LIFETIME': plant_lifetime,
        'GRID_PRICE': grid_price,
    }

    with st.spinner('Analyzing the value chain economics...'):
        capex_costs = calculator.calculate_capital_costs(user_config, target_ammonia_tonne)
        opex_costs = calculator.calculate_annual_operating_costs(user_config, capex_costs, total_kwh_needed)
        lcoa_results = calculator.calculate_lcoa(user_config, capex_costs['total_capex'], opex_costs['total_annual_opex'], target_ammonia_tonne)

    st.success("✅ Analysis Complete!")
    st.markdown("---")

    # --- Display Results ---
    st.header("Overall Analysis Results")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Final LCOA", f"${lcoa_results['lcoa_final']:.2f}", "/tonne-NH3")
    col2.metric("Required Electrolyzer Capacity", f"{electrolyzer_capacity_kw/1000:,.1f}", "MW")
    col3.metric("Required Solar Capacity", f"{user_config['SOLAR_CAPACITY_KW']/1000:,.1f}", "MW")
    col4.metric("Electrolyzer Utilization", f"{electrolyzer_utilization*100:.1f}%")

    tab1, tab2 = st.tabs(["📊 Cost Breakdown", "📋 Infrastructure Specs"])

    with tab1:
        st.subheader("LCOA Cost Components")
        cost_df = pd.DataFrame.from_dict(
            lcoa_results['breakdown'], orient='index', columns=['Cost ($/tonne)']
        )
        st.bar_chart(cost_df)

    with tab2:
        st.subheader("Calculated Infrastructure Specifications")
        specs = {
            "Target Annual Ammonia Production (tonne/year)": target_ammonia_tonne,
            "Required Electrolyzer Capacity (MW)": electrolyzer_capacity_kw / 1000,
            "Required Solar PV Capacity (MW)": user_config['SOLAR_CAPACITY_KW'] / 1000,
            "Required Wind Power Capacity (MW)": user_config['WIND_CAPACITY_KW'] / 1000,
            "Calculated Electrolyzer Utilization Rate (%)": electrolyzer_utilization * 100,
            "Total Annual Power Requirement (GWh)": total_kwh_needed / 1_000_000,
        }
        st.dataframe(pd.Series(specs, name="Value"), use_container_width=True)
