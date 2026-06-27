import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time


from data import MATERIAL_DB, LOGISTICS_FACTORS, LOGISTICS_NAMES, PRODUCT_PRESETS
from engine import calculate_circularity_metrics
from styles import GLASS_THEME_CSS, draw_mci_gauge


st.set_page_config(
    page_title="Ecoloop // Circular Design Engine",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(GLASS_THEME_CSS, unsafe_allow_html=True)

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


def load_preset(preset_key):
    preset = PRODUCT_PRESETS[preset_key]
    st.session_state.product_name = preset['name']
    st.session_state.lifespan = preset['lifespan']
    st.session_state.industry_lifespan = preset['industry_lifespan']
    st.session_state.transport_mode = preset['transport_mode']
    st.session_state.logistics_distance = preset['logistics_distance']
    st.session_state.components = [dict(c) for c in preset['components']]
    st.session_state.active_preset = preset_key

    for c in st.session_state.components:
        st.session_state[f"rin_{c['id']}"] = c['recycled_input']
        st.session_state[f"rout_{c['id']}"] = c['recyclability']

def run_optimization():
    if not st.session_state.components:
        st.session_state.opt_error = "Add some components to your Bill of Materials first before running optimization!"
    else:

        for c in st.session_state.components:
            c['recycled_input'] = 90
            c['recyclability'] = 95
            st.session_state[f"rin_{c['id']}"] = 90
            st.session_state[f"rout_{c['id']}"] = 95
        
   
        st.session_state.transport_mode = 'sea'
        
        st.session_state.lifespan = st.session_state.industry_lifespan * 1.5
        
        st.session_state.active_preset = 'custom'
        st.session_state.success_message = "Circularity optimizations applied: Sourcing shifted to 90% recycled inputs, 95% EoL recyclability, sea transport, and product longevity extended by 50% relative to industry benchmarks."


metrics = calculate_circularity_metrics(
    components=st.session_state.components,
    lifespan=st.session_state.lifespan,
    industry_lifespan=st.session_state.industry_lifespan,
    transport_mode=st.session_state.transport_mode,
    logistics_distance=st.session_state.logistics_distance
)

st.markdown("""
<div class="app-title-container">
    <div style="flex-grow: 1;">
        <h1 class="app-title-main">ECOLOOP</h1>
        <span class="app-tagline">Circular Design & Material Lifecycle Engine (Modular Python Version)</span>
    </div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Configuration Panel")
    
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
            st.session_state[f"rin_{new_comp['id']}"] = new_comp['recycled_input']
            st.session_state[f"rout_{new_comp['id']}"] = new_comp['recyclability']
            st.rerun()


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


main_left, main_right = st.columns([1.3, 1.0])

with main_left:
    st.subheader("Bill of Materials & Material Sourcing")
    
    if not st.session_state.components:
        st.info("Your Bill of Materials is currently empty. Use the sidebar settings to load a preset or add custom components to start circular design analyses.")
    else:
        st.markdown(f"**Total BOM Weight:** {metrics['total_weight']:.2f} kg  |  **Logistics Transit Carbon:** {metrics['logistics_carbon']:.2f} kg CO₂e")
        
        MAT_COLORS = {
            'metals': '#10b981',
            'plastics': '#6ee7b7',
            'ceramics': '#a7f3d0',
            'electronics': '#ffffff',
            'bio': '#047857'
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
                    if st.button("✕", key=f"del_{comp['id']}"):
                        st.session_state.components.remove(comp)
                        st.session_state.active_preset = 'custom'
                        st.rerun()
                st.markdown("<div style='margin-bottom: 16px;'></div>", unsafe_allow_html=True)

with main_right:
    st.subheader("Material Analytics & Mass Flow")
    
    if st.session_state.components:
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
        
        dest = metrics['destiny']
        w_tot = metrics['total_weight']
        
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

rec_col, action_col = st.columns([1.3, 1.0])

with rec_col:
    st.subheader("Design & Sourcing Optimization Recommendations")
    
    recs = []
    lifespan = st.session_state.lifespan
    ind_lifespan = st.session_state.industry_lifespan
    if lifespan < ind_lifespan:
        recs.append({
            'text': f"Product expected lifespan ({lifespan} years) is below industry category average ({ind_lifespan} years). Extending product longevity or providing modular modular replacement components reduces linear depletion rates.",
            'impact': "Increases utility factor F(U), boosting overall MCI score."
        })
        
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
            
    if st.session_state.transport_mode == 'air' and st.session_state.logistics_distance > 1000:
        recs.append({
            'text': "High reliance on Air Freight Logistics. Switching primary shipment channels to Maritime or Rail logistics lowers carbon footprint.",
            'impact': "Cuts supply chain distribution carbon emissions by up to 90%."
        })
        
    if not recs:
        st.success("Closed Loop Achieved: Sourcing feedstock ratios and end-of-life recycling pathways are fully optimized.")
    else:
        for r in recs[:4]:
            st.markdown(f"""
            <div class="rec-box">
                <div class="rec-title">Sourcing Optimization</div>
                <div style="font-size:12px; color:#e2e8f0; margin-top:4px;">{r['text']}</div>
                <span class="rec-impact">{r['impact']}</span>
            </div>
            """, unsafe_allow_html=True)

with action_col:
    st.subheader("Optimization Controls")
    
    if 'success_message' in st.session_state and st.session_state.success_message:
        st.success(st.session_state.success_message)
        st.session_state.success_message = None
        
    if 'opt_error' in st.session_state and st.session_state.opt_error:
        st.error(st.session_state.opt_error)
        st.session_state.opt_error = None
        
    st.button("Run Design Optimization Simulator", on_click=run_optimization, use_container_width=True)
            
    if st.session_state.components:
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
