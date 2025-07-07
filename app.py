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

    st.header("1. Production Target")
    target_ammonia_tonne = st.number_input(
        "Annual Ammonia Production Target (tonnes/year)",
        min_value=10000, max_value=10000000, value=180000, step=10000
    )
    st.markdown("---")

    st.header("2. Energy Management Strategy")
    energy_strategy = st.radio(
        "Select Strategy",
        ("Grid Balancing", "ESS Balancing"),
        help="Choose 'Grid Balancing' to use grid power or 'ESS Balancing' for a 100% clean, off-grid system."
    )
    
    grid_config = {}
    ess_config = {}

    if energy_strategy == "Grid Balancing":
        st.subheader("Grid Parameters")
        grid_config['purchase_price'] = st.number_input("Grid Purchase Price ($/kWh)", 0.01, 0.5, 0.15, 0.01)
    else: # ESS Balancing
        st.subheader("ESS Parameters")
        ess_config['capex_per_kwh'] = st.number_input("ESS CAPEX ($/kWh)", 100, 1000, 350, 10)
        ess_config['efficiency'] = st.slider("ESS Round-trip Efficiency (%)", 70.0, 95.0, 85.0, 0.5) / 100

    st.markdown("---")
    
    st.header("3. Shared Parameters")
    solar_cf = st.slider("Solar Capacity Factor (%)", 10.0, 30.0, 18.0, 0.5) / 100
    wind_cf = st.slider("Wind Capacity Factor (%)", 20.0, 50.0, 35.0, 0.5) / 100
    solar_wind_ratio = st.slider("Solar vs. Wind Generation Mix (%)", 0, 100, 50, 5)
    discount_rate = st.slider("Discount Rate (%)", 1.0, 15.0, 8.0, 0.1) / 100
    plant_lifetime = st.slider("Plant Lifetime (years)", 10, 40, 25, 1)

    st.markdown("---")
    st.info("© 2025, HWAN-OH. All rights reserved.")

# --- Main Page ---
st.title("🔗 Ammonia Value Chain Analyzer")
st.markdown("Define a **production target** and **energy strategy** to analyze the LCOA and required infrastructure.")
st.markdown("---")

with st.expander("View Project Vision & Info"):
    st.markdown("""
    #### **The Project's Essence**
    The core vision of this application is to serve as a **"Comprehensive Economic Analyzer for the Ammonia Value Chain."** Beyond simple cost calculation, it aims to be a strategic decision-making tool that determines the optimal scale of renewable energy sources, electrolyzers, and synthesis plants required to meet a production target. Future versions will incorporate ammonia utilization scenarios (e.g., SOFC, hydrogen engines, co-firing).

    #### **About the Creator: [HWAN-OH](https://github.com/HWAN-OH)**
    The developer is focused on building digital systems that model and solve complex, real-world challenges. 
    This project shares its philosophy with his core vision, the **[MirrorMind Identity Protocol](https://github.com/HWAN-OH/MirrorMind-Identity-Protocol)**, and acts as a tangible, specialized digital persona with deep expertise in energy economics.
    """)

if st.button("🚀 Run Analysis", use_container_width=True):
    # --- 1. Reverse Calculation ---
    total_kwh_needed = calculator.calculate_required_kwh(target_ammonia_tonne)
    required_re_capacity_kw = calculator.calculate_required_re_capacity(total_kwh_needed, solar_cf, wind_cf, solar_wind_ratio / 100)
    electrolyzer_capacity_kw = required_re_capacity_kw
    electrolyzer_utilization = calculator.calculate_electrolyzer_utilization(total_kwh_needed, electrolyzer_capacity_kw)

    # --- 2. Reconstruct config for LCOA calculation ---
    base_config = {
        'ELECTROLYZER_CAPACITY_KW': electrolyzer_capacity_kw,
        'SOLAR_CAPACITY_KW': required_re_capacity_kw * (solar_wind_ratio / 100),
        'WIND_CAPACITY_KW': required_re_capacity_kw * (1 - solar_wind_ratio / 100),
        'DISCOUNT_RATE': discount_rate,
        'PLANT_LIFETIME': plant_lifetime,
    }

    with st.spinner(f'Analyzing economics for **{energy_strategy}** scenario...'):
        # --- FIX: Pass 'total_kwh_needed' to the function ---
        capex_costs = calculator.calculate_capital_costs(
            base_config, 
            target_ammonia_tonne,
            total_kwh_needed, # This argument is now correctly passed
            energy_strategy, 
            ess_config, 
            solar_wind_ratio / 100
        )
        
        opex_costs = calculator.calculate_annual_operating_costs(base_config, capex_costs, total_kwh_needed, energy_strategy, grid_config)
        lcoa_results = calculator.calculate_lcoa(base_config, capex_costs['total_capex'], opex_costs['total_annual_opex'], target_ammonia_tonne)

    st.success("✅ Analysis Complete!")
    st.markdown("---")

    # --- Display Results ---
    st.header(f"Analysis Results: *{energy_strategy}*")
    col1, col2, col3 = st.columns(3)
    col1.metric("Final LCOA", f"${lcoa_results['lcoa_final']:.2f}", "/tonne-NH3")
    col2.metric("Total CAPEX", f"${capex_costs['total_capex']/1_000_000:.1f}M")
    col3.metric("Annual OPEX", f"${opex_costs['total_annual_opex']/1_000_000:.2f}M")

    tab1, tab2 = st.tabs(["📊 Cost Breakdown", "📋 Infrastructure Specs"])

    with tab1:
        st.subheader("LCOA Cost Components")
        if 'breakdown' in lcoa_results and lcoa_results['breakdown']:
            cost_df = pd.DataFrame.from_dict(
                lcoa_results['breakdown'], orient='index', columns=['Cost ($/tonne)']
            )
            st.bar_chart(cost_df)
        else:
            st.warning("Could not generate cost breakdown.")

    with tab2:
        st.subheader("Calculated Infrastructure Specifications")
        specs = {
            "Energy Strategy": energy_strategy,
            "Target Production (tonne/year)": target_ammonia_tonne,
            "Required Electrolyzer Capacity (MW)": electrolyzer_capacity_kw / 1000,
            "Required Solar PV Capacity (MW)": base_config['SOLAR_CAPACITY_KW'] / 1000,
            "Required Wind Power Capacity (MW)": base_config['WIND_CAPACITY_KW'] / 1000,
        }
        if energy_strategy == 'ESS Balancing':
            specs["Calculated ESS Storage Duration (Hours)"] = capex_costs.get('calculated_storage_duration_hours', 0)
            specs["Required ESS Capacity (MWh)"] = capex_costs.get('ess_capacity_mwh', 0)
        
        st.dataframe(pd.Series(specs, name="Value"), use_container_width=True)
