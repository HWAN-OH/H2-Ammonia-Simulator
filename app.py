import streamlit as st
import pandas as pd
import numpy as np
import calculator

# --- Page Configuration ---
st.set_page_config(
    page_title="Green Ammonia LCOA Simulator",
    page_icon="🌿",
    layout="wide"
)

# --- Sidebar ---
with st.sidebar:
    # You can replace this URL with your actual logo image
    st.image("https://raw.githubusercontent.com/HWAN-OH/MirrorMind-Identity-Protocol/main/logo.png", width=100)
    st.title("🌿 Simulation Parameters")
    st.markdown("---")

    # Financial Assumptions
    st.subheader("Financial Assumptions")
    discount_rate = st.slider("Discount Rate (%)", 1.0, 15.0, 8.0, 0.1, help="The rate used to discount future cash flows to their present value.") / 100
    plant_lifetime = st.slider("Plant Lifetime (years)", 10, 40, 25, 1)
    inflation_rate = st.slider("Inflation Rate (%)", 0.0, 5.0, 2.0, 0.1) / 100

    # Plant Specifications
    st.subheader("Plant Specifications")
    plant_capacity_mw = st.number_input("Plant Capacity (MW)", min_value=100, max_value=5000, value=1000, step=100)
    capacity_factor = st.slider("Capacity Factor (%)", 50.0, 100.0, 90.0, 0.5) / 100
    electricity_cost = st.number_input("Electricity Cost ($/kWh)", min_value=0.01, max_value=0.20, value=0.05, step=0.01, format="%.3f")

    # Transportation
    st.subheader("Transportation")
    transport_distance_km = st.number_input("Transport Distance (km)", min_value=0, max_value=10000, value=1000, step=100)
    
    st.markdown("---")
    st.info("© 2024, HWAN-OH. All rights reserved.")


# --- Main Page ---
st.title("🌿 Green Ammonia LCOA Simulator")
st.markdown("""
This simulator is designed to analyze the economic feasibility of sustainable energy projects. 
Adjust the variables on the left to calculate the **Levelized Cost of Ammonia (LCOA)** across the entire value chain.
""")
st.markdown("---")

# --- About Section ---
with st.expander("About the Project & Creator"):
    st.markdown("""
    #### **Creator: [HWAN-OH](https://github.com/HWAN-OH)**
    This application was developed by HWAN-OH, a developer focused on building digital systems that model and solve complex, real-world challenges. His work centers on creating 'digital twins' and specialized AI personas to transform abstract data into tangible solutions.

    #### **Project Philosophy: The MirrorMind Connection**
    This simulator is a practical application of a broader vision: the **[MirrorMind Identity Protocol](https://github.com/HWAN-OH/MirrorMind-Identity-Protocol)**. 
    If MirrorMind is the hub for designing versatile digital identities, this LCOA simulator represents a highly specialized persona with deep expertise in energy economics. It demonstrates how a well-defined digital model can be deployed to tackle specific, high-impact problems.
    """)

# Run Simulation Button
if st.button("🚀 Run Simulation", use_container_width=True):
    user_config = {
        'PLANT_CAPACITY_KW': plant_capacity_mw * 1000, 'CAPACITY_FACTOR': capacity_factor,
        'H2_LHV': 33.33, 'ELECTROLYZER_EFFICIENCY': 0.70, 'ELECTROLYZER_CAPEX': 450,
        'ELECTROLYZER_LIFETIME': 10, 'ASU_CAPEX': 150, 'HB_CAPEX': 550, 'STORAGE_CAPEX': 500,
        'ELECTROLYZER_OPEX_RATE': 0.015, 'ASU_OPEX_RATE': 0.02, 'HB_OPEX_RATE': 0.025,
        'STORAGE_OPEX_RATE': 0.01, 'ELECTRICITY_COST': electricity_cost, 'DISCOUNT_RATE': discount_rate,
        'PLANT_LIFETIME': plant_lifetime, 'INFLATION_RATE': inflation_rate,
        'TRANSPORT_DISTANCE_KM': transport_distance_km, 'TRANSPORT_COST_PER_TON_KM': 0.05
    }

    with st.spinner('Calculating LCOA... Please wait.'):
        annual_h2_kg, annual_nh3_tonne = calculator.calculate_annual_production(user_config)
        capex_costs = calculator.calculate_capital_costs(user_config, annual_nh3_tonne)
        opex_costs = calculator.calculate_annual_operating_costs(user_config, capex_costs)
        lcoa_results = calculator.calculate_lcoa(user_config, capex_costs['total_capex_with_replacement'], opex_costs['total_annual_opex'], annual_nh3_tonne)

    st.success("✅ Calculation Complete!")
    st.markdown("---")

    # --- Results Tabs ---
    tab1, tab2, tab3 = st.tabs(["📊 Summary", "📋 Cost Details", "📈 Sensitivity Analysis"])

    with tab1:
        st.header("Key Result Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Final LCOA", f"${lcoa_results['lcoa_final']:.2f}", "/tonne", help="The final levelized cost including production, storage, and transport.")
        col2.metric("Production LCOA", f"${lcoa_results['lcoa_production']:.2f}", "/tonne", help="The levelized cost at the production facility, excluding transport.")
        col3.metric("Annual Production", f"{annual_nh3_tonne:,.0f}", "tonnes/year")

        st.subheader("Cost Component Breakdown")
        if annual_nh3_tonne > 0:
            cost_breakdown_data = {
                'Cost Type': ['Annualized CAPEX', 'Annual OPEX', 'Transport Cost'],
                'Cost per Tonne ($/tonne)': [
                    lcoa_results['annualized_capex'] / annual_nh3_tonne,
                    opex_costs['total_annual_opex'] / annual_nh3_tonne,
                    lcoa_results['transport_cost_per_tonne']
                ]
            }
            cost_df = pd.DataFrame(cost_breakdown_data)
            st.bar_chart(cost_df.set_index('Cost Type'))
        else:
            st.warning("Annual production is zero. Cannot display cost breakdown chart.")

    with tab2:
        st.header("Detailed Cost Breakdown")
        st.subheader("Capital Expenditures (CAPEX)")
        capex_df = pd.DataFrame.from_dict(capex_costs, orient='index', columns=['Cost ($)'])
        st.dataframe(capex_df, use_container_width=True)

        st.subheader("Annual Operating Expenditures (OPEX)")
        opex_df = pd.DataFrame.from_dict(opex_costs, orient='index', columns=['Cost ($)'])
        st.dataframe(opex_df, use_container_width=True)

    with tab3:
        st.header("LCOA Sensitivity to Electricity Cost")
        st.markdown("Analyze how changes in the electricity price impact the final LCOA.")
        
        sensitivity_range = np.linspace(max(0.01, electricity_cost - 0.04), electricity_cost + 0.04, 20)
        lcoa_values = []

        for cost in sensitivity_range:
            temp_config = user_config.copy()
            temp_config['ELECTRICITY_COST'] = cost
            
            _, temp_nh3_tonne = calculator.calculate_annual_production(temp_config)
            temp_capex = calculator.calculate_capital_costs(temp_config, temp_nh3_tonne)
            temp_opex = calculator.calculate_annual_operating_costs(temp_config, temp_capex)
            temp_lcoa = calculator.calculate_lcoa(temp_config, temp_capex['total_capex_with_replacement'], temp_opex['total_annual_opex'], temp_nh3_tonne)
            lcoa_values.append(temp_lcoa['lcoa_final'])

        sensitivity_df = pd.DataFrame({
            'Electricity Cost ($/kWh)': sensitivity_range,
            'Final LCOA ($/tonne)': lcoa_values
        })
        
        st.line_chart(sensitivity_df.rename(columns={'Electricity Cost ($/kWh)':'index'}).set_index('index'))
        st.dataframe(sensitivity_df, use_container_width=True)

