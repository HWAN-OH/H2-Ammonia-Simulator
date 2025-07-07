 calculator.py
import numpy as np

def calculate_annual_production(config):
    """Calculates the annual production of hydrogen and ammonia."""
    # Prevent division by zero
    if config.get('H2_LHV', 0) == 0 or config.get('ELECTROLYZER_EFFICIENCY', 0) == 0:
        return 0, 0
    
    h2_production_per_hour = (config['PLANT_CAPACITY_KW'] * config['CAPACITY_FACTOR']) / (config['H2_LHV'] / config['ELECTROLYZER_EFFICIENCY'])
    annual_h2_production_kg = h2_production_per_hour * 24 * 365
    annual_nh3_production_kg = annual_h2_production_kg * 5.617
    annual_nh3_production_tonne = annual_nh3_production_kg / 1000
    
    return annual_h2_production_kg, annual_nh3_production_tonne

def calculate_capital_costs(config, annual_nh3_production_tonne):
    """Calculates the total CAPEX."""
    electrolyzer_capex = config['PLANT_CAPACITY_KW'] * config['ELECTROLYZER_CAPEX']
    asu_capex = config['PLANT_CAPACITY_KW'] * config['ASU_CAPEX']
    hb_capex = config['PLANT_CAPACITY_KW'] * config['HB_CAPEX']
    storage_capex = (annual_nh3_production_tonne / 365) * 15 * config['STORAGE_CAPEX']
    
    total_capex = electrolyzer_capex + asu_capex + hb_capex + storage_capex
    
    # Prevent division by zero
    if (1 + config['DISCOUNT_RATE']) == 0:
        replacement_present_value = 0
    else:
        replacement_cost = electrolyzer_capex * ((1 + config['INFLATION_RATE']) ** config['ELECTROLYZER_LIFETIME'])
        replacement_present_value = replacement_cost / ((1 + config['DISCOUNT_RATE']) ** config['ELECTROLYZER_LIFETIME'])

    total_capex_with_replacement = total_capex + replacement_present_value
    
    return {
        "electrolyzer_capex": electrolyzer_capex,
        "asu_capex": asu_capex,
        "hb_capex": hb_capex,
        "storage_capex": storage_capex,
        "total_capex_with_replacement": total_capex_with_replacement
    }

def calculate_annual_operating_costs(config, capex_costs):
    """Calculates the annual OPEX."""
    electrolyzer_opex = capex_costs["electrolyzer_capex"] * config['ELECTROLYZER_OPEX_RATE']
    asu_opex = capex_costs["asu_capex"] * config['ASU_OPEX_RATE']
    hb_opex = capex_costs["hb_capex"] * config['HB_OPEX_RATE']
    storage_opex = capex_costs["storage_capex"] * config['STORAGE_OPEX_RATE']
    
    fixed_opex = electrolyzer_opex + asu_opex + hb_opex + storage_opex
    
    annual_power_consumption = (config['PLANT_CAPACITY_KW'] * config['CAPACITY_FACTOR']) * 24 * 365
    power_cost = annual_power_consumption * config['ELECTRICITY_COST']

    total_opex = fixed_opex + power_cost
    
    return {
        "fixed_opex": fixed_opex,
        "power_cost": power_cost,
        "total_annual_opex": total_opex
    }

def calculate_lcoa(config, total_capex, total_annual_opex, annual_nh3_production_tonne):
    """Calculates the Levelized Cost of Ammonia (LCOA)."""
    # Prevent division by zero
    denominator = ((1 + config['DISCOUNT_RATE']) ** config['PLANT_LIFETIME'] - 1)
    if denominator == 0:
        crf = 0
    else:
        crf = (config['DISCOUNT_RATE'] * (1 + config['DISCOUNT_RATE']) ** config['PLANT_LIFETIME']) / denominator
          
    annualized_capex = total_capex * crf
    total_annual_cost = annualized_capex + total_annual_opex
    
    if annual_nh3_production_tonne == 0:
        lcoa_production = 0
    else:
        lcoa_production = total_annual_cost / annual_nh3_production_tonne
    
    transport_cost_per_tonne = config['TRANSPORT_DISTANCE_KM'] * config['TRANSPORT_COST_PER_TON_KM']
    lcoa_final = lcoa_production + transport_cost_per_tonne
    
    return {
        "lcoa_production": lcoa_production,
        "transport_cost_per_tonne": transport_cost_per_tonne,
        "lcoa_final": lcoa_final,
        "total_annual_cost": total_annual_cost,
        "annualized_capex": annualized_capex
    }
