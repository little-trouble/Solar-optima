import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import importlib 

import ui
import lang
import core

importlib.reload(lang)

st.set_page_config(page_title="SOLAR OPTIMA", layout="wide", initial_sidebar_state="collapsed")
ui.init_styles()
l = lang.get_text()

if 'page' not in st.session_state:
    st.session_state.page = 'home'

if 'opt_mode_idx' not in st.session_state: st.session_state.opt_mode_idx = 0
if 'user_data_input' not in st.session_state:
    st.session_state.user_data_input = "6.873046, 101.295367, 230\n6.873286, 101.295853, 400\n6.873453, 101.295484, 840"
if 'forbidden_input' not in st.session_state: st.session_state.forbidden_input = ""
if 'data_mode_idx' not in st.session_state: st.session_state.data_mode_idx = 0
if 'season_idx' not in st.session_state: st.session_state.season_idx = 0
if 'cloud_idx' not in st.session_state: st.session_state.cloud_idx = 0
if 'sigma' not in st.session_state: st.session_state.sigma = 0.05
if 'a_panel_limit' not in st.session_state: st.session_state.a_panel_limit = 180.0
if 'v_source' not in st.session_state: st.session_state.v_source = 220.0
if 'wire_size' not in st.session_state: st.session_state.wire_size = 2.5e-6

nav_col_brand, nav_col_menu, nav_col_lang = st.columns([2.5, 5, 2.5])

with nav_col_brand:
    st.markdown("<h3 style='margin:0; padding-top:5px; color:#1e3a8a; font-weight:700;'>☀ SOLAR OPTIMA</h3>", unsafe_allow_html=True)

with nav_col_menu:
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        if st.button(l['nav_home'], key='nav_home', width="stretch"):
            st.session_state.page = 'home'
            st.rerun()
    with m_col2:
        if st.button(l['nav_config'], key='nav_config', width="stretch"):
            st.session_state.page = 'config'
            st.rerun()
    with m_col3:
        if st.button(l['nav_results'], key='nav_results', width="stretch"):
            if 'results_data' in st.session_state:
                st.session_state.page = 'result'
                st.rerun()
            else:
                st.error("Please analyze configuration first!")

with nav_col_lang:
    current_lang_label = "🌐 English" if st.session_state.lang == 'th' else "🌐 ไทย"
    if st.button(current_lang_label, key='nav_lang_toggle', width="stretch"):
        lang.switch_lang()
        st.rerun()

st.markdown("---")

if st.session_state.page == 'home':
    col_text, col_img = st.columns([1.2, 1])
    with col_text:
        st.markdown(f"<h1 class='main-title'>{l['title']}</h1>", unsafe_allow_html=True)
        st.markdown(f"### {l['subtitle']}")
        st.write("")
        st.write(l['home_desc'])
        st.write("")
        if st.button(l['btn_start'], key='start_app_btn', type="primary"):
            st.session_state.page = 'config'
            st.rerun()

    with col_img:
        if os.path.exists("assets/home_banner.png"):
            # เปลี่ยนจาก use_container_width=True เป็น width="stretch"
            st.image("assets/home_banner.png", width="stretch")
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%); 
            height: 350px; border-radius: 24px; display: flex; 
            align-items: center; justify-content: center; 
            box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 2px dashed #3b82f6;">
            <div style="text-align: center; color: #0369a1;">
            <span style="font-size: 5rem;">☀️</span>
            <div style="font-weight: bold; margin-top: 10px; font-family: 'Sarabun';">[ SOLAR OPTIMA BANNER IMAGE ]</div>
            <div style="font-size: 0.85rem; color: #0284c7; margin-top: 5px;">Place file at assets/home_banner.png to replace placeholder</div>
            </div>
            </div>
            """, unsafe_allow_html=True)

elif st.session_state.page == 'config':
    st.markdown(f"<h2>{l['sidebar_settings']}</h2>", unsafe_allow_html=True)
    col_left, col_right = st.columns(2)

    with col_left: 
        st.markdown(f"#### {l['user_data']}")
        user_data_input = st.text_area(l['user_data'], value=st.session_state.user_data_input, height=150, help="Format: Latitude, Longitude, Weight", label_visibility="collapsed")
        st.session_state.user_data_input = user_data_input
        st.markdown(f"#### {l['forbidden_title']}")
        forbidden_input = st.text_input(l['forbidden_title'], value=st.session_state.forbidden_input, help=l['forbidden_help'], label_visibility="collapsed")
        st.session_state.forbidden_input = forbidden_input

    with col_right:
        st.markdown(f"#### {l['env_settings']}")
        data_modes = ["Manual", "Live NASA API"]
        selected_data_mode = st.radio("Solar Data Mode", data_modes, index=st.session_state.data_mode_idx, label_visibility="collapsed")
        st.session_state.data_mode_idx = data_modes.index(selected_data_mode)
        h_sun_final = 5.0
        if selected_data_mode == "Live NASA API":
            try:
                lines = [line.split(",") for line in user_data_input.split("\n") if line.strip()]
                users_temp = [[float(x) for x in line] for line in lines if len(line) >= 3]
                if users_temp:
                    with st.spinner('Fetching NASA Data...'):
                        h_sun_final = core.get_nasa_solar_data(users_temp[0][0], users_temp[0][1])
                        st.success(f"NASA Solar: {h_sun_final:.2f} kWh/m²/day")
            except:
                h_sun_final = 5.0
                st.warning("Using default solar data (5.0)")
        else:
            season_map = {l['summer']: 1.1, l['rainy']: 0.8, l['winter']: 0.95}
            selected_season = st.selectbox(l['season'], list(season_map.keys()), index=st.session_state.season_idx)
            st.session_state.season_idx = list(season_map.keys()).index(selected_season)
            h_sun_final = season_map[selected_season] * 5.0
            cloud_map = {l['clear']: "clear", l['partial']: "partial", l['cloudy']: "cloudy"}
            selected_cloud = st.selectbox(l['cloud'], list(cloud_map.keys()), index=st.session_state.cloud_idx)
            st.session_state.cloud_idx = list(cloud_map.keys()).index(selected_cloud)

        sigma = st.slider(l['sigma_label'], 0.0, 0.20, value=st.session_state.sigma, step=0.05)
        st.session_state.sigma = sigma
        st.markdown(f"#### {l['eng_settings']}")
        a_panel_limit = st.number_input("Panel Area Limit (m²)", value=st.session_state.a_panel_limit)
        v_source = st.number_input("Voltage Source (V)", value=st.session_state.v_source)
        wire_size = st.number_input("Wire Size (m²)", value=st.session_state.wire_size, format="%.1e")
        st.session_state.a_panel_limit = a_panel_limit
        st.session_state.v_source = v_source
        st.session_state.wire_size = wire_size

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button(l['btn_analyze'], width="stretch"):
        lines = [line.split(",") for line in st.session_state.user_data_input.split("\n") if line.strip()]
        users = [[float(x) for x in line] for line in lines if len(line) >= 3]

        if not users:
            st.error("กรุณากรอกข้อมูลพิกัดผู้ใช้ให้ถูกต้อง")
            st.stop()
        total_I = sum([u[2] for u in users]) 
        total_E_demand = sum([u[2] for u in users]) * 0.05

        forbidden_zones = []
        if st.session_state.forbidden_input.strip():
            for line in st.session_state.forbidden_input.split("\n"):
                if line.strip():
                    parts = line.split(",")
                    if len(parts) >= 4:
                        forbidden_zones.append([float(p) for p in parts[:4]])

        best_loc_eff = core.find_best_location(users, 6.873286, 101.295853, "efficiency", total_I, 1.7e-8, wire_size, 5, v_source, forbidden_zones)
        best_loc_equ = core.find_best_location(users, 6.873286, 101.295853, "equity", total_I, 1.7e-8, wire_size, 5, v_source, forbidden_zones)

        if best_loc_eff and best_loc_equ:
            opt_lat_eff, opt_lon_eff, opt_e_loss_eff, opt_p_loss_eff, opt_dist_eff = best_loc_eff
            opt_lat_equ, opt_lon_equ, opt_e_loss_equ, opt_p_loss_equ, opt_dist_equ = best_loc_equ

            avg_walk_eff = sum(core.manhattan_distance_m(opt_lat_eff, opt_lon_eff, u[0], u[1]) for u in users) / len(users)
            R_eff = 1.7e-8 * opt_dist_eff / wire_size
            v_drop_eff = (total_I * R_eff / v_source) * 100

            avg_walk_equ = sum(core.manhattan_distance_m(opt_lat_equ, opt_lon_equ, u[0], u[1]) for u in users) / len(users)
            R_equ = 1.7e-8 * opt_dist_equ / wire_size
            v_drop_equ = (total_I * R_equ / v_source) * 100
            
            areas_eff, reliability_eff = core.run_monte_carlo(
                500, sigma, h_sun_final, users, opt_lat_eff, opt_lon_eff, 
                "efficiency", total_I, 1.7e-8, wire_size, 5, v_source, 
                forbidden_zones, 0.18, 0.75, a_panel_limit
            )

            areas_equ, reliability_equ = core.run_monte_carlo(
                500, sigma, h_sun_final, users, opt_lat_equ, opt_lon_equ, 
                "equity", total_I, 1.7e-8, wire_size, 5, v_source, 
                forbidden_zones, 0.18, 0.75, a_panel_limit
            )

            e_produced = core.calc_energy(a_panel_limit, 0.18, h_sun_final, 0.75)
            wire_saved = max(0, 500 - opt_dist_eff)
            direct_co2, indirect_co2 = core.calc_carbon_reduction(e_produced, wire_saved)

            st.session_state.results_data = {
                'total_e_demand': total_E_demand,
                'e_produced': e_produced,
                'direct_co2': direct_co2,
                'indirect_co2': indirect_co2,
                'wire_saved': wire_saved,
                'eff': {
                    'lat': opt_lat_eff, 'lon': opt_lon_eff, 'e_loss': opt_e_loss_eff,
                    'dist': opt_dist_eff, 'areas': areas_eff, 'reliability': reliability_eff,
                    'avg_walk': avg_walk_eff, 'v_drop': v_drop_eff
                },
                'equ': {
                    'lat': opt_lat_equ, 'lon': opt_lon_equ, 'e_loss': opt_e_loss_equ,
                    'dist': opt_dist_equ, 'areas': areas_equ, 'reliability': reliability_equ,
                    'avg_walk': avg_walk_equ, 'v_drop': v_drop_equ
                },
                'opt_lat': opt_lat_eff, 'opt_lon': opt_lon_eff, 'opt_e_loss': opt_e_loss_eff,
                'opt_p_loss': opt_p_loss_eff, 'opt_dist': opt_dist_eff, 'areas': areas_eff,
                'reliability': reliability_eff
            } 
            st.session_state.page = 'result'
            st.rerun()
        else:
            st.error("ไม่พบตำแหน่งที่เหมาะสม กรุณาตรวจสอบพื้นที่ห้ามติดตั้งหรือค่าพารามิเตอร์")

elif st.session_state.page == 'result':
    if 'results_data' not in st.session_state:
        st.warning("No dynamic analysis data loaded.")
        if st.button(l['btn_back']):
            st.session_state.page = 'config'
            st.rerun()
    else:
        rd = st.session_state.results_data

        st.title(l['title'])
        st.markdown(f"**{l['subtitle']}**")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric(l['energy_req'], f"{rd['total_e_demand']:.2f} kWh")
        m2.metric(l['energy_gen'], f"{rd['e_produced']:.2f} kWh")
        m3.metric(l['loss'], f"{rd['opt_e_loss']:.4f} kWh", delta="-", delta_color="inverse")

        is_sufficient = rd['e_produced'] >= (rd['total_e_demand'] + rd['opt_e_loss'])
        if is_sufficient:
            m4.success(l['energy_sufficient'])
        else:
            m4.error(l['need_more_panels'])

        st.divider()
        col_left, col_right = st.columns([2, 1])

        with col_left:
            st.subheader(f"📍 {l['result_title']}")

            eff_d = rd['eff']
            equ_d = rd['equ']

            import pydeck as pdk
            import pandas as pd
            map_data = pd.DataFrame([
                {
                    "lat": eff_d['lat'], 
                    "lon": eff_d['lon'], 
                    "color": [231, 76, 60, 220], 
                    "size": 20 
                },
                {
                    "lat": equ_d['lat'], 
                    "lon": equ_d['lon'], 
                    "color": [46, 204, 113, 220], 
                    "size": 20
                } 
            ])
            mid_lat = (eff_d['lat'] + equ_d['lat']) / 2
            mid_lon = (eff_d['lon'] + equ_d['lon']) / 2

            st.pydeck_chart(pdk.Deck(
                initial_view_state=pdk.ViewState(
                    latitude=mid_lat,
                    longitude=mid_lon,
                    zoom=14,
                    pitch=0
                ),
                map_style=None, 
                layers=[
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=map_data,
                        get_position='[lon, lat]',
                        get_color='color',
                        get_radius='size',
                        pickable=True,
                        radius_min_pixels=5, 
                        radius_max_pixels=10
                    ) 
                ]
            ))
            st.markdown("<br>", unsafe_allow_html=True)
            card_col1, card_col2 = st.columns(2)
            with card_col1:
                ui.draw_sus_card(
                    label=f"💡 {l.get('mode_eff', 'Efficiency mode')}",
                    value=f"{eff_d['lat']:.5f}, {eff_d['lon']:.5f}",
                    unit="",
                    desc=f"{l['wire_desc']}: {eff_d['dist']:.2f} {l['unit_m']}"
                )
            with card_col2:
                ui.draw_sus_card(
                    label=f"💡 {l.get('mode_equ', 'Equity Mode')}",
                    value=f"{equ_d['lat']:.5f}, {equ_d['lon']:.5f}",
                    unit="",
                    desc=f"{l['wire_desc']}: {equ_d['dist']:.2f} {l['unit_m']}"
                )

            st.markdown(f"### {l['matrix_title']}")

            v_drop_eff_status = l['pass'] if eff_d['v_drop'] <= 5 else l['fail']
            v_drop_equ_status = l['pass'] if equ_d['v_drop'] <= 5 else l['fail']

            table_bg = "#FFFDF9"

            import numpy as np
            html_table = f"""
            <div style="width: 100%; overflow-x: auto; border-radius: 8px; background-color: {table_bg}; padding: 14px; border: 1px solid #E6E4DF;">
            <table style="width: 100%; border-collapse: collapse; font-family: sans-serif; font-size: 14px; color: #333;">
            <thead>
            <tr style="border-bottom: 2px solid #D1CFC9; text-align: left;">
            <th style="padding: 10px; font-weight: 600;">{l['metric_header']}</th>
            <th style="padding: 10px; font-weight: 600; color: #2E7D32;">{l['mode_equ']}</th>
            <th style="padding: 10px; font-weight: 600; color: #C62828;">{l['mode_eff']}</th>
            </tr>
            </thead>
            <tbody>
            <tr style="border-bottom: 1px solid #EDECE9;">
            <td style="padding: 10px; font-weight: bold;">{l['obj_label']}</td>
            <td style="padding: 10px; color: #555; font-size: 13px;">{l['obj_equ']}</td>
            <td style="padding: 10px; color: #555; font-size: 13px;">{l['obj_eff']}</td>
            </tr>
            <tr style="border-bottom: 1px solid #EDECE9;">
            <td style="padding: 10px; font-weight: bold;">{l['coord_label']}</td>
            <td style="padding: 10px; font-family: monospace;">({equ_d['lat']:.4f}, {equ_d['lon']:.4f})</td>
            <td style="padding: 10px; font-family: monospace;">({eff_d['lat']:.4f}, {eff_d['lon']:.4f})</td>
            </tr>
            <tr style="border-bottom: 1px solid #EDECE9;">
            <td style="padding: 10px; font-weight: bold;">{l['loss_label']}</td>
            <td style="padding: 10px;">{equ_d['e_loss']:.4f} {l['unit_kwh']}</td>
            <td style="padding: 10px;">{eff_d['e_loss']:.4f} {l['unit_kwh']}</td>
            </tr>
            <tr style="border-bottom: 1px solid #EDECE9;">
            <td style="padding: 10px; font-weight: bold;">{l['walk_label']}</td>
            <td style="padding: 10px;">{equ_d['avg_walk']:.2f} {l['unit_m']}</td>
            <td style="padding: 10px;">{eff_d['avg_walk']:.2f} {l['unit_m']}</td>
            </tr>
            <tr style="border-bottom: 1px solid #EDECE9;">
            <td style="padding: 10px; font-weight: bold;">{l['vdrop_label']}</td>
            <td style="padding: 10px;">{equ_d['v_drop']:.1f}% ({v_drop_equ_status})</td>
            <td style="padding: 10px;">{eff_d['v_drop']:.1f}% ({v_drop_eff_status})</td>
            </tr>
            <tr>
            <td style="padding: 10px; font-weight: bold;">{l['area_label']}</td>
            <td style="padding: 10px;">{np.mean(equ_d['areas']):.2f} {l['unit_sqm']}</td>
            <td style="padding: 10px;">{np.mean(eff_d['areas']):.2f} {l['unit_sqm']}</td>
            </tr>
            </tbody>
            </table>
            </div>
            """
            st.markdown(html_table, unsafe_allow_html=True)

        with col_right:
            st.subheader(f"🎲 Risk Simulation")
            st.metric(l['reliability'], f"{rd['reliability']:.1f}%")
            fig, ax = plt.subplots(figsize=(5, 4))
            ax.hist(rd['areas'], bins=20, color='#3498db', alpha=0.7)
            ax.axvline(st.session_state.a_panel_limit, color='red', linestyle='--', label='Limit')
            ax.set_title("Required Area Dist.")
            st.pyplot(fig)

        st.divider()

        st.subheader(l['sus_title'])
        sus_col1, sus_col2 = st.columns(2)
        with sus_col1:
            ui.draw_sus_card(l['co2_label'], f"{rd['direct_co2']:.2f}", l['unit_co2'], l['co2_desc'])
        with sus_col2:
            ui.draw_sus_card(l['wire_label'], f"{rd['wire_saved']:.2f}", l['unit_m'], l['wire_desc'])
        st.divider()

        st.subheader(l['finance_title'])
        cost_per_watt = 35.0
        system_size_watt = st.session_state.a_panel_limit * 200
        total_investment = system_size_watt * cost_per_watt
        electricity_price = 4.5

        annual_savings = (rd['e_produced'] - rd['opt_e_loss']) * electricity_price * 365
        payback_year = total_investment / annual_savings if annual_savings > 0 else 0
        f1, f2, f3 = st.columns(3)
        f1.metric(l['budget'], f"{total_investment:,.0f} {l['currency']}")
        f2.metric(l['savings_year'], f"{annual_savings:,.0f} {l['currency']}")
        f3.metric(l['payback'], f"{payback_year:.1f} {l['year']}")
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(l['btn_back'], width="stretch"):
            st.session_state.page = 'config'
            st.rerun()
