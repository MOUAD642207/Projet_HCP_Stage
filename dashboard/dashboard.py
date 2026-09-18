# -*- coding: utf-8 -*-
import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Dashboard Maroc - Analyse Socio-Économique",
    page_icon="🇲🇦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
     <style>
        .main { padding: 0rem 1rem; background: #F8FBF8; }
        .custom-header {
            background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 50%, #43A047 100%);
            padding: 2.5rem; border-radius: 15px; text-align: center;
            color: white; margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(46,125,50,0.25);
            position: relative; overflow: hidden;
        }
        .custom-header::before {
            content: ''; position: absolute; top: -50%; right: -20%;
            width: 60%; height: 200%;
            background: rgba(255, 255, 255, 0.05); transform: rotate(15deg);
        }
        .custom-header h1 {
            color:white; margin: 0; font-size: 3rem; font-weight: 700;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
            position: relative; z-index: 1;
        }
        .custom-header p {
            color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0;
            font-size: 1.2rem; position: relative; z-index: 1;
        }
        .custom-header .subtitle {
            font-size: 0.9rem; opacity: 0.8; margin-top: 0.5rem;
        }
        .section-header {
            background: linear-gradient(135deg, #e8eaf6, #c5cae9);
            padding: 1rem 1.5rem; border-radius: 12px;
            margin: 2.5rem 0 1.5rem 0; border-left: 6px solid #1a237e;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }
        .section-header h2 { margin: 0; color: #1a237e; font-weight: 600; font-size: 1.8rem; }
        .section-header .sub { color: #3949ab; font-size: 0.9rem; margin-top: 0.2rem; }

        .kpi-card {
            background: #F5F0E6; border-radius: 12px; padding: 1.2rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border-top: 4px solid #1a237e; height: 100%; min-height: 100px;
        }
        .kpi-card:hover { transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0,0,0,0.15); }
        .kpi-card .kpi-icon { font-size: 1.8rem; margin-bottom: 0.3rem; }
        .kpi-card .kpi-label {
            font-size: 0.8rem; color: #000000; text-transform: uppercase;
            letter-spacing: 0.5px; font-weight: 600;
        }
        .kpi-card .kpi-value {
            font-size: 2rem; font-weight: 700; color: #1a237e; margin: 0.2rem 0;
        }
        .kpi-card .kpi-delta {
            font-size: 0.9rem; font-weight: 600; padding: 0.15rem 0.6rem;
            border-radius: 20px; display: inline-block;
        }
        .kpi-card .kpi-delta.positive { color: #2e7d32; background: #e8f5e9; }
        .kpi-card .kpi-delta.negative { color: #c62828; background: #ffebee; }
        .kpi-card .kpi-delta.neutral { color: #f57c00; background: #fff3e0; }
        .kpi-blue { border-top-color: #1a237e; }
        .kpi-green { border-top-color: #2e7d32; }
        .kpi-orange { border-top-color: #e65100; }
        .kpi-red { border-top-color: #c62828; }
        .kpi-purple { border-top-color: #6a1b9a; }
        .kpi-teal { border-top-color: #00695c; }

        .info-container {
            background: #F5F0E6; padding: 1.5rem; border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08); margin: 1rem 0;
        }
        .info-container h4 {
            color: #1a237e; margin-top: 0; font-weight: 600;
            border-bottom: 2px solid #e8eaf6; padding-bottom: 0.5rem;
        }
        .info-container p { margin: 0.5rem 0; font-size: 1rem; color: #000000; }
        .info-container strong { color: #1a237e; }
        .footer {
            text-align: center; padding: 2rem; color: #666;
            font-size: 0.8rem; border-top: 1px solid #e0e0e0; margin-top: 2rem;
        }
        .graph-title {
            font-size: 1.1rem; font-weight: 600; color: #1a237e;
            margin: 0.5rem 0 1rem 0; padding: 0.5rem 0;
            border-bottom: 2px solid #e8eaf6;
        }
        @media (max-width: 768px) {
            .custom-header h1 { font-size: 2rem; }
            .kpi-card .kpi-value { font-size: 1.5rem; }
        }
    </style>
""", unsafe_allow_html=True)

# ============================================
# CHARGEMENT DU JSON AVEC CORRECTION
# ============================================

@st.cache_data
def charger_donnees_json():
    try:
        with open('donnees_maroc.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        population_reelle = {
            1960: {"total": 12300, "urbain": 3567, "rural": 8733},
            1961: {"total": 12521, "urbain": 3699, "rural": 8822},
            1962: {"total": 12741, "urbain": 3834, "rural": 8907},
            1963: {"total": 12960, "urbain": 3970, "rural": 8990},
            1964: {"total": 13178, "urbain": 4109, "rural": 9069},
            1965: {"total": 13395, "urbain": 4249, "rural": 9146},
            1966: {"total": 13611, "urbain": 4392, "rural": 9219},
            1967: {"total": 13826, "urbain": 4536, "rural": 9289},
            1968: {"total": 14040, "urbain": 4683, "rural": 9357},
            1969: {"total": 14253, "urbain": 4832, "rural": 9421},
            1970: {"total": 14465, "urbain": 4982, "rural": 9482},
            1971: {"total": 14676, "urbain": 5135, "rural": 9541},
            1972: {"total": 14886, "urbain": 5289, "rural": 9596},
            1973: {"total": 15095, "urbain": 5446, "rural": 9649},
            1974: {"total": 15303, "urbain": 5604, "rural": 9699},
            1975: {"total": 15510, "urbain": 5765, "rural": 9746},
            1976: {"total": 15716, "urbain": 5927, "rural": 9790},
            1977: {"total": 15922, "urbain": 6091, "rural": 9831},
            1978: {"total": 16126, "urbain": 6257, "rural": 9869},
            1979: {"total": 16329, "urbain": 6425, "rural": 9904},
            1980: {"total": 16531, "urbain": 6594, "rural": 9937},
            1981: {"total": 16732, "urbain": 6765, "rural": 9967},
            1982: {"total": 16933, "urbain": 6939, "rural": 9994},
            1983: {"total": 17132, "urbain": 7114, "rural": 10018},
            1984: {"total": 17330, "urbain": 7290, "rural": 10040},
            1985: {"total": 17528, "urbain": 7469, "rural": 10059},
            1986: {"total": 17724, "urbain": 7649, "rural": 10075},
            1987: {"total": 17919, "urbain": 7831, "rural": 10088},
            1988: {"total": 18113, "urbain": 8014, "rural": 10099},
            1989: {"total": 18307, "urbain": 8199, "rural": 10107},
            1990: {"total": 18499, "urbain": 8386, "rural": 10113},
            1991: {"total": 18691, "urbain": 8575, "rural": 10116},
            1992: {"total": 18881, "urbain": 8765, "rural": 10116},
            1993: {"total": 19070, "urbain": 8957, "rural": 10114},
            1994: {"total": 19259, "urbain": 9150, "rural": 10109},
            1995: {"total": 19446, "urbain": 9345, "rural": 10101},
            1996: {"total": 19633, "urbain": 9542, "rural": 10091},
            1997: {"total": 19818, "urbain": 9740, "rural": 10079},
            1998: {"total": 20003, "urbain": 9939, "rural": 10064},
            1999: {"total": 20186, "urbain": 10140, "rural": 10046},
            2000: {"total": 20369, "urbain": 10343, "rural": 10026},
            2001: {"total": 20550, "urbain": 10547, "rural": 10003},
            2002: {"total": 20731, "urbain": 10752, "rural": 9978},
            2003: {"total": 20910, "urbain": 10959, "rural": 9951},
            2004: {"total": 21089, "urbain": 11168, "rural": 9921},
            2005: {"total": 21267, "urbain": 11378, "rural": 9889},
            2006: {"total": 21443, "urbain": 11589, "rural": 9854},
            2007: {"total": 21619, "urbain": 11802, "rural": 9817},
            2008: {"total": 21794, "urbain": 12016, "rural": 9778},
            2009: {"total": 21967, "urbain": 12231, "rural": 9736},
            2010: {"total": 22140, "urbain": 12448, "rural": 9692},
            2011: {"total": 22312, "urbain": 12666, "rural": 9646},
            2012: {"total": 22482, "urbain": 12885, "rural": 9598},
            2013: {"total": 22652, "urbain": 13106, "rural": 9547},
            2014: {"total": 22821, "urbain": 13327, "rural": 9494},
            2015: {"total": 22989, "urbain": 13551, "rural": 9438},
            2016: {"total": 23155, "urbain": 13775, "rural": 9381},
            2017: {"total": 23321, "urbain": 14001, "rural": 9321},
            2018: {"total": 23486, "urbain": 14227, "rural": 9259},
            2019: {"total": 23650, "urbain": 14455, "rural": 9195},
            2020: {"total": 23813, "urbain": 14685, "rural": 9128},
            2021: {"total": 36313, "urbain": 23189, "rural": 13124},
            2022: {"total": 36670, "urbain": 23592, "rural": 13079},
            2023: {"total": 37022, "urbain": 23991, "rural": 13031},
            2024: {"total": 37370, "urbain": 24387, "rural": 12983},
            2025: {"total": 37712, "urbain": 24779, "rural": 12933},
            2026: {"total": 38050, "urbain": 25167, "rural": 12882},
            2027: {"total": 38381, "urbain": 25551, "rural": 12830},
            2028: {"total": 38706, "urbain": 25928, "rural": 12778},
            2029: {"total": 39023, "urbain": 26299, "rural": 12724},
            2030: {"total": 39330, "urbain": 26662, "rural": 12668},
            2031: {"total": 39627, "urbain": 27015, "rural": 12612},
            2032: {"total": 39915, "urbain": 27359, "rural": 12556},
            2033: {"total": 40194, "urbain": 27694, "rural": 12499},
            2034: {"total": 40465, "urbain": 28021, "rural": 12444},
            2035: {"total": 40727, "urbain": 28339, "rural": 12388},
            2036: {"total": 40981, "urbain": 28648, "rural": 12333},
            2037: {"total": 41225, "urbain": 28948, "rural": 12277},
            2038: {"total": 41460, "urbain": 29239, "rural": 12221},
            2039: {"total": 41686, "urbain": 29521, "rural": 12165},
            2040: {"total": 41902, "urbain": 29794, "rural": 12107},
            2041: {"total": 42107, "urbain": 30058, "rural": 12048},
            2042: {"total": 42301, "urbain": 30313, "rural": 11988},
            2043: {"total": 42486, "urbain": 30559, "rural": 11927},
            2044: {"total": 42661, "urbain": 30797, "rural": 11864},
            2045: {"total": 42829, "urbain": 31028, "rural": 11801},
            2046: {"total": 42990, "urbain": 31252, "rural": 11738},
            2047: {"total": 43145, "urbain": 31470, "rural": 11675},
            2048: {"total": 43292, "urbain": 31681, "rural": 11611},
            2049: {"total": 43431, "urbain": 31885, "rural": 11546},
            2050: {"total": 43562, "urbain": 32081, "rural": 11481}
        }

        for annee, valeurs in population_reelle.items():
            annee_str = str(annee)
            if annee_str in data['themes']['population']['data']['population_totale_par_milieu']['data']:
                data['themes']['population']['data']['population_totale_par_milieu']['data'][annee_str]['total'] = valeurs['total']
                data['themes']['population']['data']['population_totale_par_milieu']['data'][annee_str]['urbain'] = valeurs['urbain']
                data['themes']['population']['data']['population_totale_par_milieu']['data'][annee_str]['rural'] = valeurs['rural']
                taux_urb = (valeurs['urbain'] / valeurs['total']) * 100
                data['themes']['population']['data']['population_totale_par_milieu']['data'][annee_str]['taux_urbanisation'] = round(taux_urb, 2)

        return data

    except FileNotFoundError:
        st.error("❌ Fichier 'donnees_maroc.json' non trouvé")
        st.info("Assurez-vous que le fichier est dans le même dossier que ce script")
        return None
    except json.JSONDecodeError as e:
        st.error(f"❌ Erreur de format JSON: {e}")
        return None

data = charger_donnees_json()

if data is None:
    st.stop()

# ============================================
# FONCTIONS UTILES
# ============================================

def create_kpi_card(icon, label, value, delta, delta_color="normal", color_class="kpi-blue"):
    delta_class = "positive" if delta_color == "normal" and delta and '+' in str(delta) else \
                  "negative" if delta_color == "inverse" and delta and '+' in str(delta) else \
                  "neutral" if delta == "0.0%" or delta == "0%" else \
                  "positive" if delta_color == "inverse" and delta and '-' in str(delta) else \
                  "negative" if delta_color == "inverse" and delta and '+' in str(delta) else \
                  "positive" if delta_color == "normal" else "neutral"

    return f"""
    <div class="kpi-card {color_class}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-delta {delta_class}">{delta}</div>
    </div>
    """

# ============================================
# HEADER
# ============================================

st.markdown("""
    <div class="custom-header">
        <h1>🇲🇦 Tableau de Bord Socio-Économique</h1>
        <p>Maroc - Analyse complète des données démographiques, économiques et sociales</p>
        <div class="subtitle">Source: Haut-Commissariat au Plan (HCP) • Dernière mise à jour: 2026</div>
    </div>
""", unsafe_allow_html=True)

# ============================================
# 1. INDICATEURS CLÉS (KPI)
# ============================================

# ============================================
# 1. INDICATEURS CLÉS (KPI) — VALEURS RÉELLES ACTUELLES
# ============================================

st.markdown('<div class="section-header"><h2>📊 Indicateurs Clés</h2><div class="sub">Vue d\'ensemble des principaux indicateurs économiques et sociaux (valeurs réelles actualisées)</div></div>', unsafe_allow_html=True)

pop_data = data['themes']['population']['data']['population_totale_par_milieu']['data']
pop_2025 = pop_data.get('2025', {})
pop_total = pop_2025.get('total', 37800)

macro_data = data['themes']['marche_travail']['data']['indicateurs_globaux']['data']
macro_2025 = macro_data.get('2025', {})

# --- Ligne 1 : Population / PIB / Chômage / Réserves ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(create_kpi_card(
        "👥", "Population Totale",
        "37,8 M", "+1.2%", "normal", "kpi-blue"
    ), unsafe_allow_html=True)

with col2:
    st.markdown(create_kpi_card(
        "📈", "PIB nominal",
        "~182 Mds USD", "+3.5%", "normal", "kpi-green"
    ), unsafe_allow_html=True)

with col3:
    st.markdown(create_kpi_card(
        "💼", "Taux de Chômage",
        "9,5%", "-0.4%", "inverse", "kpi-red"
    ), unsafe_allow_html=True)

with col4:
    st.markdown(create_kpi_card(
        "💰", "Réserves de Change",
        "~496 Mds MAD", "+5.2%", "normal", "kpi-purple"
    ), unsafe_allow_html=True)

# --- Ligne 2 : Urbanisation / Dette / Inflation / PIB/hab ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(create_kpi_card(
        "🏠", "Taux d'Urbanisation",
        "65,7%", "+0.6%", "normal", "kpi-teal"
    ), unsafe_allow_html=True)

with col2:
    st.markdown(create_kpi_card(
        "📊", "Dette Publique",
        "~68% du PIB", "+1.0%", "inverse", "kpi-orange"
    ), unsafe_allow_html=True)

with col3:
    st.markdown(create_kpi_card(
        "📉", "Taux d'Inflation",
        "~1,3%", "-0.2%", "inverse", "kpi-green"
    ), unsafe_allow_html=True)

with col4:
    st.markdown(create_kpi_card(
        "💶", "PIB par Habitant",
        "~3 643 USD", "+2.8%", "normal", "kpi-blue"
    ), unsafe_allow_html=True)

# --- Ligne 3 : Taux directeur / Compte courant / Scolarisation / Activité ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(create_kpi_card(
        "🏦", "Taux Directeur",
        "2,25%", "0.0%", "neutral", "kpi-purple"
    ), unsafe_allow_html=True)

with col2:
    st.markdown(create_kpi_card(
        "💳", "Solde Compte Courant",
        "Déficit modéré", "Structurel", "inverse", "kpi-orange"
    ), unsafe_allow_html=True)

with col3:
    st.markdown(create_kpi_card(
        "🎓", "Scolarisation Primaire",
        "> 99%", "+0.2%", "normal", "kpi-teal"
    ), unsafe_allow_html=True)

with col4:
    st.markdown(create_kpi_card(
        "📈", "Taux d'Activité",
        "~43%", "-0.1%", "inverse", "kpi-orange"
    ), unsafe_allow_html=True)

st.markdown("---")
   
    

# ============================================
# 2. DÉMOGRAPHIE
# ============================================

st.markdown('<div class="section-header"><h2>👥 Analyse Démographique</h2><div class="sub">Évolution de la population et tendances d\'urbanisation</div></div>', unsafe_allow_html=True)

pop_dict = data['themes']['population']['data']['population_totale_par_milieu']['data']
df_pop = pd.DataFrame.from_dict(pop_dict, orient='index').reset_index()
df_pop.columns = ['Annee', 'Total', 'Urbain', 'Rural', 'Taux_Urbanisation']
df_pop['Annee'] = df_pop['Annee'].astype(int)

st.markdown('<p class="graph-title">📈 Évolution de la Population (1960-2050)</p>', unsafe_allow_html=True)

fig = go.Figure()
fig.add_trace(go.Scatter(x=df_pop['Annee'], y=df_pop['Total'] / 1000, name='Population Totale',
    line=dict(color='#1a237e', width=4), fill='tozeroy', fillcolor='rgba(26, 35, 126, 0.1)'))
fig.add_trace(go.Scatter(x=df_pop['Annee'], y=df_pop['Urbain'] / 1000, name='Population Urbaine',
    line=dict(color='#2e7d32', width=3)))
fig.add_trace(go.Scatter(x=df_pop['Annee'], y=df_pop['Rural'] / 1000, name='Population Rurale',
    line=dict(color='#e65100', width=3)))

fig.update_layout(
    xaxis_title="Année", yaxis_title="Population (Millions)",
    hovermode='x unified', height=450,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(size=12))
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<p class="graph-title">🏙️ Taux d\'Urbanisation</p>', unsafe_allow_html=True)
    fig = px.area(df_pop, x='Annee', y='Taux_Urbanisation',
        labels={'Taux_Urbanisation': 'Taux (%)'})
    fig.update_traces(fill='tozeroy', line=dict(color='#1a237e', width=3))
    fig.add_hline(y=50, line_dash="dash", line_color="#e65100",
                 annotation_text="Seuil 50% (2000)", annotation_position="bottom right")
    fig.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)', font=dict(size=12))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<p class="graph-title">📊 Répartition Urbain/Rural (2025)</p>', unsafe_allow_html=True)
    pop_2025_data = pop_data.get('2025', {})
    valeurs = [pop_2025_data.get('urbain', 0), pop_2025_data.get('rural', 0)]
    fig = go.Figure(data=[go.Pie(labels=['Urbain', 'Rural'], values=valeurs, hole=0.4,
        marker=dict(colors=['#1a237e', '#90caf9']), textinfo='label+percent',
        textposition='inside', pull=[0.05, 0])])
    fig.update_layout(title=f"Population Totale: {pop_2025_data.get('total', 0)/1000:.1f} M",
        height=400, showlegend=True, plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)', font=dict(size=12))
    st.plotly_chart(fig, use_container_width=True)

# --- NOUVEAU : Population par région 2030 + donut ---
st.markdown('<p class="graph-title">🗺️ Population par région — projection régionale</p>', unsafe_allow_html=True)

reg_raw = data['themes']['population']['data']['projections_regionales']['data']
reg_records = []
for year, regions in reg_raw.items():
    for region, vals in regions.items():
        reg_records.append({"annee": int(year), "region": region, **vals})
df_reg = pd.DataFrame(reg_records)

year_reg = st.select_slider("Année de projection", options=sorted(df_reg['annee'].unique()),
                            value=int(df_reg['annee'].max()), key="reg_year")
df_reg_year = df_reg[df_reg['annee'] == year_reg].sort_values('population', ascending=False)

c1, c2 = st.columns([3, 2])
with c1:
    fig = px.bar(df_reg_year, x='region', y='population', color='region',
        color_discrete_sequence=px.colors.qualitative.Set3,
        labels={'population': 'population (milliers)', 'region': ''})
    fig.update_layout(height=500, showlegend=False, plot_bgcolor='white',
        paper_bgcolor='white', xaxis_tickangle=-40, yaxis=dict(gridcolor='#EEEEEE'),
        title=f"Population par région — {year_reg} (milliers)")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    fig = px.pie(df_reg_year, names='region', values='population', hole=0.4,
        title="Répartition régionale")
    fig.update_traces(textinfo='percent', textposition='inside')
    fig.update_layout(height=500, plot_bgcolor='white', paper_bgcolor='white',
        legend=dict(orientation="v", x=1.02, y=1, font=dict(size=10)),
        margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================
# 3. MACRO-ÉCONOMIE - PIB
# ============================================

st.markdown('<div class="section-header"><h2>📈 Analyse Macro-Économique</h2><div class="sub">Évolution du PIB et de ses composantes</div></div>', unsafe_allow_html=True)

pib_dict = data['themes']['pib']['data']
df_pib = pd.DataFrame.from_dict(pib_dict, orient='index').reset_index()
df_pib.columns = ['Periode', 'PIB', 'Importations', 'Consommation_Menages',
                 'Consommation_Admin', 'CF_ISBL', 'Investissement', 'Exportations']

st.markdown('<p class="graph-title">📊 Évolution du PIB et ses Composantes</p>', unsafe_allow_html=True)

fig = go.Figure()
fig.add_trace(go.Scatter(x=df_pib['Periode'], y=df_pib['PIB'], name='PIB Total',
    line=dict(color='#1a237e', width=4)))
fig.add_trace(go.Scatter(x=df_pib['Periode'], y=df_pib['Consommation_Menages'],
    name='Consommation Ménages', line=dict(color='#2e7d32', width=3)))
fig.add_trace(go.Scatter(x=df_pib['Periode'], y=df_pib['Investissement'],
    name='Investissement', line=dict(color='#e65100', width=3)))
fig.add_trace(go.Scatter(x=df_pib['Periode'], y=df_pib['Exportations'],
    name='Exportations', line=dict(color='#c62828', width=3)))
fig.add_trace(go.Scatter(x=df_pib['Periode'], y=df_pib['Importations'],
    name='Importations', line=dict(color='#6a1b9a', width=3, dash='dash')))

fig.update_layout(
    xaxis_title="Trimestre", yaxis_title="Montant (Millions MAD)",
    hovermode='x unified', height=450,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(size=12))
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<p class="graph-title">🧩 Structure du PIB (Dernier Trimestre)</p>', unsafe_allow_html=True)
    last_period = df_pib.iloc[0]
    pib_components = {
        'Consommation Ménages': last_period['Consommation_Menages'] / last_period['PIB'] * 100,
        'Investissement': last_period['Investissement'] / last_period['PIB'] * 100,
        'Exportations': last_period['Exportations'] / last_period['PIB'] * 100,
        'Importations': last_period['Importations'] / last_period['PIB'] * 100
    }
    colors = ['#1a237e', '#0d47a1', '#42a5f5', '#90caf9']
    fig = go.Figure(data=[go.Bar(x=list(pib_components.keys()),
        y=list(pib_components.values()), marker_color=colors,
        text=[f"{v:.1f}%" for v in pib_components.values()],
        textposition='outside', textfont=dict(size=14, weight='bold'))])
    fig.update_layout(title=f"PIB: {last_period['PIB']:,} Millions MAD",
        yaxis_title="% du PIB", height=400, plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)', font=dict(size=12))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<p class="graph-title">📈 Évolution Trimestrielle du PIB</p>', unsafe_allow_html=True)
    fig = px.line(df_pib, x='Periode', y='PIB', labels={'PIB': 'PIB (Millions MAD)'})
    fig.update_traces(line=dict(color='#1a237e', width=4))
    fig.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)', font=dict(size=12))
    st.plotly_chart(fig, use_container_width=True)

# --- NOUVEAU : Évolution du PIB (ligne verte) ---
st.markdown('<p class="graph-title">💰 Évolution du PIB</p>', unsafe_allow_html=True)
df_pib_sorted = df_pib.sort_values('Periode')
fig = px.line(df_pib_sorted, x='Periode', y='PIB',
              labels={'PIB': 'pib', 'Periode': 'periode'})
fig.update_traces(line=dict(color='#2E8B70', width=3))
fig.update_layout(height=450, plot_bgcolor='white', paper_bgcolor='white',
                  yaxis=dict(gridcolor='#EEEEEE'),
                  xaxis=dict(tickangle=-60, nticks=25))
st.plotly_chart(fig, use_container_width=True)

# --- NOUVEAU : Composantes de la demande (aire empilée) ---
st.markdown('<p class="graph-title">📊 Composantes de la demande (emplois du PIB)</p>', unsafe_allow_html=True)
composantes_cols = ['Consommation_Menages', 'Consommation_Admin', 'CF_ISBL', 'Investissement', 'Exportations']
df_comp = df_pib_sorted[['Periode'] + composantes_cols].copy()
df_comp = df_comp.rename(columns={
    'Consommation_Menages': 'consommation_menages',
    'Consommation_Admin': 'consommation_admin',
    'CF_ISBL': 'cf_isbl',
    'Investissement': 'fbc',
    'Exportations': 'exportations',
})
df_comp_melt = df_comp.melt(id_vars='Periode', var_name='Composante', value_name='Montant')

fig = px.area(df_comp_melt, x='Periode', y='Montant', color='Composante',
    color_discrete_sequence=["#8FD6B4", "#F9C784", "#A9B7E0", "#F4A6C0", "#C8E6A0"],
    labels={'Montant': 'Millions MAD', 'Periode': 'Trimestre'})
fig.update_layout(height=500, plot_bgcolor='white', paper_bgcolor='white',
    legend=dict(orientation="v", x=1.02, y=1, title="Composante"),
    yaxis=dict(gridcolor='#EEEEEE'),
    xaxis=dict(tickangle=-60, nticks=25))
st.plotly_chart(fig, use_container_width=True)

# --- NOUVEAU : Balance commerciale ---
st.markdown('<p class="graph-title">⚖️ Balance commerciale (Exportations − Importations)</p>', unsafe_allow_html=True)
df_pib_sorted = df_pib_sorted.copy()
df_pib_sorted['balance_commerciale'] = df_pib_sorted['Exportations'] - df_pib_sorted['Importations']

fig = go.Figure()
fig.add_trace(go.Bar(
    x=df_pib_sorted['Periode'],
    y=df_pib_sorted['balance_commerciale'],
    marker_color=['#E74C3C' if v < 0 else '#2ECC71' for v in df_pib_sorted['balance_commerciale']]))
fig.update_layout(height=450, plot_bgcolor='white', paper_bgcolor='white',
    yaxis=dict(title='Millions MAD', gridcolor='#EEEEEE'),
    xaxis=dict(tickangle=-60, nticks=25))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================
# 4. MARCHÉ DU TRAVAIL
# ============================================

st.markdown('<div class="section-header"><h2>💼 Marché du Travail</h2><div class="sub">Analyse du chômage et de l\'emploi par région</div></div>', unsafe_allow_html=True)

macro_dict = data['themes']['marche_travail']['data']['indicateurs_globaux']['data']
df_macro = pd.DataFrame.from_dict(macro_dict, orient='index').reset_index()
df_macro.columns = ['Annee', 'Chomage_National', 'Chomage_Urbain', 'Chomage_Jeunes', 'Taux_Activite']

st.markdown('<p class="graph-title">📊 Évolution du Taux de Chômage</p>', unsafe_allow_html=True)

fig = go.Figure()
fig.add_trace(go.Scatter(x=df_macro['Annee'], y=df_macro['Chomage_National'],
    name='National', line=dict(color='#c62828', width=4)))
fig.add_trace(go.Scatter(x=df_macro['Annee'], y=df_macro['Chomage_Urbain'],
    name='Urbain', line=dict(color='#e65100', width=3)))
fig.add_trace(go.Scatter(x=df_macro['Annee'], y=df_macro['Chomage_Jeunes'],
    name='Jeunes (15-24 ans)', line=dict(color='#6a1b9a', width=3, dash='dash')))
fig.add_trace(go.Scatter(x=df_macro['Annee'], y=df_macro['Taux_Activite'],
    name="Taux d'Activité", line=dict(color='#1a237e', width=3, dash='dot')))

fig.update_layout(xaxis_title="Année", yaxis_title="Taux (%)",
    hovermode='x unified', height=450,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(size=12))
st.plotly_chart(fig, use_container_width=True)

st.markdown('<p class="graph-title">🗺️ Top 20 Provinces - Taux de Chômage (2025)</p>', unsafe_allow_html=True)

province_data = data['themes']['marche_travail']['data']['taux_chomage_par_province']['data']['national']
df_prov = pd.DataFrame.from_dict(province_data, orient='index').reset_index()
df_prov.columns = ['Province', '2025', '2024', '2023', '2022', '2021', '2020', '2019', '2018', '2017']
df_prov = df_prov.dropna(subset=['2025'])
df_prov = df_prov.nlargest(20, '2025')

fig = px.bar(df_prov, x='Province', y='2025', title="",
    labels={'2025': 'Taux de Chômage (%)'}, color='2025',
    color_continuous_scale='RdBu_r', text='2025')
fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig.update_layout(xaxis_tickangle=-45, height=500,
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    font=dict(size=12), coloraxis_colorbar=dict(title="Taux (%)"))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================
# 5. FINANCES PUBLIQUES
# ============================================

st.markdown('<div class="section-header"><h2>💰 Finances Publiques</h2><div class="sub">Budget de l\'État par ministère</div></div>', unsafe_allow_html=True)

budget_data = data['themes']['finances_publiques']['data']
df_budget = pd.DataFrame(budget_data)

st.markdown('<p class="graph-title">📊 Dépenses Publiques par Ministère (2024-2025)</p>', unsafe_allow_html=True)

fig = go.Figure()
fig.add_trace(go.Bar(x=df_budget['ministere'], y=df_budget['fonctionnement_2024'],
    name='Fonctionnement 2024', marker_color='#1a237e',
    text=df_budget['fonctionnement_2024'], textposition='outside', texttemplate='%{text:,.0f}'))
fig.add_trace(go.Bar(x=df_budget['ministere'], y=df_budget['investissement_2024'],
    name='Investissement 2024', marker_color='#42a5f5',
    text=df_budget['investissement_2024'], textposition='outside', texttemplate='%{text:,.0f}'))
fig.add_trace(go.Bar(x=df_budget['ministere'], y=df_budget['investissement_2025'],
    name='Investissement 2025', marker_color='#0d47a1',
    text=df_budget['investissement_2025'], textposition='outside', texttemplate='%{text:,.0f}'))

fig.update_layout(xaxis_title="Ministère", yaxis_title="Millions MAD",
    barmode='group', xaxis_tickangle=-45, height=550,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    font=dict(size=11), showlegend=True)
st.plotly_chart(fig, use_container_width=True)

st.markdown('<p class="graph-title">📈 Variation des Investissements (2024 → 2025)</p>', unsafe_allow_html=True)

fig = px.bar(df_budget.sort_values('variation', ascending=True),
    x='ministere', y='variation',
    labels={'variation': 'Variation (%)', 'ministere': 'Ministère'},
    color='variation', color_continuous_scale='RdYlGn', text='variation')
fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
fig.add_hline(y=0, line_dash="dash", line_color="black", line_width=2)
fig.update_layout(xaxis_tickangle=-45, height=450,
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    font=dict(size=12), coloraxis_colorbar=dict(title="Variation (%)"))
st.plotly_chart(fig, use_container_width=True)

# --- NOUVEAU : Répartition budget fonctionnement 2024 (donut) ---
st.markdown('<p class="graph-title">🍩 Répartition du budget de fonctionnement 2024</p>', unsafe_allow_html=True)
fig = px.pie(df_budget, names='ministere', values='fonctionnement_2024', hole=0.4)
fig.update_traces(textinfo='percent', textposition='inside')
fig.update_layout(height=600, plot_bgcolor='white', paper_bgcolor='white',
    legend=dict(orientation="v", x=1.02, y=1, font=dict(size=11)),
    margin=dict(l=20, r=20, t=40, b=20))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================
# 6. ÉDUCATION
# ============================================

st.markdown('<div class="section-header"><h2>🎓 Éducation</h2><div class="sub">Taux de scolarisation par cycle et par sexe</div></div>', unsafe_allow_html=True)

edu_data = data['themes']['education']['data']
df_edu_list = []
for annee, cycles in edu_data.items():
    for cycle in cycles:
        df_edu_list.append({
            'Annee': int(annee),
            'Cycle': cycle['cycle'],
            'Global': cycle['global'],
            'Filles': cycle['filles'],
            'Garcons': cycle['garcons']
        })
df_edu = pd.DataFrame(df_edu_list)

df_edu_pivot = df_edu.pivot_table(index='Annee', columns='Cycle', values='Global', aggfunc='first').reset_index()
new_cols = {'Annee': 'Annee'}
for col in df_edu_pivot.columns[1:]:
    if 'Primaire' in col:
        new_cols[col] = 'Primaire'
    elif 'Collégial' in col:
        new_cols[col] = 'College'
    elif 'Qualifiant' in col:
        new_cols[col] = 'Secondaire'
    else:
        new_cols[col] = col
df_edu_pivot = df_edu_pivot.rename(columns=new_cols)

st.markdown('<p class="graph-title">📈 Évolution de la Scolarisation par Cycle</p>', unsafe_allow_html=True)

fig = go.Figure()
colors = {'Primaire': '#2e7d32', 'College': '#1a237e', 'Secondaire': '#e65100'}
for col in ['Primaire', 'College', 'Secondaire']:
    if col in df_edu_pivot.columns:
        fig.add_trace(go.Scatter(x=df_edu_pivot['Annee'], y=df_edu_pivot[col],
            name=col, line=dict(color=colors.get(col, 'gray'), width=3),
            mode='lines+markers', marker=dict(size=6)))

fig.update_layout(xaxis_title="Année", yaxis_title="Taux (%)",
    hovermode='x unified', height=450,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(size=12))
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<p class="graph-title">📊 Scolarisation par Genre (2025)</p>', unsafe_allow_html=True)
    edu_2025 = df_edu[df_edu['Annee'] == 2025]
    cycles_list = ['Primaire', 'College', 'Secondaire']
    cycles_map = {
        'Primaire': '6-11 ans (Primaire)',
        'College': '12-14 ans (Collégial)',
        'Secondaire': '15-17 ans (Qualifiant)'
    }
    global_vals, filles_vals, garcons_vals = [], [], []
    for cycle in cycles_list:
        cycle_name = cycles_map.get(cycle, cycle)
        cycle_data = edu_2025[edu_2025['Cycle'] == cycle_name]
        if not cycle_data.empty:
            global_vals.append(cycle_data['Global'].values[0])
            filles_vals.append(cycle_data['Filles'].values[0])
            garcons_vals.append(cycle_data['Garcons'].values[0])
        else:
            global_vals.append(0); filles_vals.append(0); garcons_vals.append(0)

    fig = go.Figure()
    fig.add_trace(go.Bar(x=cycles_list, y=global_vals, name='Global',
        marker_color='#1a237e', text=[f"{v:.1f}%" for v in global_vals], textposition='outside'))
    fig.add_trace(go.Bar(x=cycles_list, y=filles_vals, name='Filles',
        marker_color='#e91e63', text=[f"{v:.1f}%" for v in filles_vals], textposition='outside'))
    fig.add_trace(go.Bar(x=cycles_list, y=garcons_vals, name='Garçons',
        marker_color='#2196f3', text=[f"{v:.1f}%" for v in garcons_vals], textposition='outside'))

    fig.update_layout(barmode='group', yaxis_title="Taux (%)", height=400,
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<p class="graph-title">📈 Progression Globale (2010-2025)</p>', unsafe_allow_html=True)
    edu_2010 = df_edu[df_edu['Annee'] == 2010]
    edu_2025 = df_edu[df_edu['Annee'] == 2025]
    progressions = []
    cycle_labels = {
        '6-11 ans (Primaire)': 'Primaire',
        '12-14 ans (Collégial)': 'Collège',
        '15-17 ans (Qualifiant)': 'Secondaire'
    }
    for cycle_name, label in cycle_labels.items():
        data_2010 = edu_2010[edu_2010['Cycle'] == cycle_name]
        data_2025 = edu_2025[edu_2025['Cycle'] == cycle_name]
        if not data_2010.empty and not data_2025.empty:
            prog = data_2025['Global'].values[0] - data_2010['Global'].values[0]
            progressions.append((label, prog, data_2010['Global'].values[0], data_2025['Global'].values[0]))

    fig = go.Figure()
    colors_list = ['#2e7d32', '#1a237e', '#e65100']
    for i, (label, prog, start, end) in enumerate(progressions):
        fig.add_trace(go.Bar(x=[label], y=[prog], name=label,
            marker_color=colors_list[i % len(colors_list)],
            text=[f"+{prog:.1f}%"], textposition='outside',
            textfont=dict(size=14, weight='bold')))
        fig.add_annotation(x=label, y=prog/2,
            text=f"{start:.1f}% → {end:.1f}%", showarrow=False,
            font=dict(size=11, color='grey'),
            bgcolor='rgba(0,0,0,0.6)', bordercolor='grey', borderwidth=1, borderpad=3)

    fig.update_layout(title="Progression 2010 → 2025", yaxis_title="Points de pourcentage",
        height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# --- NOUVEAU : Comparaison 3 cycles (dernière année) ---
last_year = int(df_edu['Annee'].max())
df_last = df_edu[df_edu['Annee'] == last_year].copy()
df_melt = df_last.melt(id_vars='Cycle', value_vars=['Global', 'Filles', 'Garcons'],
                       var_name='variable', value_name='value')
df_melt['variable'] = df_melt['variable'].replace({'Global': 'global', 'Filles': 'filles', 'Garcons': 'garcons'})

st.markdown(f'<p class="graph-title">📊 Comparaison des 3 cycles — {last_year}</p>', unsafe_allow_html=True)
fig = px.bar(df_melt, x='Cycle', y='value', color='variable', barmode='group',
    color_discrete_map={'global': '#2E8B70', 'filles': '#F08050', 'garcons': '#7B8BC9'},
    labels={'value': 'valeur', 'Cycle': 'cycle', 'variable': 'variable'})
fig.update_layout(height=420, plot_bgcolor='white', paper_bgcolor='white',
    legend=dict(orientation="v", x=1.02, y=1, title="variable"),
    yaxis=dict(gridcolor='#EEEEEE', range=[0, 100]))
st.plotly_chart(fig, use_container_width=True)

# --- NOUVEAU : Écart filles / garçons dans le temps ---
df_ecart = df_edu.copy()
df_ecart['ecart_filles_garcons'] = df_ecart['Filles'] - df_ecart['Garcons']

st.markdown('<p class="graph-title">📈 Écart filles / garçons dans le temps (points de %)</p>', unsafe_allow_html=True)
fig = px.line(df_ecart, x='Annee', y='ecart_filles_garcons', color='Cycle',
    color_discrete_sequence=['#2E8B70', '#F08050', '#7B8BC9'],
    labels={'ecart_filles_garcons': 'ecart_filles_garcons', 'Annee': 'annee', 'Cycle': 'cycle'})
fig.update_traces(line=dict(width=2.5))
fig.add_hline(y=0, line_dash="dash", line_color="black", line_width=1)
fig.update_layout(height=450, plot_bgcolor='white', paper_bgcolor='white',
    legend=dict(orientation="v", x=1.02, y=1, title="cycle"),
    yaxis=dict(gridcolor='#EEEEEE'))
st.plotly_chart(fig, use_container_width=True)

# --- NOUVEAU : Taux de scolarisation par cycle (dropdown) ---
st.markdown('<p class="graph-title">🔎 Taux de scolarisation par cycle (filtre interactif)</p>', unsafe_allow_html=True)
cycles_dispo = sorted(df_edu['Cycle'].unique())
cycle_choisi = st.selectbox("Cycle", cycles_dispo, index=0, key="cycle_select")

df_cycle = df_edu[df_edu['Cycle'] == cycle_choisi].sort_values('Annee')
df_cycle_melt = df_cycle.melt(id_vars='Annee', value_vars=['Global', 'Filles', 'Garcons'],
                              var_name='Catégorie', value_name='Taux')
df_cycle_melt['Catégorie'] = df_cycle_melt['Catégorie'].replace(
    {'Global': 'global', 'Filles': 'filles', 'Garcons': 'garcons'})

fig = px.line(df_cycle_melt, x='Annee', y='Taux', color='Catégorie',
    color_discrete_map={'global': '#2E8B70', 'filles': '#F08050', 'garcons': '#7B8BC9'},
    labels={'Taux': 'Taux (%)', 'Annee': 'Année'})
fig.update_traces(line=dict(width=2.5))
fig.update_layout(height=450, plot_bgcolor='white', paper_bgcolor='white',
    legend=dict(orientation="v", x=1.02, y=1, title="Catégorie"),
    yaxis=dict(gridcolor='#EEEEEE'),
    title=f"Taux de scolarisation — {cycle_choisi}")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================
# 7. TYPE DE CHÔMAGE
# ============================================

st.markdown('<div class="section-header"><h2>📊 Analyse du Type de Chômage</h2><div class="sub">Répartition des chômeurs ayant déjà travaillé ou jamais travaillé</div></div>', unsafe_allow_html=True)

type_chomage = data['themes']['marche_travail']['data']['type_chomage']['data']
type_data = []
for category, values in type_chomage.items():
    for milieu, periods in values.items():
        for period, value in periods.items():
            type_data.append({'Type': category, 'Milieu': milieu, 'Période': period, 'Valeur': value})
df_type = pd.DataFrame(type_data)

st.markdown('<p class="graph-title">📈 Évolution du Type de Chômage (National)</p>', unsafe_allow_html=True)

df_type_national = df_type[df_type['Milieu'] == 'national']
fig = go.Figure()
for type_chom in df_type_national['Type'].unique():
    df_t = df_type_national[df_type_national['Type'] == type_chom]
    label = "Ayant déjà travaillé" if "ayant_deja" in type_chom else "N'ayant jamais travaillé"
    fig.add_trace(go.Scatter(x=df_t['Période'], y=df_t['Valeur'], name=label, line=dict(width=3)))

fig.update_layout(xaxis_title="Période", yaxis_title="Pourcentage (%)",
    hovermode='x unified', height=400,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(size=12))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================
# 8. AGRICULTURE & PÊCHE (NOUVELLE SECTION)
# ============================================

st.markdown('<div class="section-header"><h2>🌾 Agriculture & Pêche</h2><div class="sub">Production céréalière et activités halieutiques</div></div>', unsafe_allow_html=True)

agri_data = data['themes']['agriculture_peche']['data']
df_agri = pd.DataFrame.from_dict(agri_data, orient='index').reset_index()
df_agri.columns = ['Annee', 'Production_Ceres', 'Debarquements_Peche', 'Valeur_Peche']
df_agri['Annee'] = df_agri['Annee'].astype(int)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<p class="graph-title">🎣 Débarquements de pêche (tonnes)</p>', unsafe_allow_html=True)
    fig = px.line(df_agri, x='Annee', y='Debarquements_Peche', markers=True,
        labels={'Debarquements_Peche': 'debarquements_peche', 'Annee': 'annee'})
    fig.update_traces(line=dict(color='#2E8B70', width=3), marker=dict(size=8, color='#2E8B70'))
    fig.update_layout(height=400, plot_bgcolor='white', paper_bgcolor='white',
        font=dict(size=12), yaxis=dict(gridcolor='#EEEEEE'))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<p class="graph-title">💰 Valeur de la pêche (Millions MAD)</p>', unsafe_allow_html=True)
    fig = px.line(df_agri, x='Annee', y='Valeur_Peche', markers=True,
        labels={'Valeur_Peche': 'valeur_peche', 'Annee': 'annee'})
    fig.update_traces(line=dict(color='#2E8B70', width=3), marker=dict(size=8, color='#2E8B70'))
    fig.update_layout(height=400, plot_bgcolor='white', paper_bgcolor='white',
        font=dict(size=12), yaxis=dict(gridcolor='#EEEEEE'))
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<p class="graph-title">🌾 Production céréalière (tonnes)</p>', unsafe_allow_html=True)
fig = px.bar(df_agri, x='Annee', y='Production_Ceres',
    labels={'Production_Ceres': 'production_ceres', 'Annee': 'annee'})
fig.update_traces(marker_color='#2E8B70')
fig.update_layout(height=400, plot_bgcolor='white', paper_bgcolor='white',
    font=dict(size=12), yaxis=dict(gridcolor='#EEEEEE'))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================
# 9. TOURISME & TRANSPORT (NOUVELLE SECTION)
# ============================================

st.markdown('<div class="section-header"><h2>✈️ Tourisme & Transport</h2><div class="sub">Arrivées touristiques, nuitées et recettes</div></div>', unsafe_allow_html=True)

tour_data = data['themes']['tourisme_transport']['data']
df_tour = pd.DataFrame.from_dict(tour_data, orient='index').reset_index()
df_tour.columns = ['Annee', 'Arrivees', 'Nuites', 'Recettes']
df_tour['Annee'] = df_tour['Annee'].astype(int)

st.markdown('<p class="graph-title">📈 Arrivées touristiques et nuitées</p>', unsafe_allow_html=True)
df_tour_melt = df_tour.melt(id_vars='Annee', value_vars=['Arrivees', 'Nuites'],
                            var_name='variable', value_name='value')
df_tour_melt['variable'] = df_tour_melt['variable'].replace(
    {'Arrivees': 'arrivees_touristiques', 'Nuites': 'nuitées'})

fig = px.line(df_tour_melt, x='Annee', y='value', color='variable',
    color_discrete_map={'arrivees_touristiques': '#2E8B70', 'nuitées': '#F08050'},
    labels={'value': 'value', 'Annee': 'annee', 'variable': 'variable'})
fig.update_traces(line=dict(width=2.5))
fig.update_layout(height=450, plot_bgcolor='white', paper_bgcolor='white',
    legend=dict(orientation="v", x=1.02, y=1, title="variable"),
    yaxis=dict(gridcolor='#EEEEEE'))
st.plotly_chart(fig, use_container_width=True)

st.markdown('<p class="graph-title">💰 Recettes voyages (Millions MAD)</p>', unsafe_allow_html=True)
fig = px.bar(df_tour, x='Annee', y='Recettes', labels={'Recettes': 'recettes', 'Annee': 'annee'})
fig.update_traces(marker_color='#2E8B70')
fig.update_layout(height=400, plot_bgcolor='white', paper_bgcolor='white',
    yaxis=dict(gridcolor='#EEEEEE'))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================
# 10. ÉNERGIE & MINES (NOUVELLE SECTION)
# ============================================

st.markdown('<div class="section-header"><h2>⚡ Énergie & Mines</h2><div class="sub">Production électrique, renouvelables et phosphate</div></div>', unsafe_allow_html=True)

energie_data = data['themes']['energie_mines']['data']
df_energie = pd.DataFrame.from_dict(energie_data, orient='index').reset_index()
df_energie.columns = ['Annee', 'Production_Electrique', 'Part_Renouvelable', 'Phosphate']
df_energie['Annee'] = df_energie['Annee'].astype(int)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<p class="graph-title">⚡ Production électrique et part des énergies renouvelables</p>', unsafe_allow_html=True)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=df_energie['Annee'], y=df_energie['Production_Electrique'],
        name='Production électrique (GWh)', marker_color='#2E8B70'), secondary_y=False)
    fig.add_trace(go.Scatter(x=df_energie['Annee'], y=df_energie['Part_Renouvelable'],
        name='Part renouvelable (%)', mode='lines+markers',
        line=dict(color='#7B68EE', width=3), marker=dict(size=7)), secondary_y=True)
    fig.update_yaxes(title_text="GWh", secondary_y=False)
    fig.update_yaxes(title_text="%", secondary_y=True)
    fig.update_layout(height=420, plot_bgcolor='white', paper_bgcolor='white',
        legend=dict(orientation="h", y=1.12, x=0.5, xanchor='center'), font=dict(size=12))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<p class="graph-title">🪨 Production de phosphate (milliers de tonnes)</p>', unsafe_allow_html=True)
    fig = px.area(df_energie, x='Annee', y='Phosphate',
        labels={'Phosphate': 'phosphate', 'Annee': 'annee'})
    fig.update_traces(line=dict(color='#2E8B70', width=2), fillcolor='rgba(46,139,112,0.25)')
    fig.update_layout(height=420, plot_bgcolor='white', paper_bgcolor='white',
        font=dict(size=12), yaxis=dict(gridcolor='#EEEEEE'))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================
# 11. BTP & IMMOBILIER (NOUVELLE SECTION)
# ============================================

st.markdown('<div class="section-header"><h2>🏗️ BTP & Immobilier</h2><div class="sub">Indice des prix des actifs immobiliers</div></div>', unsafe_allow_html=True)

btp_data = data['themes']['btp_immobilier']['data']
df_btp = pd.DataFrame.from_dict(btp_data, orient='index').reset_index()
df_btp.columns = ['Annee', 'Consommation_Ciment', 'Superficie_Autorisee', 'IPAI']
df_btp['Annee'] = df_btp['Annee'].astype(int)

st.markdown('<p class="graph-title">📈 Indice des prix des actifs immobiliers (IPAI)</p>', unsafe_allow_html=True)
fig = px.line(df_btp, x='Annee', y='IPAI', markers=True,
    labels={'IPAI': 'ipai', 'Annee': 'annee'})
fig.update_traces(line=dict(color='#2E8B70', width=3), marker=dict(size=7, color='#2E8B70'))
fig.update_layout(height=400, plot_bgcolor='white', paper_bgcolor='white',
    yaxis=dict(gridcolor='#EEEEEE'))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================
# 12. INDICATEURS MONÉTAIRES (NOUVELLE SECTION)
# ============================================

st.markdown('<div class="section-header"><h2>🏦 Indicateurs Monétaires</h2><div class="sub">Taux directeur, inflation et crédits bancaires</div></div>', unsafe_allow_html=True)

mon_data = data['themes']['indicateurs_monetaires']['data']
df_mon = pd.DataFrame.from_dict(mon_data, orient='index').reset_index()
df_mon.columns = ['Annee', 'Taux_Directeur', 'Inflation', 'Credits_PIB']
df_mon['Annee'] = df_mon['Annee'].astype(int)

col1, col2 = st.columns(2)
with col1:
    st.markdown('<p class="graph-title">📉 Taux directeur vs inflation (%)</p>', unsafe_allow_html=True)
    df_mon_melt = df_mon.melt(id_vars='Annee', value_vars=['Taux_Directeur', 'Inflation'],
                              var_name='variable', value_name='value')
    df_mon_melt['variable'] = df_mon_melt['variable'].replace(
        {'Taux_Directeur': 'taux_directeur', 'Inflation': 'inflation'})

    fig = px.line(df_mon_melt, x='Annee', y='value', color='variable',
        color_discrete_map={'taux_directeur': '#2E8B70', 'inflation': '#F08050'},
        labels={'value': 'value', 'Annee': 'annee', 'variable': 'variable'})
    fig.update_traces(line=dict(width=2.5))
    fig.update_layout(height=400, plot_bgcolor='white', paper_bgcolor='white',
        legend=dict(orientation="v", x=1.02, y=1, title="variable"),
        yaxis=dict(gridcolor='#EEEEEE'))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<p class="graph-title">🏦 Crédits bancaires / PIB (%)</p>', unsafe_allow_html=True)
    fig = px.bar(df_mon, x='Annee', y='Credits_PIB',
        labels={'Credits_PIB': 'credits_pib', 'Annee': 'annee'})
    fig.update_traces(marker_color='#2E8B70')
    fig.update_layout(height=400, plot_bgcolor='white', paper_bgcolor='white',
        yaxis=dict(gridcolor='#EEEEEE'))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================
# FOOTER
# ============================================

st.markdown("""
    <div class="footer">
        Dashboard réalisé avec Streamlit et Plotly<br>
        Sources : Haut-Commissariat au Plan (HCP), Bank Al-Maghrib, Ministère des Finances du Maroc<br>
        Dernière mise à jour : 2026
    </div>
""", unsafe_allow_html=True)