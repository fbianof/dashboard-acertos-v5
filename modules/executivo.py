import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

def mostrar_executivo(df, df_ideb):


    # ==================================================
    # VALIDAÇÕES
    # ==================================================

    if df is None or len(df) == 0:
        st.warning("Nenhum dado encontrado.")
        return

    st.header("📈 EXECUTIVO")

    # ==================================================
    # INDICADORES
    # ==================================================

    total_escolas = df["Escola"].nunique()
    total_turmas = df["Turma"].nunique()
    total_alunos = len(df)

    media_geral = df["Acertos"].mean()

    perc_meta = (
        (df["Acertos"] >= 13).sum()
        / len(df)
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
        "🏫 Escolas",
        total_escolas
    )

    c2.metric(
        "👨‍🏫 Turmas",
        total_turmas
    )

    c3.metric(
        "👨‍🎓 Alunos",
        f"{total_alunos:,}".replace(",", ".")
    )

    # ==================================================
    # KPIs LINHA 2
    # ==================================================

    c4, c5, c6 = st.columns(3)

    c4.metric(
        "📊 Média Geral",
        f"{media_geral:.2f}"
    )

    c5.metric(
        "🎯 % Meta",
        f"{perc_meta:.1f}%"
    )

    c6.metric(
        "📚 Média IDEB",
        "-"
        if media_ideb is None
        else f"{media_ideb:.2f}"
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
            color_continuous_scale=cores
        )

        fig_top.add_scatter(
            x=top10["Acertos"] + 0.15,
            y=top10["Escola"],
            mode="text",
            text=[
                f"{v:.2f}"
                for v in top10["Acertos"]
            ],
            textfont=dict(
                size=14,
                color="black"
            ),
            showlegend=False
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
            color_continuous_scale=cores
        )

        fig_bottom.add_scatter(
            x=bottom10["Acertos"] + 0.15,
            y=bottom10["Escola"],
            mode="text",
            text=[
                f"{v:.2f}"
                for v in bottom10["Acertos"]
            ],
            textfont=dict(
                size=14,
                color="black"
            ),
            showlegend=False
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
        .round(0)
        .astype(int)
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

    st.dataframe(
        ranking_df,
        use_container_width=True,
        hide_index=True,
        height=450
    )
    st.divider()

    # ==================================================
    # INSIGHTS IA
    # ==================================================

    st.subheader("🤖 Insights IA")

    col1, col2 = st.columns(2)

    with col1:

        st.success("Pontos Positivos")

        st.markdown(f"""
    ```
    
    ✅ Melhor escola da rede: **{melhor_escola}**
    
    ✅ {perc_meta:.1f}% dos alunos atingiram a meta
    
    ✅ Rede possui **{total_escolas} escolas analisadas**
    
    ✅ Média geral de **{media_geral:.2f} Média**
    
    ✅ Ranking consolidado para tomada de decisão
    """)


    with col2:

        diferenca = (
            ranking_escolas.max()
            - ranking_escolas.min()
        )

        st.error("Pontos de Atenção")

        st.markdown(f"""
    ```
    
    ⚠️ Escola crítica: **{pior_escola}**
    
    ⚠️ {100 - perc_meta:.1f}% dos alunos não atingiram a meta
    
    ⚠️ Diferença entre melhor e pior escola: **{diferenca:.2f}**
    
    ⚠️ Necessidade de acompanhamento pedagógico
    
    ⚠️ Possível desigualdade de desempenho
    """)


    st.divider()

    # ==================================================
    # RELATÓRIO EXECUTIVO
    # ==================================================

    st.subheader("📄 Relatório Executivo")

    if st.button(
        "🤖 Gerar Relatório Executivo",
        key="relatorio_executivo"
    ):

        relatorio = f"""
    ```
    
    A rede analisada possui {total_escolas} escolas,
    {total_turmas} turmas e {total_alunos} alunos.
    
    A média geral foi de {media_geral:.2f} Média.
    
    A escola destaque da rede foi {melhor_escola}.
    
    A unidade que requer maior atenção é {pior_escola}.
    
    O percentual de alunos que atingiram a meta foi de
    {perc_meta:.1f}%.
    """


        st.text_area(
            "Relatório Gerado",
            relatorio,
            height=250
        )

    st.divider()

    # ==================================================
    # EXPORTAÇÃO
    # ==================================================

    st.subheader("📥 Exportações")

    buffer = BytesIO()

    ranking_df.to_excel(
        buffer,
        index=False
    )

    st.download_button(
        label="📥 Exportar Ranking Geral",
        data=buffer.getvalue(),
        file_name="ranking_escolas.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

