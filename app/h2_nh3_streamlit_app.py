
import streamlit as st
import numpy as np

st.set_page_config(page_title="H2-NH3 시뮬레이터", layout="wide")

st.title("🌱 H2-Ammonia Simulator")
st.markdown("암모니아 목표 생산량을 기준으로 설비 규모와 LCOA를 계산합니다.")

# ------------------------
# 🔌 전력 공급 방식 선택
# ------------------------
power_source = st.selectbox(
    "전력 공급 방식 선택",
    options=[
        "태양광 + 풍력 (간헐적 운전)",
        "태양광 + 풍력 + ESS (연속 운전)",
        "일반 전력망 (그리드 전기)"
    ]
)

if "그리드" in power_source:
    grid_price = st.number_input("전기요금 (원/kWh)", min_value=0.0, step=10.0, value=100.0)
    electrolyzer_capacity_factor = 1.0
    use_h2_tank = False
    use_ess = False
else:
    grid_price = 0.0
    if "ESS" in power_source:
        electrolyzer_capacity_factor = 1.0
        use_ess = True
        use_h2_tank = False
    else:
        electrolyzer_capacity_factor = 0.6
        use_ess = False
        use_h2_tank = True

# ------------------------
# 📥 입력값
# ------------------------
target_nh3_ton = st.number_input("🎯 연간 NH₃ 목표 생산량 (톤)", value=100000)
nh3_per_h2 = 0.17647  # 1kg H2 → 5.67kg NH3 → 1톤 NH3에 필요한 H2 = 176.47 kg
h2_needed_kg = target_nh3_ton * nh3_per_h2 * 1000
elec_per_kg_h2 = 50  # kWh/kg-H2
annual_h2_energy_kwh = h2_needed_kg * elec_per_kg_h2 / electrolyzer_capacity_factor

# ------------------------
# ☀️ 재생에너지 설정
# ------------------------
solar_cf = st.slider("☀️ 태양광 용량계수 (Capacity Factor)", 0.1, 0.25, 0.18)
wind_cf = st.slider("💨 풍력 용량계수 (Capacity Factor)", 0.2, 0.5, 0.35)
solar_ratio = st.slider("태양광 비중 (%)", 0, 100, 50) / 100
wind_ratio = 1 - solar_ratio

solar_energy = annual_h2_energy_kwh * solar_ratio
wind_energy = annual_h2_energy_kwh * wind_ratio

solar_capacity_mw = solar_energy / (8760 * solar_cf)
wind_capacity_mw = wind_energy / (8760 * wind_cf)

# ------------------------
# ⚙️ CAPEX 계산
# ------------------------
capex = {}
capex['Electrolyzer'] = h2_needed_kg / 1000 / electrolyzer_capacity_factor * 1000  # 만원/MW 기준
capex['태양광'] = solar_capacity_mw * 1200 if grid_price == 0 else 0
capex['풍력'] = wind_capacity_mw * 2500 if grid_price == 0 else 0
capex['ESS'] = solar_capacity_mw * 500 if use_ess else 0
capex['수소탱크'] = h2_needed_kg * 0.1 if use_h2_tank else 0  # 단순 비례 계산

total_capex = sum(capex.values())

# ------------------------
# 💸 OPEX 계산
# ------------------------
opex = grid_price * annual_h2_energy_kwh / 1000 if grid_price > 0 else 0

# ------------------------
# 📤 출력
# ------------------------
st.subheader("📊 결과 요약")
st.markdown(f"**총 설비 CAPEX**: {total_capex:,.0f} 만원")
st.markdown(f"**연간 전기요금(OPEX)**: {opex:,.0f} 원")
lcoa = (total_capex * 1e4 + opex) / target_nh3_ton  # 원/톤
st.markdown(f"**LCOA (원/톤)**: {lcoa:,.0f}")
