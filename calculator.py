import numpy as np

# --- Constants: Fixed technical and cost parameters ---
H2_LHV = 33.33  # Lower Heating Value of Hydrogen (kWh/kg)
ELECTROLYZER_EFFICIENCY = 0.70  # Efficiency of the electrolyzer
KG_H2_PER_KG_NH3 = 3 / 17.031 # Stoichiometric ratio of H2 in NH3
H2_KG_PER_TONNE_NH3 = KG_H2_PER_KG_NH3 * 1000

# CAPEX assumptions
ELECTROLYZER_CAPEX_PER_KW = 450  # $/kW
SOLAR_CAPEX_PER_KW = 600 # $/kW
WIND_CAPEX_PER_KW = 1200 # $/kW
HB_CAPEX_PER_KW_ELECTROLYZER = 550 # Haber-Bosch CAPEX relative to electrolyzer capacity ($/kW)
STORAGE_CAPEX_PER_TONNE = 500 # $/tonne

# OPEX assumptions (as a percentage of CAPEX)
ELECTROLYZER_OPEX_RATE = 0.015
RE_OPEX_RATE = 0.015 # For both Solar and Wind
HB_OPEX_RATE = 0.025
STORAGE_OPEX_RATE = 0.01

INFLATION_RATE = 0.02 # Used for calculating electrolyzer replacement cost

def calculate_required_kwh(target_ammonia_tonne):
    """Calculates the total annual kWh required for the target ammonia production."""
    required_h2_kg = target_ammonia_tonne * H2_KG_PER_TONNE_NH3
    kwh_per_kg_h2 = H2_LHV / ELECTROLYZER_EFFICIENCY
    total_kwh = required_h2_kg * kwh_per_kg_h2
    return total_kwh

def calculate_required_re_capacity(total_kwh_needed, solar_cf, wind_cf, solar_ratio):
    """Calculates the required renewable energy capacity (kW) to supply the needed energy."""
    hours_in_year = 365 * 24
    
    # Weighted average capacity factor for the entire renewable plant
    avg_re_cf = (solar_cf * solar_ratio) + (wind_cf * (1 - solar_ratio))
    
    if avg_re_cf == 0:
        return 0
        
    # Average power output required throughout the year (kW)
    avg_power_kw = total_kwh_needed / hours_in_year
    
    # Required capacity (kW) = Average Power / Capacity Factor
    required_capacity_kw = avg_power_kw / avg_re_cf
    return required_capacity_kw

def calculate_electrolyzer_utilization(total_kwh_needed, electrolyzer_capacity_kw):
    """Calculates the annual utilization rate of the electrolyzer."""
    if electrolyzer_capacity_kw == 0:
        return 0
    max_possible_kwh = electrolyzer_capacity_kw * 365 * 24
    return total_kwh_needed / max_possible_kwh

def calculate_capital_costs(config, target_ammonia_tonne):
    """Calculates the total capital expenditures (CAPEX)."""
    electrolyzer_capex = config['ELECTROLYZER_CAPACITY_KW'] * ELECTROLYZER_CAPEX_PER_KW
    solar_capex = config['SOLAR_CAPACITY_KW'] * SOLAR_CAPEX_PER_KW
    wind_capex = config['WIND_CAPACITY_KW'] * WIND_CAPEX_PER_KW
    hb_capex = config['ELECTROLYZER_CAPACITY_KW'] * HB_CAPEX_PER_KW_ELECTROLYZER
    storage_capex = target_ammonia_tonne * 0.1 * STORAGE_CAPEX_PER_TONNE # Assume storage for 10% of annual production
    
    # Calculate present value of electrolyzer replacement (assuming a 10-year lifetime)
    replacement_cost = electrolyzer_capex * ((1 + INFLATION_RATE) ** 10)
    replacement_pv = replacement_cost / ((1 + config['DISCOUNT_RATE']) ** 10)
    
    total_capex = electrolyzer_capex + solar_capex + wind_capex + hb_capex + storage_capex + replacement_pv
    
    return {
        "electrolyzer_capex": electrolyzer_capex,
        "solar_capex": solar_capex,
        "wind_capex": wind_capex,
        "haber_bosch_capex": hb_capex,
        "storage_capex": storage_capex,
        "electrolyzer_replacement_pv": replacement_pv,
        "total_capex": total_capex
    }

def calculate_annual_operating_costs(config, capex_costs, total_kwh_needed):
    """Calculates the total annual operating expenditures (OPEX)."""
    electrolyzer_opex = capex_costs['electrolyzer_capex'] * ELECTROLYZER_OPEX_RATE
    re_opex = (capex_costs['solar_capex'] + capex_costs['wind_capex']) * RE_OPEX_RATE
    hb_opex = capex_costs['haber_bosch_capex'] * HB_OPEX_RATE
    storage_opex = capex_costs['storage_capex'] * STORAGE_OPEX_RATE
    
    fixed_opex = electrolyzer_opex + re_opex + hb_opex + storage_opex
    
    # Assume 90% of power is from dedicated renewables, 10% is purchased from the grid
    grid_power_kwh = total_kwh_needed * 0.10
    grid_cost = grid_power_kwh * config['GRID_PRICE']
    
    total_opex = fixed_opex + grid_cost
    
    return {
        "fixed_opex": fixed_opex,
        "grid_purchase_cost": grid_cost,
        "total_annual_opex": total_opex
    }

def calculate_lcoa(config, total_capex, total_annual_opex, target_ammonia_tonne):
    """Calculates the Levelized Cost of Ammonia (LCOA)."""
    if target_ammonia_tonne == 0:
        return {"lcoa_final": 0, "breakdown": {}}

    # Capital Recovery Factor (CRF)
    crf_denominator = ((1 + config['DISCOUNT_RATE']) ** config['PLANT_LIFETIME']) - 1
    if crf_denominator == 0:
        return {"lcoa_final": 0, "breakdown": {}}
        
    crf = (config['DISCOUNT_RATE'] * (1 + config['DISCOUNT_RATE']) ** config['PLANT_LIFETIME']) / crf_denominator
          
    annualized_capex = total_capex * crf
    total_annual_cost = annualized_capex + total_annual_opex
    lcoa_final = total_annual_cost / target_ammonia_tonne
    
    breakdown = {
        "Annualized CAPEX": annualized_capex / target_ammonia_tonne,
        "Annual OPEX": total_annual_opex / target_ammonia_tonne
    }
    
    return {"lcoa_final": lcoa_final, "breakdown": breakdown}
