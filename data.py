# MATERIAL DATABASE AND EMISSION COEFFICIENTS
MATERIAL_DB = {
    'metals': {
        'name': 'Metals (Al, Steel, Cu)',
        'carbon_virgin': 8.2,      # kg CO2e / kg
        'carbon_recycled': 1.4,    # kg CO2e / kg
        'default_recycled': 40,
        'default_recyclability': 85
    },
    'plastics': {
        'name': 'Plastics (ABS, PC, PET)',
        'carbon_virgin': 3.2,
        'carbon_recycled': 0.9,
        'default_recycled': 25,
        'default_recyclability': 75
    },
    'ceramics': {
        'name': 'Ceramics & Glass',
        'carbon_virgin': 1.3,
        'carbon_recycled': 0.4,
        'default_recycled': 15,
        'default_recyclability': 90
    },
    'electronics': {
        'name': 'Electronics (PCBs, Chips)',
        'carbon_virgin': 26.5,
        'carbon_recycled': 5.5,
        'default_recycled': 5,
        'default_recyclability': 50
    },
    'bio': {
        'name': 'Bio-based / Organic (Bamboo, Wood)',
        'carbon_virgin': 0.6,
        'carbon_recycled': 0.1,
        'default_recycled': 80,
        'default_recyclability': 95
    }
}

LOGISTICS_FACTORS = {
    'sea': 0.000012,   # Maritime Cargo (kg CO2e / kg / km)
    'rail': 0.000028,  # Rail Freight
    'road': 0.000115,  # Road Transport (Trucks)
    'air': 0.000810    # Air Freight
}

LOGISTICS_NAMES = {
    'sea': 'Maritime Cargo (Lowest Carbon)',
    'rail': 'Rail Freight',
    'road': 'Road transport (Trucks)',
    'air': 'Air Freight (Highest Carbon)'
}

# PRODUCT PRESETS DATA
PRODUCT_PRESETS = {
    'smartphone': {
        'name': 'Eco Smartphone',
        'lifespan': 3.5,
        'industry_lifespan': 3.0,
        'transport_mode': 'air',
        'logistics_distance': 8500.0,
        'components': [
            {'id': '1', 'name': 'Aluminum Outer Frame', 'material': 'metals', 'weight': 0.16, 'recycled_input': 45, 'recyclability': 85},
            {'id': '2', 'name': 'Aluminosilicate Cover Glass', 'material': 'ceramics', 'weight': 0.04, 'recycled_input': 20, 'recyclability': 60},
            {'id': '3', 'name': 'Main Logic Board & Sensors', 'material': 'electronics', 'weight': 0.05, 'recycled_input': 5, 'recyclability': 45},
            {'id': '4', 'name': 'Lithium-Cobalt Battery pack', 'material': 'electronics', 'weight': 0.07, 'recycled_input': 10, 'recyclability': 60},
            {'id': '5', 'name': 'Internal Bracket (Polycarbonate)', 'material': 'plastics', 'weight': 0.03, 'recycled_input': 30, 'recyclability': 70}
        ]
    },
    'runningshoe': {
        'name': 'Sustainable Running Shoes',
        'lifespan': 1.2,
        'industry_lifespan': 1.0,
        'transport_mode': 'sea',
        'logistics_distance': 12000.0,
        'components': [
            {'id': '1', 'name': 'Recycled Polyester Knit Upper', 'material': 'plastics', 'weight': 0.12, 'recycled_input': 85, 'recyclability': 80},
            {'id': '2', 'name': 'Sugarcane Bio-EVA Midsole', 'material': 'bio', 'weight': 0.24, 'recycled_input': 60, 'recyclability': 50},
            {'id': '3', 'name': 'Natural Rubber Outsole', 'material': 'bio', 'weight': 0.10, 'recycled_input': 40, 'recyclability': 60},
            {'id': '4', 'name': 'Cotton Laces & Collar Lining', 'material': 'bio', 'weight': 0.03, 'recycled_input': 90, 'recyclability': 95}
        ]
    },
    'coffeemug': {
        'name': 'Smart Heat-retaining Coffee Mug',
        'lifespan': 5.0,
        'industry_lifespan': 4.0,
        'transport_mode': 'road',
        'logistics_distance': 1200.0,
        'components': [
            {'id': '1', 'name': 'Double-walled Ceramic Body', 'material': 'ceramics', 'weight': 0.38, 'recycled_input': 15, 'recyclability': 90},
            {'id': '2', 'name': 'Stainless Steel Inner Liner', 'material': 'metals', 'weight': 0.15, 'recycled_input': 75, 'recyclability': 95},
            {'id': '3', 'name': 'Recycled Silicone Base Grip', 'material': 'plastics', 'weight': 0.06, 'recycled_input': 50, 'recyclability': 85},
            {'id': '4', 'name': 'Heating Element & Battery PCB', 'material': 'electronics', 'weight': 0.08, 'recycled_input': 10, 'recyclability': 40}
        ]
    },
    'custom': {
        'name': 'Custom Product',
        'lifespan': 2.0,
        'industry_lifespan': 2.0,
        'transport_mode': 'road',
        'logistics_distance': 800.0,
        'components': []
    }
}
