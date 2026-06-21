import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="Dashboard Acertos V5", page_icon="📊", layout="wide")
st.title("📊 Dashboard Acertos V5")

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
        fig = px.bar(rank, x="Acertos", y="Escola", orientation='h', text_auto='.2f', color_discrete_sequence=[cor_tema])
        fig.update_layout(height=max(400, len(rank) * 80), bargap=0.2)
    else:
        fig = px.pie(rank, values="Acertos", names="Escola")
    st.plotly_chart(fig, use_container_width=True)
    c1, c2 = st.columns(2)
    with c1:
        st.write("🏆 Top 10 Escolas"); st.dataframe(rank.head(10), use_container_width=True)
        st.plotly_chart(px.pie(rank.head(10), values="Acertos", names="Escola", title="Top 10"), use_container_width=True)
    with c2:
        st.write("⚠️ Piores 10 Escolas"); st.dataframe(rank.tail(10), use_container_width=True)
        st.plotly_chart(px.pie(rank.tail(10), values="Acertos", names="Escola", title="Bottom 10"), use_container_width=True)

with tab2:
    st.subheader("Ranking: Turmas")
    rank_t = df_filtrado.groupby("Turma")["Acertos"].mean().reset_index().sort_values("Acertos", ascending=False)
    tipo_t = st.radio("Formato Turmas:", ["Colunas", "Rosca"], horizontal=True)
    if tipo_t == "Colunas":
        fig = px.bar(rank_t, x="Turma", y="Acertos", text_auto='.2f', color_discrete_sequence=[cor_tema])
        fig.update_layout(bargap=0.2)
    else:
        fig = px.pie(rank_t, values="Acertos", names="Turma", hole=0.5)
    st.plotly_chart(fig, use_container_width=True)
    c1, c2 = st.columns(2)
    with c1:
        st.write("🏆 Top 10 Turmas"); st.dataframe(rank_t.head(10), use_container_width=True)
        st.plotly_chart(px.pie(rank_t.head(10), values="Acertos", names="Turma", hole=0.5, title="Top 10 (Rosca)"), use_container_width=True)
    with c2:
        st.write("⚠️ Piores 10 Turmas"); st.dataframe(rank_t.tail(10), use_container_width=True)
        st.plotly_chart(px.pie(rank_t.tail(10), values="Acertos", names="Turma", hole=0.5, title="Bottom 10 (Rosca)"), use_container_width=True)

with tab3:
    st.subheader("Alunos por Turma")
    qtd = df_filtrado.groupby("Turma")["Acertos"].count().reset_index().rename(columns={"Acertos": "Total"})
    qtd['Percent'] = (qtd['Total'] / qtd['Total'].sum() * 100).round(1)
    fig_a = px.bar(qtd, x="Turma", y="Total", text=qtd.apply(lambda row: f"{row['Total']} ({row['Percent']}%)", axis=1))
    fig_a.update_layout(bargap=0.2)
    st.plotly_chart(fig_a, use_container_width=True)
    c1, c2 = st.columns(2)
    c1.write("📈 Maiores Turmas"); c1.dataframe(qtd.nlargest(10, 'Total'))
    c2.write("📉 Menores Turmas"); c2.dataframe(qtd.nsmallest(10, 'Total'))

with tab4:
    st.subheader("Distribuição de Acertos")
    notas = df_filtrado['Acertos'].value_counts().reset_index()
    notas.columns = ['Acertos', 'Qtde']
    notas['Percent'] = (notas['Qtde'] / notas['Qtde'].sum() * 100).round(1)
    fig_n = px.bar(notas.sort_values('Acertos'), x='Acertos', y='Qtde', text=notas.apply(lambda row: f"{row['Qtde']} ({row['Percent']}%)", axis=1))
    fig_n.update_layout(bargap=0.2)
    st.plotly_chart(fig_n, use_container_width=True)

with tab5:
    st.subheader("Meta (>= 13)")
    df_filtrado['Status'] = df_filtrado['Acertos'].apply(lambda x: 'Atingiu Meta' if x >= 13 else 'Abaixo da Meta')
    fig = px.pie(df_filtrado, names='Status', title="Proporção de Alunos", hole=0.3)
    st.plotly_chart(fig, use_container_width=True)

st.download_button("📥 Baixar Excel", data=BytesIO(), file_name="acertos_processado.xlsx")