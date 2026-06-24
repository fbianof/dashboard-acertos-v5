import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

from streamlit import caption


def mostrar_executivo(df, df_ideb):
    # ==================================================
    # VALIDAÇÕES
    # ==================================================
    if df is None or len(df) == 0:
        st.warning("Nenhum dado encontrado.")
        return
    st.header("📈 VISÃO GERAL")
    # ==================================================
    # INDICADORES
    # ==================================================

    total_escolas = df["Escola"].nunique()
    total_turmas = df["Turma"].nunique()
    total_alunos = len(df)

    media_geral = df["Acertos"].mean()

    perc_aproveitamento = (
        df["Acertos"].mean() / 18
    ) * 100

    ranking_escolas = (
        df.groupby("Escola")["Acertos"]
        .mean()
        .sort_values(ascending=False)
    )

    melhor_escola = ranking_escolas.index[0]
    pior_escola = ranking_escolas.index[-1]

    media_ideb = None

    if (
        df_ideb is not None
        and "IDEB_Escola" in df_ideb.columns
    ):
        media_ideb = df_ideb["IDEB_Escola"].mean()

    # ==================================================
    # KPIs LINHA 1
    # ==================================================

    c1, c2, c3 = st.columns(3)

    c1.metric(
        label="🏫 Escolas",
        value=total_escolas,
        help="Quantidade total de escolas filtradas."
    )

    c2.metric(
        label="👨‍🏫 Turmas",
        value=total_turmas,
        help="Quantidade total de turmas filtradas para avaliação."
    )

    c3.metric(
        label="🎓 Alunos",
        value=f"{total_alunos:,}".replace(",", "."),
        help="Quantidade total de alunos participantes."
    )

    # ==================================================
    # KPIs LINHA 2
    # ==================================================

    c4, c5, c6 = st.columns(3)

    c4.metric(
        label="📊 Média Geral",
        value=f"{media_geral:.2f}",
        help="Média de acertos considerando todos os alunos."
    )

    c5.metric(
        label="🎯 Aproveitamento Geral",
        value=f"{perc_aproveitamento:.1f}%",
        help="Percentual médio de acertos. Fórmula: (Média de Acertos ÷ 18 questões) × 100."
    )

    c6.metric(
        label="📚 Média IDEB",
        value=f"{media_ideb:.2f}",
        help="Média do IDEB das escolas selecionadas."
    )

    st.info(
        f"🏆 Melhor Escola da Rede: {melhor_escola}"
    )

    st.warning(
        f"⚠️ Escola que requer maior atenção: {pior_escola}"
    )

    st.divider()

    # ==================================================
    # TOP 10 E PIORES 10
    # ==================================================

    st.subheader("📊 Desempenho das Escolas")

    top10 = (
        ranking_escolas
        .head(10)
        .reset_index()
        .sort_values("Acertos")
    )

    bottom10 = (
        ranking_escolas
        .tail(10)
        .reset_index()
    )

    paleta_exec = st.selectbox(
        "Paleta dos gráficos",
        [
            "Colorido",
            "Escala Azul",
            "Escala Verde",
            "Escala Vermelha",
            "Escala Laranja"
        ],
        key="paleta_executivo"
    )

    if paleta_exec == "Colorido":

        cores = px.colors.qualitative.Bold

    elif paleta_exec == "Escala Azul":

        cores = px.colors.sequential.Blues

    elif paleta_exec == "Escala Verde":

        cores = px.colors.sequential.Greens

    elif paleta_exec == "Escala Vermelha":

        cores = px.colors.sequential.Reds

    else:

        cores = px.colors.sequential.Oranges

    col1, col2 = st.columns(2)

    # ==================================================
    # PREPARAÇÃO DOS RÓTULOS
    # ==================================================

    top10 = top10.copy()
    bottom10 = bottom10.copy()

    top10["Rotulo"] = top10["Acertos"].apply(
        lambda x: f"{x:.2f}"
    )

    bottom10["Rotulo"] = bottom10["Acertos"].apply(
        lambda x: f"{x:.2f}"
    )

    # ==================================================
    # TOP 10
    # ==================================================

    with col1:

        st.markdown("### 🏆 Top 10 Escolas")

        fig_top = px.bar(
            top10,
            x="Acertos",
            y="Escola",
            orientation="h",
            color="Acertos",
            color_continuous_scale=cores,
            text="Rotulo"
        )

        fig_top.update_traces(
            textposition="auto",
            textfont=dict(
                size=14,
            )
        )

        fig_top.update_xaxes(
            range=[
                0,
                top10["Acertos"].max() * 1.15
            ]
        )

        fig_top.update_layout(
            height=550,
            font=dict(size=14),
            bargap=0.10,
            coloraxis_showscale=False,
            margin=dict(
                l=10,
                r=120,
                t=30,
                b=10
            )
        )

        st.plotly_chart(
            fig_top,
            use_container_width=True
        )

    # ==================================================
    # PIORES 10
    # ==================================================

    with col2:

        st.markdown("### ⚠️ Piores 10 Escolas")

        fig_bottom = px.bar(
            bottom10,
            x="Acertos",
            y="Escola",
            orientation="h",
            color="Acertos",
            color_continuous_scale=cores,
            text="Rotulo"
        )

        fig_bottom.update_traces(
            textposition="auto",
            textfont=dict(
                size=14,
            )
        )

        fig_bottom.update_xaxes(
            range=[
                0,
                bottom10["Acertos"].max() * 1.15
            ]
        )

        fig_bottom.update_layout(
            height=550,
            font=dict(size=14),
            bargap=0.10,
            coloraxis_showscale=False,
            margin=dict(
                l=10,
                r=120,
                t=30,
                b=10
            )
        )

        st.plotly_chart(
            fig_bottom,
            use_container_width=True
        )


    st.divider()

    # ==================================================
    # RANKING GERAL
    # ==================================================

    st.subheader("🏅 Ranking Geral das Escolas")

    ranking_df = (
        df.groupby("Escola")
        .agg(
            Qtde_Alunos=("Aluno", "count"),
            Acertos=("Acertos", "sum"),
            Média=("Acertos", "mean")
        )
        .reset_index()
    )

    ranking_df = ranking_df.sort_values(
        "Média",
        ascending=False
    )

    ranking_df.insert(
        0,
        "Posição",
        range(
            1,
            len(ranking_df) + 1
        )
    )

    
    ranking_df["Média"] = (
        ranking_df["Média"]
        .round(2)
    )

    # Ordena as colunas corretamente

    ranking_df = ranking_df[
        [
            "Posição",
            "Escola",
            "Qtde_Alunos",
            "Acertos",
            "Média"
        ]
    ]

    # Renomeia apenas para exibição

    ranking_df.columns = [
        "Posição",
        "Escola",
        "Qtde Alunos",
        "Acertos",
        "Média"
    ]

    altura = min(
        3000,
        (len(ranking_df) + 1) * 35
    )

    st.dataframe(
        ranking_df,
        use_container_width=True,
        hide_index=True,
        height=altura
    )

st.divider()

st.divider()
