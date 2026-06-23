import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

def mostrar_alunos(df):

    # ==================================================
    # VALIDAÇÃO
    # ==================================================

    if df is None or len(df) == 0:
        st.warning("Nenhum dado encontrado.")
        return

    # ==================================================
    # CABEÇALHO
    # ==================================================

    st.header("👨‍🎓 ALUNOS")

    # ==================================================
    # FILTRO DE ESCOLA
    # ==================================================

    escolas_df = (
        df.groupby("Escola")
        .agg(
            Qtde_Turmas=("Turma", "nunique"),
            Qtde_Alunos=("Aluno", "count")
        )
        .reset_index()
        .sort_values("Escola")
    )

    opcoes_escolas = {
        "🏫 Todas as Escolas": "TODAS"
    }

    for _, row in escolas_df.iterrows():
        texto = (
            f"{row['Escola']} | "
            f"Turmas: {row['Qtde_Turmas']} | "
            f"Alunos: {row['Qtde_Alunos']}"
        )

        opcoes_escolas[texto] = row["Escola"]

    escola_exibicao = st.selectbox(
        "🏫 Filtrar Escola",
        list(opcoes_escolas.keys()),
        key="filtro_alunos_escola"
    )

    escola_selecionada = (
        opcoes_escolas[escola_exibicao]
    )

    # ==================================================
    # FILTRO
    # ==================================================

    if escola_selecionada == "TODAS":

        df_filtrado = df.copy()

    else:

        df_filtrado = df[
            df["Escola"] == escola_selecionada
            ].copy()

    # ==================================================
    # INDICADORES
    # ==================================================

    total_alunos = len(df_filtrado)

    media_geral = (
        df_filtrado["Acertos"]
        .mean()
    )

    melhor_aluno = (
        df_filtrado
        .sort_values(
            "Acertos",
            ascending=False
        )
        .iloc[0]
    )

    pior_aluno = (
        df_filtrado
        .sort_values(
            "Acertos",
            ascending=True
        )
        .iloc[0]
    )

    perc_meta = (
            (
                    df_filtrado["Acertos"] >= 13
            ).mean() * 100
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "👨‍🎓 Alunos",
        total_alunos
    )

    c2.metric(
        "📊 Média Geral",
        f"{media_geral:.2f}"
    )

    c3.metric(
        "🏆 Melhor Nota",
        melhor_aluno["Acertos"]
    )

    c4.metric(
        "🎯 % Meta",
        f"{perc_meta:.1f}%"
    )

    if escola_selecionada == "TODAS":

        st.info(
            f"🏆 Melhor aluno da rede: {melhor_aluno['Aluno']}"
        )

        st.warning(
            f"⚠️ Aluno que requer atenção: {pior_aluno['Aluno']}"
        )

    else:

        st.info(
            f"🏆 Melhor aluno da escola: {melhor_aluno['Aluno']}"
        )

        st.warning(
            f"⚠️ Aluno que requer atenção: {pior_aluno['Aluno']}"
        )

    st.divider()

    # ==================================================
    # RANKING ANALÍTICO DOS ALUNOS
    # ==================================================

    st.subheader("🏅 Ranking Analítico dos Alunos")

    # ==================================================
    # LIMPEZA DOS DADOS
    # ==================================================

    base_alunos = df_filtrado.copy()

    base_alunos["Aluno"] = (
        base_alunos["Aluno"]
        .astype(str)
        .str.strip()
    )

    base_alunos = base_alunos[
        base_alunos["Aluno"].notna()
    ]

    base_alunos = base_alunos[
        base_alunos["Aluno"] != ""
        ]

    base_alunos = base_alunos[
        base_alunos["Aluno"] != "nan"
        ]

    # ==================================================
    # CLASSIFICAÇÃO
    # ==================================================

    def classificar_aluno(acertos):

        if acertos >= 16:
            return "🟢 Excelente"

        elif acertos >= 13:
            return "🔵 Bom"

        elif acertos >= 10:
            return "🟠 Atenção"

        else:
            return "🔴 Crítico"

    # ==================================================
    # DADOS
    # ==================================================

    ranking_alunos = (
        base_alunos[
            [
                "Escola",
                "Turma",
                "Aluno",
                "Acertos"
            ]
        ]
        .copy()
    )

    # Remove linhas vazias

    ranking_alunos["Escola"] = (
        ranking_alunos["Escola"]
        .astype(str)
        .str.strip()
    )

    ranking_alunos["Turma"] = (
        ranking_alunos["Turma"]
        .astype(str)
        .str.strip()
    )

    ranking_alunos["Aluno"] = (
        ranking_alunos["Aluno"]
        .astype(str)
        .str.strip()
    )

    ranking_alunos = ranking_alunos[
        ranking_alunos["Aluno"].notna()
    ]

    ranking_alunos = ranking_alunos[
        ranking_alunos["Aluno"] != ""
        ]

    ranking_alunos = ranking_alunos[
        ranking_alunos["Aluno"] != "nan"
        ]

    ranking_alunos = ranking_alunos[
        ranking_alunos["Escola"] != ""
        ]

    ranking_alunos = ranking_alunos[
        ranking_alunos["Turma"] != ""
        ]

    # Remove registros sem acertos

    ranking_alunos = ranking_alunos.dropna(
        subset=["Acertos"]
    )

    # ==================================================
    # CLASSIFICAÇÃO
    # ==================================================

    ranking_alunos["Classificação"] = (
        ranking_alunos["Acertos"]
        .apply(classificar_aluno)
    )

    ranking_alunos = ranking_alunos.sort_values(
        "Acertos",
        ascending=False
    )

    ranking_alunos.insert(
        0,
        "Posição",
        range(
            1,
            len(ranking_alunos) + 1
        )
    )

    ranking_alunos["Acertos"] = (
        ranking_alunos["Acertos"]
        .round(0)
        .astype(int)
    )

    # ==================================================
    # ORDEM DAS COLUNAS
    # ==================================================

    ranking_alunos = ranking_alunos[
        [
            "Posição",
            "Escola",
            "Turma",
            "Aluno",
            "Acertos",
            "Classificação"
        ]
    ]

    st.dataframe(
        ranking_alunos,
        use_container_width=True,
        hide_index=True,
        height=500
    )

    st.divider()



    # ==================================================
    # RESUMO DAS CLASSIFICAÇÕES
    # ==================================================

    qtde_excelente = (
        ranking_alunos["Classificação"]
        .str.contains("Excelente")
        .sum()
    )

    qtde_bom = (
        ranking_alunos["Classificação"]
        .str.contains("Bom")
        .sum()
    )

    qtde_atencao = (
        ranking_alunos["Classificação"]
        .str.contains("Atenção")
        .sum()
    )

    qtde_critico = (
        ranking_alunos["Classificação"]
        .str.contains("Crítico")
        .sum()
    )

    total_alunos_ranking = len(
        ranking_alunos
    )

    perc_excelente = (
            qtde_excelente
            / total_alunos_ranking
            * 100
    )

    perc_bom = (
            qtde_bom
            / total_alunos_ranking
            * 100
    )

    perc_atencao = (
            qtde_atencao
            / total_alunos_ranking
            * 100
    )

    perc_critico = (
            qtde_critico
            / total_alunos_ranking
            * 100
    )

    st.markdown(
        "### 📊 Resumo das Classificações"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.success(
            f"""
    🟢 EXCELENTE

    👨‍🎓 {qtde_excelente} alunos

    📈 {perc_excelente:.1f}%
    """
        )

    with c2:

        st.info(
            f"""
    🔵 BOM

    👨‍🎓 {qtde_bom} alunos

    📈 {perc_bom:.1f}%
    """
        )

    with c3:

        st.warning(
            f"""
    🟠 ATENÇÃO

    👨‍🎓 {qtde_atencao} alunos

    📈 {perc_atencao:.1f}%
    """
        )

    with c4:

        st.error(
            f"""
    🔴 CRÍTICO

    👨‍🎓 {qtde_critico} alunos

    📈 {perc_critico:.1f}%
    """
        )

    st.divider()

    # ==================================================
    # DISTRIBUIÇÃO DOS ALUNOS
    # ==================================================

    st.subheader("📊 Distribuição dos Alunos")

    dist_alunos = (
        ranking_alunos
        .groupby("Classificação")
        .size()
        .reset_index(name="Quantidade")
    )

    ordem = [
        "🟢 Excelente",
        "🔵 Bom",
        "🟠 Atenção",
        "🔴 Crítico"
    ]

    dist_alunos["Classificação"] = pd.Categorical(
        dist_alunos["Classificação"],
        categories=ordem,
        ordered=True
    )

    dist_alunos = dist_alunos.sort_values(
        "Classificação"
    )

    tipo_dist = st.selectbox(
        "Tipo de gráfico",
        [
            "Pizza",
            "Rosca",
            "Barras",
            "Área"
        ],
        key="grafico_distribuicao_alunos"
    )

    cores_dist = {
        "🟢 Excelente": "#22C55E",
        "🔵 Bom": "#3B82F6",
        "🟠 Atenção": "#F59E0B",
        "🔴 Crítico": "#EF4444"
    }

    # ==================================================
    # PIZZA
    # ==================================================

    if tipo_dist == "Pizza":

        fig_dist = px.pie(
            dist_alunos,
            names="Classificação",
            values="Quantidade",
            color="Classificação",
            color_discrete_map=cores_dist
        )

        fig_dist.update_traces(
            textinfo="percent+label+value"
        )

    # ==================================================
    # ROSCA
    # ==================================================

    elif tipo_dist == "Rosca":

        fig_dist = px.pie(
            dist_alunos,
            names="Classificação",
            values="Quantidade",
            hole=0.45,
            color="Classificação",
            color_discrete_map=cores_dist
        )

        fig_dist.update_traces(
            textinfo="percent+label+value"
        )

    # ==================================================
    # BARRAS
    # ==================================================

    elif tipo_dist == "Barras":

        fig_dist = px.bar(
            dist_alunos,
            x="Classificação",
            y="Quantidade",
            text="Quantidade",
            color="Classificação",
            color_discrete_map=cores_dist
        )

        fig_dist.update_traces(
            textposition="outside"
        )

    # ==================================================
    # ÁREA
    # ==================================================

    else:

        fig_dist = px.area(
            dist_alunos,
            x="Classificação",
            y="Quantidade",
            color="Classificação",
            color_discrete_map=cores_dist
        )

        fig_dist.add_scatter(
            x=dist_alunos["Classificação"],
            y=dist_alunos["Quantidade"],
            mode="markers+text",
            text=dist_alunos["Quantidade"],
            textposition="top center",
            showlegend=False
        )

    fig_dist.update_layout(
        height=550,
        legend_title="Classificação"
    )

    st.plotly_chart(
        fig_dist,
        use_container_width=True
    )

    # ==================================================
    # LEGENDA
    # ==================================================

    st.info("""
    ### 📖 Critérios de Classificação dos Alunos

    🟢 Excelente → 16 ou mais acertos

    🔵 Bom → 13 a 15 acertos

    🟠 Atenção → 10 a 12 acertos

    🔴 Crítico → abaixo de 10 acertos

    A distribuição permite identificar rapidamente a concentração dos alunos por faixa de desempenho e orientar ações pedagógicas.
    """)

    st.divider()

    # ==================================================
    # ALUNOS DESTAQUE E ALUNOS EM ATENÇÃO
    # ==================================================

    st.subheader(
        "🏆 Alunos Destaque e ⚠️ Alunos que Requerem Atenção"
    )

    qtde_top = st.selectbox(
        "Quantidade de alunos",
        [5, 10, 20, 30, 40, 50, 100],
        index=1,
        key="qtde_top_alunos"
    )

    # ==================================================
    # DADOS
    # ==================================================

    top_alunos = (
        ranking_alunos
        .sort_values(
            "Acertos",
            ascending=False
        )
        .head(qtde_top)
        .copy()
    )

    bottom_alunos = (
        ranking_alunos
        .sort_values(
            "Acertos",
            ascending=True
        )
        .head(qtde_top)
        .copy()
    )

    col1, col2 = st.columns(2)

    # ==================================================
    # MELHORES ALUNOS
    # ==================================================

    with col1:

        st.success(
            f"🏆 Top {qtde_top} Alunos"
        )

        fig_top = px.bar(
            top_alunos,
            x="Acertos",
            y="Aluno",
            orientation="h",
            text="Acertos",
            color="Acertos",
            color_continuous_scale="Greens"
        )

        fig_top.update_traces(
            texttemplate="%{x}",
            textposition="outside",
            cliponaxis=False
        )

        fig_top.update_layout(
            height=500,
            coloraxis_showscale=False,
            yaxis=dict(
                autorange="reversed"
            )
        )

        st.plotly_chart(
            fig_top,
            use_container_width=True
        )

    # ==================================================
    # ALUNOS EM ATENÇÃO
    # ==================================================

    with col2:

        st.error(
            f"⚠️ Top {qtde_top} Alunos que Requerem Atenção"
        )

        fig_bottom = px.bar(
            bottom_alunos,
            x="Acertos",
            y="Aluno",
            orientation="h",
            text="Acertos",
            color="Acertos",
            color_continuous_scale="Reds"
        )

        fig_bottom.update_traces(
            texttemplate="%{x}",
            textposition="outside",
            cliponaxis=False
        )

        fig_bottom.update_layout(
            height=500,
            coloraxis_showscale=False,
            yaxis=dict(
                autorange="reversed"
            )
        )

        st.plotly_chart(
            fig_bottom,
            use_container_width=True
        )



    st.divider()


    st.divider()