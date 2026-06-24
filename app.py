import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

from modules.executivo import mostrar_executivo
from modules.escolas import mostrar_escolas
from modules.turmas import mostrar_turmas
from modules.alunos import mostrar_alunos
from modules.notas import mostrar_notas
from modules.metas import mostrar_metas
from modules.ideb import mostrar_ideb

# ==================================================
# CONFIGURAÇÃO
# ==================================================

st.set_page_config(
    page_title="Dashboard Semecel Rondonópolis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>

/* ==================================================
   LAYOUT GERAL
================================================== */

.block-container {
    padding-top: 0.9rem;
    padding-bottom: 1rem;
}

/* ==================================================
   SIDEBAR
================================================== */

section[data-testid="stSidebar"] {
    width: 320px !important;
}

[data-testid="stSidebar"] {
    border-right: 1px solid rgba(128,128,128,0.15);
}

/* Remove espaço superior da sidebar */
[data-testid="stSidebar"] > div:first-child {
    padding-top: 0rem !important;
    margin-top: -10px !important;
}

[data-testid="stSidebarHeader"] {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
    min-height: 0 !important;
}

[data-testid="stSidebarContent"] {
    padding-top: 0rem !important;
    padding-left: 0.8rem;
    padding-right: 0.8rem;
}

section[data-testid="stSidebar"] .block-container {
    padding-top: 0rem !important;
}

/* ==================================================
   TÍTULO SIDEBAR
================================================== */

.sidebar-title {
    text-align: center;
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 12px;
}

/* ==================================================
   DIVISÓRIAS
================================================== */

hr {
    margin-top: 8px;
    margin-bottom: 8px;
}

/* ==================================================
   OPTION MENU
================================================== */

.nav-link {
    padding-top: 10px !important;
    padding-bottom: 10px !important;
    border-radius: 8px;
}

.nav-link:hover {
    border-radius: 8px;
}

.nav-link.active {
    border-radius: 8px;
}

/* CORREÇÃO DOS ÍCONES */

.nav-link i {
    color: #0D6EFD !important;
}

.nav-link svg {
    color: #0D6EFD !important;
    fill: #0D6EFD !important;
}

.nav-link.active,
.nav-link.active span,
.nav-link.active i,
.nav-link.active svg,
.nav-link.active path {
    color: white !important;
    fill: white !important;
}

/* ==================================================
   FILTROS
================================================== */

div[data-baseweb="select"] {
    font-size: 0.95rem;
}

/* ==================================================
   MULTISELECT - ITENS SELECIONADOS
================================================== */

[data-baseweb="tag"] {
    background-color: #0D6EFD !important;
    border-radius: 6px !important;
}

[data-baseweb="tag"] span {
    color: white !important;
    font-weight: 500;
}

[data-baseweb="tag"] svg {
    color: white !important;
}

[data-baseweb="tag"] svg:hover {
    opacity: 0.8;
}

/* ==================================================
   SCROLLBAR SIDEBAR
================================================== */

[data-testid="stSidebar"] ::-webkit-scrollbar {
    width: 8px;
}

[data-testid="stSidebar"] ::-webkit-scrollbar-thumb {
    background: rgba(128,128,128,0.4);
    border-radius: 10px;
}

[data-testid="stSidebar"] ::-webkit-scrollbar-track {
    background: transparent;
}

/* ==================================================
   KPIs EXECUTIVOS (st.metric)
================================================== */

[data-testid="stMetric"] {
    padding: 18px;
    border-radius: 16px;

    border-left: 6px solid #0D6EFD;

    background: rgba(255,255,255,0.03);

    box-shadow:
        0 2px 8px rgba(0,0,0,0.08),
        0 8px 24px rgba(0,0,0,0.08);

    transition: all 0.25s ease;

    min-height: 125px;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-4px);

    box-shadow:
        0 6px 14px rgba(0,0,0,0.12),
        0 12px 30px rgba(0,0,0,0.15);
}

/* ==================================================
   TÍTULO DOS KPIs
================================================== */

[data-testid="stMetric"] > [data-testid="stMarkdownContainer"] p {
    font-size: 1.15rem !important;
    font-weight: 600 !important;
}

/* ==================================================
   VALORES DOS KPIs
================================================== */

[data-testid="stMetricValue"] p {
    font-size: 2.0rem !important;
    font-weight: 700 !important;
}


/* ==================================================
   MODO ESCURO
================================================== */

[data-theme="dark"] [data-testid="stMetric"] {
    background: rgba(255,255,255,0.02);

    box-shadow:
        0 4px 12px rgba(0,0,0,0.35),
        0 12px 28px rgba(0,0,0,0.25);
}

/* ==================================================
   TABELAS
================================================== */

[data-testid="stDataFrame"] {
    border-radius: 12px;
}

/* ==================================================
   GRÁFICOS
================================================== */

.js-plotly-plot {
    border-radius: 12px;
}

/* ==================================================
   SUBHEADERS
================================================== */

h2, h3 {
    margin-top: 0.3rem !important;
    margin-bottom: 0.8rem !important;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# CARREGAMENTO DOS DADOS
# ==================================================

try:
    df = pd.read_excel("data/Acertos_V7.xlsx")
except Exception:
    st.error("Arquivo data/Acertos_V7.xlsx não encontrado.")
    st.stop()

try:
    df_ideb = pd.read_excel("data/ideb.xlsx")
except Exception:
    df_ideb = None

# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:
    st.markdown(
        '<div class="sidebar-title">📊 DASHBOARD SEMECEL RONDONÓPOLIS</div>',
        unsafe_allow_html=True
    )
    menu = option_menu(
        menu_title=None,
        options=[
            "VISÃO GERAL",
            "ESCOLAS",
            "TURMAS",
            "ALUNOS",
            "NOTAS",
            "METAS",
            "IDEB"
        ],
        icons=[
            "bar-chart",
            "building",
            "people",
            "person",
            "journal-text",
            "bullseye",
            "graph-up"
        ],
        default_index=0,
        styles={
            "container": {
                "padding": "0!important"
            },
            "icon": {
                "color": "#0D6EFD",
                "font-size": "18px"
            },
            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "4px",
                "padding": "10px",
                "--hover-color": "rgba(13,110,253,0.15)"
            },
            "nav-link-selected": {
                "background-color": "#0D6EFD",
                "color": "white"
            }
        }
    )


    st.markdown("### ⚙️ Filtros")

    escolas = sorted(df["Escola"].dropna().unique())

    escolas_selecionadas = st.multiselect(
        "Filtro Executivo / Escolas",
        escolas,
        default=escolas
    )

# ==================================================
# FILTRO GLOBAL
# ==================================================

df_filtrado = df[
    df["Escola"].isin(escolas_selecionadas)
]

# ==================================================
# CONTEÚDO
# ==================================================

if menu == "VISÃO GERAL":

    mostrar_executivo(
        df_filtrado,
        df_ideb
    )

elif menu == "ESCOLAS":

    mostrar_escolas(
        df_filtrado,
        df_ideb
    )

elif menu == "TURMAS":

    mostrar_turmas(
        df_filtrado
    )

elif menu == "ALUNOS":

    mostrar_alunos(
        df_filtrado
    )

elif menu == "NOTAS":

    mostrar_notas(
        df_filtrado
    )

elif menu == "METAS":

    mostrar_metas(
        df_filtrado
    )

elif menu == "IDEB":

    if df_ideb is None:
        st.warning("Planilha IDEB não encontrada.")
    else:
        mostrar_ideb(
            df_ideb
        )