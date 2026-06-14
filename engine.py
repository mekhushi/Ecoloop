from data import MATERIAL_DB, LOGISTICS_FACTORS

def calculate_circularity_metrics(components, lifespan, industry_lifespan, transport_mode, logistics_distance):
    """
    Computes Ellen MacArthur Foundation (EMF) Material Circularity Index (MCI), 
    Linear Flow Index (LFI), supply chain carbon offsets, and mass distribution paths.
    """
    if not components:
        return {
            'mci': 0.0, 'lfi': 1.0, 'carbon_saved': 0.0, 'feedstock_ratio': 0.0,
            'total_weight': 0.0, 'recycled_mass': 0.0, 'logistics_carbon': 0.0,
            'destiny': {'recycled': 0.0, 'recovered': 0.0, 'waste': 0.0},
            'materials': {'metals': 0.0, 'plastics': 0.0, 'ceramics': 0.0, 'electronics': 0.0, 'bio': 0.0}
        }
        
    total_weight = 0.0
    total_virgin_mass = 0.0
    total_waste_mass = 0.0
    total_recycled_mass = 0.0
    total_recovered_mass = 0.0
    
    carbon_virgin_total = 0.0
    carbon_actual_total = 0.0
    
    efficiency_recycle_in = 0.90
    efficiency_recycle_out = 0.90
    
    materials_weight = {'metals': 0.0, 'plastics': 0.0, 'ceramics': 0.0, 'electronics': 0.0, 'bio': 0.0}
    
    for c in components:
        mass = float(c['weight'])
        total_weight += mass
        materials_weight[c['material']] += mass
        
        rin = float(c['recycled_input']) / 100.0
        rout = float(c['recyclability']) / 100.0
        
        # Virgin mass V
        v = mass * (1.0 - rin)
        total_virgin_mass += v
        total_recycled_mass += (mass * rin)
        
        # Waste generated in input recycling (W0)
        w0 = mass * (1.0 - efficiency_recycle_in) * (rin / efficiency_recycle_in)
        
        # Waste generated in EoL recycling (Wc)
        wc = mass * (1.0 - efficiency_recycle_out) * rout
        
        # Linear landfilled waste (Wf)
        wf = mass * (1.0 - rout)
        total_recovered_mass += (mass * rout)
        
        # Total waste associated with component W
        w = w0 + wc + wf
        total_waste_mass += w
        
        # Carbon Calculation
        mat_props = MATERIAL_DB[c['material']]
        c_v = mass * mat_props['carbon_virgin']
        c_act = (mass * (1.0 - rin) * mat_props['carbon_virgin']) + (mass * rin * mat_props['carbon_recycled'])
        
        carbon_virgin_total += c_v
        carbon_actual_total += c_act
        
    # Linear Flow Index (LFI)
    lfi = (total_virgin_mass + total_waste_mass) / (2.0 * total_weight)
    lfi = max(0.0, min(1.0, lfi))
    
    # Utility Factor F(U)
    utility_ratio = lifespan / industry_lifespan if industry_lifespan > 0 else 1.0
    utility_factor = 0.9 / utility_ratio if utility_ratio > 0 else 1.0
    utility_factor = min(1.0, utility_factor)
    
    # Material Circularity Index (MCI)
    mci = 1.0 - (lfi * utility_factor)
    mci = max(0.0, min(1.0, mci))
    
    # Carbon offset
    carbon_saved = max(0.0, carbon_virgin_total - carbon_actual_total)
    
    # Feedstock circular ratio
    feedstock_ratio = (total_recycled_mass / total_weight) * 100.0 if total_weight > 0 else 0.0
    
    # Logistics carbon
    log_factor = LOGISTICS_FACTORS[transport_mode]
    logistics_carbon = total_weight * logistics_distance * log_factor
    
    # Mass Destiny
    recycle_dest = total_recycled_mass
    recover_dest = total_recovered_mass
    waste_dest = max(0.0, total_weight - (recover_dest * efficiency_recycle_out))
    
    return {
        'mci': mci,
        'lfi': lfi,
        'carbon_saved': carbon_saved,
        'feedstock_ratio': feedstock_ratio,
        'total_weight': total_weight,
        'recycled_mass': total_recycled_mass,
        'logistics_carbon': logistics_carbon,
        'destiny': {
            'recycled': recycle_dest,
            'recovered': recover_dest,
            'waste': waste_dest
        },
        'materials': materials_weight
    }
