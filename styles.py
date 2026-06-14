# Dark Glassmorphism Styling System and Custom SVG Icons

GLASS_THEME_CSS = """
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
"""

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
