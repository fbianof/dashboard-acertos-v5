import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="Dashboard Acertos V5", page_icon="📊", layout="wide")
st.title("📊 Dashboard Acertos V5")


# Função de análise IA simplificada
def gerar_analise_ia(df):
    rank = df.groupby("Escola")["Acertos"].mean().sort_values(ascending=False)

    if len(rank) < 2:
        return "Dados insuficientes para uma análise comparativa profunda."

    melhor = rank.index[0]
    pior = rank.index[-1]
    media_geral = df["Acertos"].mean()

    analise = f"""
    ### 🔍 Insights do Desempenho
    Analisando os dados atuais, a escola **{melhor}** destaca-se com o maior índice de aproveitamento, 
    servindo como um modelo de sucesso para as demais. Em contrapartida, a escola **{pior}** apresenta os resultados mais baixos, indicando uma oportunidade prioritária para intervenções 
    pedagógicas ou reforço escolar. 

    Com uma média geral de **{media_geral:.2f}** acertos, nota-se uma variabilidade significativa 
    entre as instituições. Esse cenário sugere que a padronização das estratégias de ensino 
    poderia ajudar a elevar o desempenho das escolas que estão abaixo da média, reduzindo a 
    distância entre os extremos do nosso ranking e promovendo uma educação mais equilibrada.
    """
    return analise


# Upload e Filtros
cor_tema = st.sidebar.color_picker("Cor dos gráficos", "#1f77b4")
arquivo = st.sidebar.file_uploader("Selecione o arquivo Excel", type=["xlsx"])
if arquivo is None:
    st.info("Selecione uma planilha Excel.")
    st.stop()

df = pd.read_excel(arquivo)
df["Escola"] = df["Escola"].astype(str)
df["Turma"] = df["Turma"].astype(str)

escolas = st.sidebar.multiselect("Escola", sorted(df["Escola"].unique()), default=sorted(df["Escola"].unique()))
turmas = st.sidebar.multiselect("Turma", sorted(df["Turma"].unique()), default=sorted(df["Turma"].unique()))
df_filtrado = df[(df["Escola"].isin(escolas)) & (df["Turma"].isin(turmas))]

# Abas
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Escolas", "Turmas", "Alunos", "Notas", "Metas"])

with tab1:
    st.subheader("Ranking: Escolas")
    rank = df_filtrado.groupby("Escola")["Acertos"].mean().reset_index().sort_values("Acertos", ascending=False)
    tipo = st.radio("Formato Escolas:", ["Barras", "Pizza"], horizontal=True)

    if tipo == "Barras":
        fig = px.bar(rank, x="Acertos", y="Escola", orientation='h', text_auto='.2f',
                     color_discrete_sequence=[cor_tema])
        fig.update_layout(height=max(400, len(rank) * 80), bargap=0.2)
    else:
        fig = px.pie(rank, values="Acertos", names="Escola")
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    c1.write("🏆 Top 10 Escolas");
    c1.dataframe(rank.head(10), use_container_width=True)
    c2.write("⚠️ Piores 10 Escolas");
    c2.dataframe(rank.tail(10), use_container_width=True)

    st.markdown("---")
    st.markdown(gerar_analise_ia(df_filtrado))

with tab2:
    st.subheader("Ranking: Turmas")
    rank_t = df_filtrado.groupby("Turma")["Acertos"].mean().reset_index().sort_values("Acertos", ascending=False)
    fig_t = px.bar(rank_t, x="Turma", y="Acertos", text_auto='.2f', color_discrete_sequence=[cor_tema])
    st.plotly_chart(fig_t, use_container_width=True)

with tab3:
    st.subheader("Alunos por Turma")
    qtd = df_filtrado.groupby("Turma")["Acertos"].count().reset_index()
    fig_a = px.bar(qtd, x="Turma", y="Acertos", text_auto=True)
    st.plotly_chart(fig_a, use_container_width=True)

with tab4:
    st.subheader("Distribuição de Acertos")
    fig_n = px.histogram(df_filtrado, x='Acertos', nbins=20, color_discrete_sequence=[cor_tema])
    st.plotly_chart(fig_n, use_container_width=True)

with tab5:
    st.subheader("Meta (>= 13)")
    df_filtrado['Status'] = df_filtrado['Acertos'].apply(lambda x: 'Atingiu Meta' if x >= 13 else 'Abaixo da Meta')
    fig_m = px.pie(df_filtrado, names='Status', hole=0.3)
    st.plotly_chart(fig_m, use_container_width=True)

# Download seguro (usa o motor padrão do pandas)
buffer = BytesIO()
df_filtrado.to_excel(buffer, index=False)
st.download_button("📥 Baixar Excel Filtrado", data=buffer.getvalue(), file_name="acertos_processado.xlsx")