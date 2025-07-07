import numpy as np

# --- Constants ---
H2_LHV = 33.33
ELECTROLYZER_EFFICIENCY = 0.70
H2_KG_PER_TONNE_NH3 = (3 / 17.031) * 1000

ELECTROLYZER_CAPEX_PER_KW = 450
SOLAR_CAPEX_PER_KW = 600
WIND_CAPEX_PER_KW = 1200
HB_CAPEX_PER_KW_ELECTROLYZER = 550
STORAGE_CAPEX_PER_TONNE = 500

ELECTROLYZER_OPEX_RATE = 0.015
RE_OPEX_RATE = 0.015
HB_OPEX_RATE = 0.025
STORAGE_OPEX_RATE = 0.01
ESS_OPEX_RATE = 0.01

INFLATION_RATE = 0.02

# --- Calculation Functions ---
def calculate_required_kwh(target_ammonia_tonne):
    required_h2_kg = target_ammonia_tonne * H2_KG_PER_TONNE_NH3
    kwh_per_kg_h2 = H2_LHV / ELECTROLYZER_EFFICIENCY
    return required_h2_kg * kwh_per_kg_h2

def calculate_required_re_capacity(total_kwh_needed, solar_cf, wind_cf, solar_ratio):
    avg_re_cf = (solar_cf * solar_ratio) + (wind_cf * (1 - solar_ratio))
    if avg_re_cf == 0: return 0
    avg_power_kw = total_kwh_needed / (365 * 24)
    return avg_power_kw / avg_re_cf

def calculate_electrolyzer_utilization(total_kwh_needed, electrolyzer_capacity_kw):
    if electrolyzer_capacity_kw == 0: return 0
    return total_kwh_needed / (electrolyzer_capacity_kw * 365 * 24)

# --- FIX: Added 'total_kwh_needed' as an argument ---
def calculate_capital_costs(base_config, target_ammonia_tonne, total_kwh_needed, strategy, ess_config={}, solar_wind_ratio=0.5):
    """Calculates total CAPEX based on the selected energy strategy."""
    electrolyzer_capex = base_config['ELECTROLYZER_CAPACITY_KW'] * ELECTROLYZER_CAPEX_PER_KW
    solar_capex = base_config['SOLAR_CAPACITY_KW'] * SOLAR_CAPEX_PER_KW
    wind_capex = base_config['WIND_CAPACITY_KW'] * WIND_CAPEX_PER_KW
    hb_capex = base_config['ELECTROLYZER_CAPACITY_KW'] * HB_CAPEX_PER_KW_ELECTROLYZER
    storage_capex = target_ammonia_tonne * 0.1 * STORAGE_CAPEX_PER_TONNE
    
    replacement_cost = electrolyzer_capex * ((1 + INFLATION_RATE) ** 10)
    replacement_pv = replacement_cost / ((1 + base_config['DISCOUNT_RATE']) ** 10)
    
    total_capex = electrolyzer_capex + solar_capex + wind_capex + hb_capex + storage_capex + replacement_pv
    
    capex_breakdown = {
        "electrolyzer_capex": electrolyzer_capex, "solar_capex": solar_capex,
        "wind_capex": wind_capex, "haber_bosch_capex": hb_capex,
        "storage_capex": storage_capex, "electrolyzer_replacement_pv": replacement_pv
    }

    if strategy == 'ESS Balancing':
        max_storage_hours = 14
        min_storage_hours = 6
        storage_duration_hours = (max_storage_hours - min_storage_hours) * solar_wind_ratio + min_storage_hours
        
        # Now this calculation will work correctly
        avg_power_consumption_kw = total_kwh_needed / (365 * 24)
        ess_capacity_kwh = avg_power_consumption_kw * storage_duration_hours
        
        ess_capex = ess_capacity_kwh * ess_config['capex_per_kwh']
        total_capex += ess_capex
        
        capex_breakdown['ess_capex'] = ess_capex
        capex_breakdown['ess_capacity_mwh'] = ess_capacity_kwh / 1000
        capex_breakdown['calculated_storage_duration_hours'] = storage_duration_hours

    capex_breakdown['total_capex'] = total_capex
    return capex_breakdown

def calculate_annual_operating_costs(base_config, capex_costs, total_kwh_needed, strategy, grid_config={}):
    """Calculates total annual OPEX based on the selected energy strategy."""
    electrolyzer_opex = capex_costs['electrolyzer_capex'] * ELECTROLYZER_OPEX_RATE
    re_opex = (capex_costs['solar_capex'] + capex_costs['wind_capex']) * RE_OPEX_RATE
    hb_opex = capex_costs['haber_bosch_capex'] * HB_OPEX_RATE
    storage_opex = capex_costs['storage_capex'] * STORAGE_OPEX_RATE
    
    fixed_opex = electrolyzer_opex + re_opex + hb_opex + storage_opex
    variable_opex = 0

    if strategy == 'Grid Balancing':
        grid_power_kwh = total_kwh_needed * 0.30
        variable_opex = grid_power_kwh * grid_config['purchase_price']
    else: # ESS Balancing
        ess_opex = capex_costs.get('ess_capex', 0) * ESS_OPEX_RATE
        fixed_opex += ess_opex
    
    total_opex = fixed_opex + variable_opex
    
    return {
        "fixed_opex": fixed_opex,
        "variable_opex (grid_cost)": variable_opex,
        "total_annual_opex": total_opex
    }

def calculate_lcoa(base_config, total_capex, total_annual_opex, target_ammonia_tonne):
    if target_ammonia_tonne == 0: return {"lcoa_final": 0, "breakdown": {}}

    crf_denominator = ((1 + base_config['DISCOUNT_RATE']) ** base_config['PLANT_LIFETIME']) - 1
    if crf_denominator == 0: return {"lcoa_final": 0, "breakdown": {}}
    crf = (base_config['DISCOUNT_RATE'] * (1 + base_config['DISCOUNT_RATE']) ** base_config['PLANT_LIFETIME']) / crf_denominator
          
    annualized_capex = total_capex * crf
    total_annual_cost = annualized_capex + total_annual_opex
    lcoa_final = total_annual_cost / target_ammonia_tonne
    
    breakdown = {
        "Annualized CAPEX": annualized_capex / target_ammonia_tonne,
        "Annual OPEX": total_annual_opex / target_ammonia_tonne
    }
    
    return {"lcoa_final": lcoa_final, "breakdown": breakdown}
