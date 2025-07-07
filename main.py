 app.py
import streamlit as st
import pandas as pd
import calculator # 수정된 calculator 모듈

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="Green Ammonia LCOA Simulator",
    page_icon="💡",
    layout="wide"
)

# --- 사이드바: 사용자 입력 ---
st.sidebar.header("Simulation Parameters")

# 재무 가정
st.sidebar.subheader("Financial Assumptions")
discount_rate = st.sidebar.slider("Discount Rate (%)", 1.0, 15.0, 8.0, 0.1) / 100
plant_lifetime = st.sidebar.slider("Plant Lifetime (years)", 10, 40, 25, 1)
inflation_rate = st.sidebar.slider("Inflation Rate (%)", 0.0, 5.0, 2.0, 0.1) / 100

# 플랜트 사양
st.sidebar.subheader("Plant Specifications")
plant_capacity_mw = st.sidebar.number_input("Plant Capacity (MW)", min_value=100, max_value=5000, value=1000, step=100)
capacity_factor = st.sidebar.slider("Capacity Factor (%)", 50.0, 100.0, 90.0, 0.5) / 100
electricity_cost = st.sidebar.number_input("Electricity Cost ($/kWh)", min_value=0.01, max_value=0.20, value=0.05, step=0.01, format="%.3f")

# 운송
st.sidebar.subheader("Transportation")
transport_distance_km = st.sidebar.number_input("Transport Distance (km)", min_value=0, max_value=10000, value=1000, step=100)

# --- 메인 페이지 ---
st.title("💡 Green Ammonia LCOA Simulator")
st.markdown("This tool calculates the Levelized Cost of Ammonia (LCOA) based on your input parameters.")

# 시뮬레이션 실행 버튼
if st.button("Run Simulation"):
    # 사용자 입력을 기반으로 config 딕셔너리 생성
    user_config = {
        'PLANT_CAPACITY_KW': plant_capacity_mw * 1000,
        'CAPACITY_FACTOR': capacity_factor,
        'H2_LHV': 33.33,
        'ELECTROLYZER_EFFICIENCY': 0.70,
        'ELECTROLYZER_CAPEX': 450,
        'ELECTROLYZER_LIFETIME': 10,
        'ASU_CAPEX': 150,
        'HB_CAPEX': 550,
        'STORAGE_CAPEX': 500,
        'ELECTROLYZER_OPEX_RATE': 0.015,
        'ASU_OPEX_RATE': 0.02,
        'HB_OPEX_RATE': 0.025,
        'STORAGE_OPEX_RATE': 0.01,
        'ELECTRICITY_COST': electricity_cost,
        'DISCOUNT_RATE': discount_rate,
        'PLANT_LIFETIME': plant_lifetime,
        'INFLATION_RATE': inflation_rate,
        'TRANSPORT_DISTANCE_KM': transport_distance_km,
        'TRANSPORT_COST_PER_TON_KM': 0.05
    }

    with st.spinner('Calculating LCOA...'):
        # 1. 연간 생산량 계산
        annual_h2_kg, annual_nh3_tonne = calculator.calculate_annual_production(user_config)

        # 2. CAPEX 계산
        capex_costs = calculator.calculate_capital_costs(user_config, annual_nh3_tonne)

        # 3. OPEX 계산
        opex_costs = calculator.calculate_annual_operating_costs(user_config, capex_costs)

        # 4. LCOA 계산
        lcoa_results = calculator.calculate_lcoa(user_config, capex_costs['total_capex_with_replacement'], opex_costs['total_annual_opex'], annual_nh3_tonne)

    st.success("Calculation Complete!")

    # --- 결과 표시 ---
    st.header("Simulation Results")

    # 최종 LCOA 메트릭
    col1, col2, col3 = st.columns(3)
    col1.metric("Final LCOA", f"${lcoa_results['lcoa_final']:.2f}", "/tonne")
    col2.metric("Production Cost", f"${lcoa_results['lcoa_production']:.2f}", "/tonne")
    col3.metric("Transport Cost", f"${lcoa_results['transport_cost_per_tonne']:.2f}", "/tonne")

    # 비용 구성 바 차트
    st.subheader("Cost Breakdown ($/tonne)")
    cost_breakdown_data = {
        'Annualized CAPEX': lcoa_results['annualized_capex'] / annual_nh3_tonne if annual_nh3_tonne > 0 else 0,
        'Annual OPEX': opex_costs['total_annual_opex'] / annual_nh3_tonne if annual_nh3_tonne > 0 else 0,
        'Transport Cost': lcoa_results['transport_cost_per_tonne']
    }
    cost_df = pd.DataFrame.from_dict(cost_breakdown_data, orient='index', columns=['Cost per Tonne'])
    st.bar_chart(cost_df)

    # 상세 결과 expander
    with st.expander("Show Detailed Results"):
        st.subheader("Production")
        st.text(f"Annual Ammonia Production: {annual_nh3_tonne:,.2f} tonnes")
        
        st.subheader("Capital Expenditures (CAPEX)")
        st.dataframe(pd.DataFrame([capex_costs]))

        st.subheader("Operating Expenditures (OPEX)")
        st.dataframe(pd.DataFrame([opex_costs]))
        
        st.subheader("Levelized Cost Analysis")
        st.dataframe(pd.DataFrame([lcoa_results]))

        # 다운로드용 전체 결과 취합
        final_results = {
            "Plant Capacity (MW)": plant_capacity_mw,
            "Capacity Factor (%)": capacity_factor * 100,
            "Electricity Cost ($/kWh)": electricity_cost,
            "Discount Rate (%)": discount_rate * 100,
            "Annual NH3 Production (tonne)": annual_nh3_tonne,
            **{f"CAPEX - {k.replace('_', ' ').title()} ($)": v for k, v in capex_costs.items()},
            **{f"OPEX - {k.replace('_', ' ').title()} ($)": v for k, v in opex_costs.items()},
            **{f"LCOA - {k.replace('_', ' ').title()} ($/tonne)": v for k, v in lcoa_results.items()},
        }
        csv = pd.DataFrame([final_results]).to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="Download Full Results as CSV",
            data=csv,
            file_name='LCOA_results.csv',
            mime='text/csv',
        )
