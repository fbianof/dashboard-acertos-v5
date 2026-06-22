import streamlit as st
import pandas as pd

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
    page_title="Dashboard Semecel V7",
    page_icon="📊",
    layout="wide"
)

# ==================================================

# ESTILO GLOBAL

# ==================================================

st.markdown("""

<style>

/* CARDS KPI */
[data-testid="stMetric"]{
    background: #F8FAFC;
    padding: 14px;
    border-radius: 14px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 4px 12px rgba(0,0,0,0.12);
}

/* TÍTULO KPI */
[data-testid="stMetricLabel"]{
    color:#374151;
    font-size:1rem;
    font-weight:600;
}

/* VALOR KPI */
[data-testid="stMetricValue"]{
    color:#111827;
    font-size:2.4rem;
    font-weight:800;
}

/* HOVER */
[data-testid="stMetric"]:hover{
    transform: translateY(-2px);
    transition: 0.2s;
    box-shadow: 0 8px 18px rgba(0,0,0,0.18);
}

</style>

""", unsafe_allow_html=True)


# ==================================================
# CABEÇALHO
# ==================================================

st.title("📊 Dashboard Semecel V7")
st.caption("Sistema de Gestão Educacional, Avaliações e IDEB")

# ==================================================
# CARREGAMENTO DOS DADOS
# ==================================================

try:
    df = pd.read_excel("data/Acertos_V7.xlsx")
except:
    st.error("Arquivo data/Acertos_V7.xlsx não encontrado.")
    st.stop()

try:
    df_ideb = pd.read_excel("data/ideb.xlsx")
except:
    df_ideb = None

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.header("⚙️ Configurações")

cor_tema = st.sidebar.color_picker(
    "Cor padrão dos gráficos",
    "#1f77b4"
)

# ==================================================
# FILTROS GLOBAIS
# ==================================================

escolas = sorted(df["Escola"].dropna().unique())

escolas_selecionadas = st.sidebar.multiselect(
    "🏫 Escolas",
    escolas,
    default=escolas
)

df_filtrado = df[
    df["Escola"].isin(escolas_selecionadas)
]

# ==================================================
# ABAS
# ==================================================

(
    tab_exec,
    tab_escolas,
    tab_turmas,
    tab_alunos,
    tab_notas,
    tab_metas,
    tab_ideb
) = st.tabs([
    "📈 EXECUTIVO",
    "🏫 ESCOLAS",
    "👨‍🏫 TURMAS",
    "👨‍🎓 ALUNOS",
    "📝 NOTAS",
    "🎯 METAS",
    "📚 IDEB"
])

# ==================================================
# EXECUTIVO
# ==================================================

with tab_exec:
    mostrar_executivo(
        df_filtrado,
        df_ideb
    )

# ==================================================
# ESCOLAS
# ==================================================

with tab_escolas:
    mostrar_escolas(
        df_filtrado,
        df_ideb
    )

# ==================================================
# TURMAS
# ==================================================

with tab_turmas:
    mostrar_turmas(
        df_filtrado
    )

# ==================================================
# ALUNOS
# ==================================================

with tab_alunos:
    mostrar_alunos(
        df_filtrado
    )

# ==================================================
# NOTAS
# ==================================================

with tab_notas:
    mostrar_notas(
        df_filtrado
    )

# ==================================================
# METAS
# ==================================================

with tab_metas:
    mostrar_metas(
        df_filtrado
    )

# ==================================================
# IDEB
# ==================================================

with tab_ideb:

    if df_ideb is None:
        st.warning("Planilha IDEB não encontrada.")
    else:
        mostrar_ideb(
            df_ideb
        )