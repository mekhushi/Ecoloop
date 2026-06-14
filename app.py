import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

# 1. PAGE SETUP & CONFIGURATION
st.set_page_config(
    page_title="Ecoloop // Circular Design Engine",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling to create a premium Dark Glassmorphism interface
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');
    
    /* Main Background and Text */
    .stApp {
        background-color: #060913;
        background-image: radial-gradient(at 0% 0%, rgba(16, 185, 129, 0.04) 0px, transparent 50%),
                           radial-gradient(at 100% 0%, rgba(6, 182, 212, 0.04) 0px, transparent 50%),
                           radial-gradient(at 50% 100%, rgba(139, 92, 246, 0.04) 0px, transparent 50%);
        color: #f1f5f9;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    /* Hide Streamlit default menu/footer */
    header { visibility: hidden; }
    footer { visibility: hidden; }
    div[data-testid="stHeader"] { background: transparent !important; }
    
    /* Custom Typography overrides */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: -0.5px !important;
    }
    
    /* Title Tagline Styling */
    .app-title-container {
        margin-bottom: 28px;
        padding-bottom: 18px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    .app-title-main {
        font-size: 30px;
        font-weight: 800;
        letter-spacing: 2px;
        background: linear-gradient(135deg, #10b981, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .app-tagline {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #64748b;
        font-weight: 600;
        display: block;
        margin-top: 4px;
    }
    
    /* Glassmorphic KPI Cards */
    .kpi-card {
        background: rgba(11, 17, 32, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.25) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        border-color: rgba(6, 182, 212, 0.15) !important;
        box-shadow: 0 8px 30px rgba(6, 182, 212, 0.06) !important;
    }
    .kpi-label {
        font-size: 11px;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .kpi-value {
        font-family: 'Outfit', sans-serif;
        font-size: 24px;
        font-weight: 800;
        color: #ffffff;
        margin-top: 2px;
    }
    .kpi-meta {
        font-size: 11px;
        color: #475569;
        margin-top: 2px;
        font-weight: 500;
    }
    
    /* Color classes */
    .mci-color { color: #10b981 !important; }
    .lfi-color { color: #8b5cf6 !important; }
    .carbon-color { color: #06b6d4 !important; }
    
    /* Premium Recommendation Card styling */
    .rec-box {
        background: rgba(11, 17, 32, 0.45) !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
        border-left: 3px solid #06b6d4 !important;
        border-radius: 8px !important;
        padding: 14px 18px !important;
        margin-bottom: 12px !important;
        transition: all 0.2s ease;
    }
    .rec-box:hover {
        background: rgba(11, 17, 32, 0.6) !important;
        border-color: rgba(6, 182, 212, 0.12) !important;
    }
    .rec-title {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #06b6d4;
    }
    .rec-impact {
        font-weight: 700;
        color: #10b981;
        font-size: 11px;
        margin-top: 6px;
        display: block;
    }
    
    /* Sidebar aesthetic */
    .stSidebar {
        background-color: #04060d !important;
        border-right: 1px solid rgba(255, 255, 255, 0.03) !important;
    }
    
    /* Form fields and selectors styling */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>div, .stSelectbox>div>div>button {
        background-color: rgba(11, 17, 32, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
        color: #e2e8f0 !important;
        font-size: 13px !important;
        padding: 4px 12px !important;
    }
    .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
        border-color: #10b981 !important;
        box-shadow: 0 0 0 1px rgba(16, 185, 129, 0.15) !important;
    }
    
    /* Sidebar text colors */
    .stSidebar p, .stSidebar label {
        color: #94a3b8 !important;
        font-size: 12px !important;
        font-weight: 500 !important;
    }
    
    /* Standard buttons styling */
    .stButton>button {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        color: #94a3b8 !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }
    .stButton>button:hover {
        background: rgba(255, 255, 255, 0.06) !important;
        border-color: rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
    }
    
    /* Optimization primary button override */
    div[data-testid="stHorizontalBlock"] div.row-widget.stButton > button {
        background: linear-gradient(135deg, #10b981, #059669) !important;
        color: #ffffff !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.15) !important;
    }
    div[data-testid="stHorizontalBlock"] div.row-widget.stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.25) !important;
    }
    
    /* Streamlit interactive block spacing */
    div[data-testid="stBlock"] {
        padding: 0px !important;
    }
    
    /* Subheader bottom border styling */
    h3 {
        padding-bottom: 8px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04) !important;
        margin-bottom: 16px !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. MATERIAL LOGISTICS AND EMISSION DATA COEFICIENTS
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
    'sea': 0.000012,   # Maritime Cargo
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

# 3. INITIALIZE STATE IN SESSION STATE
if 'product_name' not in st.session_state:
    st.session_state.product_name = PRODUCT_PRESETS['smartphone']['name']
    st.session_state.lifespan = PRODUCT_PRESETS['smartphone']['lifespan']
    st.session_state.industry_lifespan = PRODUCT_PRESETS['smartphone']['industry_lifespan']
    st.session_state.transport_mode = PRODUCT_PRESETS['smartphone']['transport_mode']
    st.session_state.logistics_distance = PRODUCT_PRESETS['smartphone']['logistics_distance']
    st.session_state.components = [dict(c) for c in PRODUCT_PRESETS['smartphone']['components']]
    st.session_state.active_preset = 'smartphone'
    for c in st.session_state.components:
        st.session_state[f"rin_{c['id']}"] = c['recycled_input']
        st.session_state[f"rout_{c['id']}"] = c['recyclability']

# Function to load a preset
def load_preset(preset_key):
    preset = PRODUCT_PRESETS[preset_key]
    st.session_state.product_name = preset['name']
    st.session_state.lifespan = preset['lifespan']
    st.session_state.industry_lifespan = preset['industry_lifespan']
    st.session_state.transport_mode = preset['transport_mode']
    st.session_state.logistics_distance = preset['logistics_distance']
    st.session_state.components = [dict(c) for c in preset['components']]
    st.session_state.active_preset = preset_key
    # Sync the widget slider values in session state
    for c in st.session_state.components:
        st.session_state[f"rin_{c['id']}"] = c['recycled_input']
        st.session_state[f"rout_{c['id']}"] = c['recyclability']

# Callback function for optimization button
def run_optimization():
    if not st.session_state.components:
        st.session_state.opt_error = "Add some components to your Bill of Materials first before running optimization!"
    else:
        # Shift everything to optimal rates
        for c in st.session_state.components:
            c['recycled_input'] = 90
            c['recyclability'] = 95
            st.session_state[f"rin_{c['id']}"] = 90
            st.session_state[f"rout_{c['id']}"] = 95
        
        # Green transport
        st.session_state.transport_mode = 'sea'
        
        # Extend lifespan to close structural utility gap
        st.session_state.lifespan = st.session_state.industry_lifespan * 1.5
        
        st.session_state.active_preset = 'custom'
        st.session_state.success_message = "Circularity optimizations applied: Sourcing shifted to 90% recycled inputs, 95% EoL recyclability, sea transport, and product longevity extended by 50% relative to industry benchmarks."

# 4. CORE MATHEMATICAL COMPUTATIONS (MCI MODEL)
def calculate_circularity_metrics():
    components = st.session_state.components
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
    utility_ratio = st.session_state.lifespan / st.session_state.industry_lifespan if st.session_state.industry_lifespan > 0 else 1.0
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
    log_factor = LOGISTICS_FACTORS[st.session_state.transport_mode]
    logistics_carbon = total_weight * st.session_state.logistics_distance * log_factor
    
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

# Compute metrics
metrics = calculate_circularity_metrics()

# Function to render a visual circular progress SVG gauge for the MCI score
def draw_mci_gauge(score):
    percent = int(score * 100)
    circumference = 251.2
    offset = circumference - (score * circumference)
    
    if score >= 0.8:
        rating = "Highly Circular"
        color = "#10b981" # Emerald Green
    elif score >= 0.4:
        rating = "Transitioning"
        color = "#34d399" # Soft Mint Green
    else:
        rating = "Linear Design"
        color = "#ffffff" # Pure White
        
    gauge_html = f"""
    <div style="background: rgba(15, 23, 42, 0.55); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 12px; padding: 18px 24px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3); display: flex; align-items: center; justify-content: space-between; height: 110px;">
        <div style="display: flex; flex-direction: column; justify-content: center; height: 100%;">
            <span style="font-size: 11px; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 2px;">Circularity Index (MCI)</span>
            <span style="font-family: 'Outfit', sans-serif; font-size: 11px; font-weight: 700; color: {color}; text-transform: uppercase; letter-spacing: 0.5px;">{rating}</span>
        </div>
        <div style="position: relative; width: 70px; height: 70px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-left: 10px;">
            <svg style="transform: rotate(-90deg); width: 100%; height: 100%;" viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="40" stroke="rgba(255,255,255,0.04)" stroke-width="8" fill="none" />
                <circle cx="50" cy="50" r="40" stroke="{color}" stroke-dasharray="251.2" stroke-dashoffset="{offset}" stroke-width="8" stroke-linecap="round" fill="none" style="transition: stroke-dashoffset 0.6s ease; filter: drop-shadow(0 0 4px {color});" />
            </svg>
            <div style="position: absolute; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                <span style="font-family: 'Outfit', sans-serif; font-size: 18px; font-weight: 800; color: #ffffff;">{score:.2f}</span>
            </div>
        </div>
    </div>
    """
    return gauge_html

# 5. HEADER COMPONENT
st.markdown("""
<div class="app-title-container">
    <div style="flex-grow: 1;">
        <h1 class="app-title-main">ECOLOOP</h1>
        <span class="app-tagline">Circular Design & Material Lifecycle Engine (Python Portfolio Version)</span>
    </div>
</div>
""", unsafe_allow_html=True)

# 6. SIDEBAR - PRODUCT SETTINGS & BUILDER
with st.sidebar:
    st.markdown("### Configuration Panel")
    
    # Preset Selection
    preset_options = ['smartphone', 'runningshoe', 'coffeemug', 'custom']
    preset_choice = st.selectbox(
        "Load Product Preset",
        options=preset_options,
        index=preset_options.index(st.session_state.active_preset),
        format_func=lambda x: PRODUCT_PRESETS[x]['name']
    )
    
    if preset_choice != st.session_state.active_preset:
        load_preset(preset_choice)
        st.rerun()
        
    st.markdown("---")
    st.markdown("### Product Settings")
    
    st.session_state.product_name = st.text_input("Product Model Name", value=st.session_state.product_name)
    
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        st.session_state.lifespan = st.number_input("Lifespan (yrs)", value=st.session_state.lifespan, min_value=0.1, step=0.1)
    with col_l2:
        st.session_state.industry_lifespan = st.number_input("Industry Avg (yrs)", value=st.session_state.industry_lifespan, min_value=0.1, step=0.1)
        
    transport_options = list(LOGISTICS_FACTORS.keys())
    st.session_state.transport_mode = st.selectbox(
        "Logistics Mode",
        options=transport_options,
        index=transport_options.index(st.session_state.transport_mode),
        format_func=lambda x: LOGISTICS_NAMES[x]
    )
    st.session_state.logistics_distance = st.number_input("Logistics Distance (km)", value=st.session_state.logistics_distance, min_value=0.0, step=50.0)

    st.markdown("---")
    st.markdown("### Add Component")
    with st.form("add_component_form", clear_on_submit=True):
        c_name = st.text_input("Component Name", placeholder="e.g. Aluminum Casing")
        c_mat = st.selectbox("Material Category", options=list(MATERIAL_DB.keys()), format_func=lambda x: MATERIAL_DB[x]['name'])
        c_weight = st.number_input("Weight (kg)", min_value=0.001, max_value=500.0, value=0.5, step=0.01)
        
        submitted = st.form_submit_button("Add to BOM")
        if submitted and c_name:
            def_props = MATERIAL_DB[c_mat]
            new_comp = {
                'id': str(int(time.time() * 1000)),
                'name': c_name,
                'material': c_mat,
                'weight': c_weight,
                'recycled_input': def_props['default_recycled'],
                'recyclability': def_props['default_recyclability']
            }
            st.session_state.components.append(new_comp)
            st.session_state.active_preset = 'custom'
            # Initialize slider keys in session state for the new component
            st.session_state[f"rin_{new_comp['id']}"] = new_comp['recycled_input']
            st.session_state[f"rout_{new_comp['id']}"] = new_comp['recyclability']
            st.rerun()

# 7. MAIN INTERFACE LAYOUT
# Row 1: KPI Statistics Card Widgets
kpi_mci, kpi_lfi, kpi_carbon, kpi_feedstock = st.columns(4)

with kpi_mci:
    st.markdown(draw_mci_gauge(metrics['mci']), unsafe_allow_html=True)

with kpi_lfi:
    st.markdown(f"""
    <div class="kpi-card" style="display: flex; align-items: center; justify-content: space-between; height: 110px;">
        <div style="display: flex; flex-direction: column; justify-content: center;">
            <span class="kpi-label">Linear Flow Index</span>
            <div class="kpi-value lfi-color">{metrics['lfi']:.2f}</div>
            <span class="kpi-meta">{metrics['lfi']*100:.0f}% non-circular flow</span>
        </div>
        <div style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); width: 42px; height: 42px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #ffffff; flex-shrink: 0; margin-left: 10px;">
            <svg style="width:20px; height:20px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi_carbon:
    st.markdown(f"""
    <div class="kpi-card" style="display: flex; align-items: center; justify-content: space-between; height: 110px;">
        <div style="display: flex; flex-direction: column; justify-content: center;">
            <span class="kpi-label">CO₂e Sourcing Offset</span>
            <div class="kpi-value carbon-color">{metrics['carbon_saved']:.1f} kg</div>
            <span class="kpi-meta">Saved vs 100% virgin</span>
        </div>
        <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.2); width: 42px; height: 42px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #10b981; flex-shrink: 0; margin-left: 10px;">
            <svg style="width:20px; height:20px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
        </div>
    </div>
    """, unsafe_allow_html=True)

with kpi_feedstock:
    st.markdown(f"""
    <div class="kpi-card" style="display: flex; align-items: center; justify-content: space-between; height: 110px;">
        <div style="display: flex; flex-direction: column; justify-content: center;">
            <span class="kpi-label">Recycled Feedstock Ratio</span>
            <div class="kpi-value" style="color: #10b981;">{metrics['feedstock_ratio']:.1f}%</div>
            <span class="kpi-meta">{metrics['recycled_mass']:.2f} kg circular input</span>
        </div>
        <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.2); width: 42px; height: 42px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #10b981; flex-shrink: 0; margin-left: 10px;">
            <svg style="width:20px; height:20px;" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Row 2: Two-column layout (Bill of Materials editor on Left, Charts on Right)
main_left, main_right = st.columns([1.3, 1.0])

with main_left:
    st.subheader("Bill of Materials & Material Sourcing")
    
    if not st.session_state.components:
        st.info("Your Bill of Materials is currently empty. Use the sidebar settings to load a preset or add custom components to start circular design analyses.")
    else:
        # Display table summary
        st.markdown(f"**Total BOM Weight:** {metrics['total_weight']:.2f} kg  |  **Logistics Transit Carbon:** {metrics['logistics_carbon']:.2f} kg CO₂e")
        
        # Build individual cards for interactive adjustment of feedstock and recyclability
        MAT_COLORS = {
            'metals': '#10b981',      # Emerald Green
            'plastics': '#6ee7b7',    # Mint Green
            'ceramics': '#a7f3d0',    # Soft Sage Green
            'electronics': '#ffffff',  # Pure White
            'bio': '#047857'          # Deep Forest Green
        }
        
        for idx, comp in enumerate(st.session_state.components):
            mat_name = MATERIAL_DB[comp['material']]['name']
            border_color = MAT_COLORS[comp['material']]
            
            with st.container():
                st.markdown(f"""
                <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.04); border-left: 4px solid {border_color}; border-radius: 8px; padding: 12px 16px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <div>
                            <strong style="color: #ffffff; font-size: 14px;">{comp['name']}</strong>
                            <span style="font-size: 10px; text-transform: uppercase; background: rgba(255,255,255,0.08); padding: 2px 6px; border-radius: 4px; color: #94a3b8; margin-left: 8px;">{mat_name}</span>
                        </div>
                        <span style="font-size: 12px; color: #94a3b8; font-weight: 500;">Weight: {comp['weight']:.2f} kg</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Dynamic slider adjustments inside st.columns
                col_slider1, col_slider2, col_delete = st.columns([2, 2, 0.5])
                
                with col_slider1:
                    new_rin = st.slider(
                        f"Recycled Feedstock %",
                        min_value=0, max_value=100,
                        key=f"rin_{comp['id']}",
                        label_visibility="collapsed"
                    )
                    st.markdown(f"<span style='font-size:11px; color:#94a3b8;'>Recycled Input: <strong>{new_rin}%</strong></span>", unsafe_allow_html=True)
                    if new_rin != comp['recycled_input']:
                        comp['recycled_input'] = new_rin
                        st.session_state.active_preset = 'custom'
                        st.rerun()
                        
                with col_slider2:
                    new_rout = st.slider(
                        f"EoL Recyclability %",
                        min_value=0, max_value=100,
                        key=f"rout_{comp['id']}",
                        label_visibility="collapsed"
                    )
                    st.markdown(f"<span style='font-size:11px; color:#94a3b8;'>EoL Recyclability: <strong>{new_rout}%</strong></span>", unsafe_allow_html=True)
                    if new_rout != comp['recyclability']:
                        comp['recyclability'] = new_rout
                        st.session_state.active_preset = 'custom'
                        st.rerun()
                        
                with col_delete:
                    # Clear delete button
                    if st.button("✕", key=f"del_{comp['id']}"):
                        st.session_state.components.remove(comp)
                        st.session_state.active_preset = 'custom'
                        st.rerun()
                st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)

with main_right:
    st.subheader("Material Analytics & Mass Flow")
    
    if st.session_state.components:
        # A. Plotly Material Composition Doughnut Chart
        m_weights = metrics['materials']
        df_comp = pd.DataFrame({
            'Material Class': [MATERIAL_DB[k]['name'] for k in m_weights.keys() if m_weights[k] > 0],
            'Weight (kg)': [v for v in m_weights.values() if v > 0]
        })
        
        fig_pie = px.pie(
            df_comp, 
            names='Material Class', 
            values='Weight (kg)',
            hole=0.6,
            color_discrete_sequence=['#047857', '#10b981', '#34d399', '#a7f3d0', '#ffffff']
        )
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94a3b8', family='Inter', size=10),
            margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.markdown("<p style='font-size:12px; font-weight:600; color:#94a3b8; margin-bottom: 2px;'>MATERIAL COMPOSITION RATIO</p>", unsafe_allow_html=True)
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # B. Plotly Material Destiny Stacked Horizontal Bar
        dest = metrics['destiny']
        w_tot = metrics['total_weight']
        
        # Feedstock Input Row
        df_destiny = pd.DataFrame([
            {'Flow': 'Feedstock Input', 'Category': 'Recycled Content', 'Mass (kg)': dest['recycled']},
            {'Flow': 'Feedstock Input', 'Category': 'Virgin Feedstock', 'Mass (kg)': w_tot - dest['recycled']},
            {'Flow': 'Disposal Output', 'Category': 'Recovered / Recycled', 'Mass (kg)': dest['recovered']},
            {'Flow': 'Disposal Output', 'Category': 'Unrecoverable Waste', 'Mass (kg)': dest['waste']}
        ])
        
        fig_bar = px.bar(
            df_destiny,
            x='Mass (kg)',
            y='Flow',
            color='Category',
            orientation='h',
            color_discrete_map={
                'Recycled Content': '#10b981',
                'Virgin Feedstock': '#ffffff',
                'Recovered / Recycled': '#34d399',
                'Unrecoverable Waste': '#047857'
            },
            height=200
        )
        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94a3b8', family='Inter', size=10),
            margin=dict(t=20, b=10, l=10, r=10),
            xaxis=dict(gridcolor='rgba(255,255,255,0.03)', title=dict(font=dict(size=10))),
            yaxis=dict(title=None),
            legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5)
        )
        st.markdown("<p style='font-size:12px; font-weight:600; color:#94a3b8; margin-top:20px; margin-bottom: 2px;'>LIFECYCLE MASS DESTINY (INPUT VS OUTPUT)</p>", unsafe_allow_html=True)
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("Please configure your Bill of Materials to generate visualization graphs.")

# Row 3: Design Optimization Recommendations & System Actions
rec_col, action_col = st.columns([1.3, 1.0])

with rec_col:
    st.subheader("Design & Sourcing Optimization Recommendations")
    
    recs = []
    
    # Analyze lifespan
    lifespan = st.session_state.lifespan
    ind_lifespan = st.session_state.industry_lifespan
    if lifespan < ind_lifespan:
        recs.append({
            'text': f"Product expected lifespan ({lifespan} years) is below industry category average ({ind_lifespan} years). Extending product longevity or providing modular modular replacement components reduces linear depletion rates.",
            'impact': "Increases utility factor F(U), boosting overall MCI score."
        })
        
    # Component analysis
    for c in st.session_state.components:
        if c['recycled_input'] < 50:
            mat_props = MATERIAL_DB[c['material']]
            co2_saved = (mat_props['carbon_virgin'] - mat_props['carbon_recycled']) * c['weight']
            recs.append({
                'text': f"Component '{c['name']}' uses primarily virgin materials. Substituting with recycled {c['material']} reduces extractive pressures.",
                'impact': f"Saves ~{co2_saved:.1f} kg CO₂e greenhouse gas emissions."
            })
        if c['recyclability'] < 60:
            recs.append({
                'text': f"Component '{c['name']}' features low EoL recovery potential ({c['recyclability']}%). Implement dry mechanical joins instead of adhesive gluing to allow clean separation.",
                'impact': f"Diverts ~{(c['weight'] * 0.4):.2f} kg from final landfill destinations."
            })
            
    # Logistics transport
    if st.session_state.transport_mode == 'air' and st.session_state.logistics_distance > 1000:
        recs.append({
            'text': "High reliance on Air Freight Logistics. Switching primary shipment channels to Maritime or Rail logistics lowers carbon footprint.",
            'impact': "Cuts supply chain distribution carbon emissions by up to 90%."
        })
        
    if not recs:
        st.success("Closed Loop Achieved: Sourcing feedstock ratios and end-of-life recycling pathways are fully optimized.")
    else:
        for r in recs[:4]: # Limit to top 4 recommendations to avoid clutter
            st.markdown(f"""
            <div class="rec-box">
                <div class="rec-title">Sourcing Optimization</div>
                <div style="font-size:12px; color:#e2e8f0; margin-top:4px;">{r['text']}</div>
                <span class="rec-impact">{r['impact']}</span>
            </div>
            """, unsafe_allow_html=True)

with action_col:
    st.subheader("Optimization Controls")
    
    # Show success message if set in session state
    if 'success_message' in st.session_state and st.session_state.success_message:
        st.success(st.session_state.success_message)
        st.session_state.success_message = None
        
    # Show error message if set in session state
    if 'opt_error' in st.session_state and st.session_state.opt_error:
        st.error(st.session_state.opt_error)
        st.session_state.opt_error = None
        
    # Auto-Optimize Button - Triggered via Callback to prevent StreamlitAPIException
    st.button("Run Design Optimization Simulator", on_click=run_optimization, use_container_width=True)
            
    # Download Audit Report CSV
    if st.session_state.components:
        # Create CSV data
        df_csv = pd.DataFrame(st.session_state.components)
        df_csv['product_name'] = st.session_state.product_name
        df_csv['calculated_mci'] = metrics['mci']
        df_csv['calculated_lfi'] = metrics['lfi']
        df_csv['total_carbon_saved_kg'] = metrics['carbon_saved']
        df_csv['total_logistics_carbon_kg'] = metrics['logistics_carbon']
        
        csv_data = df_csv.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="Export Sourcing Audit Report (CSV)",
            data=csv_data,
            file_name=f"ecoloop_audit_{st.session_state.product_name.lower().replace(' ', '_')}.csv",
            mime='text/csv',
            use_container_width=True
        )
    else:
        st.button("Export Sourcing Audit Report (CSV)", disabled=True, use_container_width=True)
        
    st.markdown("""
    <div style="background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255, 255, 255, 0.04); border-radius: 8px; padding: 12px; margin-top: 16px;">
        <span style="font-size: 11px; color: #64748b; display: block; text-align: center;">
            Ecoloop Engine calculated following circular economy standards outlined by the <strong>Ellen MacArthur Foundation (EMF)</strong>.
        </span>
    </div>
    """, unsafe_allow_html=True)
