import streamlit as st
import pandas as pd
import plotly.express as px


def mostrar_turmas(df):
    # ==================================================
    # CABEÇALHO
    # ==================================================

    st.header("👨‍🏫 TURMAS")

    # ==================================================
    # VALIDAÇÃO
    # ==================================================

    if df is None or len(df) == 0:
        st.warning("Nenhum dado encontrado.")
        return

    # ==================================================
    # FILTRO DE ESCOLA
    # ==================================================

    escolas_df = (
        df.groupby("Escola")
        .agg(
            Qtde_Turmas=("Turma", "nunique")
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
            f"Turmas: {row['Qtde_Turmas']}"
        )

        opcoes_escolas[texto] = row["Escola"]

    escola_exibicao = st.selectbox(
        "🏫 Filtrar Escola",
        list(opcoes_escolas.keys())
    )

    escola_selecionada = (
        opcoes_escolas[
            escola_exibicao
        ]
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
    # DADOS DAS TURMAS
    # ==================================================

    ranking_turmas = (
        df_filtrado
        .groupby("Turma")
        .agg(
            Qtde_Alunos=("Aluno", "count"),
            Média=("Acertos", "mean")
        )
        .reset_index()
    )

    ranking_turmas["Média"] = (
        ranking_turmas["Média"]
        .round(2)
    )

    ranking_turmas = ranking_turmas.sort_values(
        "Média",
        ascending=False
    )


    # ==================================================
    # KPIs
    # ==================================================

    total_turmas = len(ranking_turmas)

    total_alunos = (
        ranking_turmas["Qtde_Alunos"]
        .sum()
    )

    media_geral = (
        ranking_turmas["Média"]
        .mean()
    )

    melhor_turma = (
        ranking_turmas.iloc[0]["Turma"]
    )

    pior_turma = (
        ranking_turmas.iloc[-1]["Turma"]
    )

    nota_melhor = (
        ranking_turmas.iloc[0]["Média"]
    )

    nota_pior = (
        ranking_turmas.iloc[-1]["Média"]
    )

    perc_acima_media = (
        (
            ranking_turmas["Média"]
            > media_geral
        ).mean() * 100
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "👨‍🏫 Total de Turmas",
        total_turmas,
        help="Quantidade total de turmas consideradas nos filtros aplicados."
    )

    c2.metric(
        "🎓 Total de Alunos",
        total_alunos,
        help="Quantidade total de alunos pertencentes às turmas selecionadas."
    )

    c3.metric(
        "📊 Média Geral",
        f"{media_geral:.2f}",
        help="Média de acertos dos alunos das turmas selecionadas."
    )

    c4, c5, c6 = st.columns(3)

    c4.metric(
        "🏆 Nota da Melhor Turma",
        f"{nota_melhor:.2f}",
        help="Maior média de acertos obtida entre as turmas selecionadas."
    )

    c5.metric(
        "⚠️ Nota da Turma Crítica",
        f"{nota_pior:.2f}",
        help="Menor média de acertos obtida entre as turmas selecionadas."
    )

    c6.metric(
        "🎯 % Acima da Média",
        f"{perc_acima_media:.1f}%",
        help="Percentual de turmas com média superior à média geral das turmas selecionadas."
    )

    st.info(
        f"🏆 Melhor Turma da Escola: {melhor_turma} ({escola_selecionada})"
    )

    st.warning(
        f"⚠️ Turma que requer maior atenção: {pior_turma} ({escola_selecionada})"
    )

    st.divider()

    # ==================================================
    # GRÁFICO PRINCIPAL
    # ==================================================

    st.subheader("📊 Ranking das Turmas")

    paleta = st.selectbox(
        "🎨 Paleta de Cores",
        [
            "Colorido",
            "Escala Azul",
            "Escala Verde",
            "Escala Vermelha",
            "Escala Laranja"
        ],
        key="paleta_ranking_turmas"
    )

    if paleta == "Colorido":
        cores = px.colors.qualitative.Bold

    elif paleta == "Escala Azul":
        cores = px.colors.sequential.Blues

    elif paleta == "Escala Verde":
        cores = px.colors.sequential.Greens

    elif paleta == "Escala Vermelha":
        cores = px.colors.sequential.Reds

    else:
        cores = px.colors.sequential.Oranges

    tipo = st.selectbox(
        "Tipo de gráfico",
        [
            "Barras Horizontais",
            "Barras Verticais",
            "Linha",
            "Área",
            "Pizza",
            "Rosca"
        ],
        key="tipo_grafico_turmas"
    )

    if tipo == "Barras Horizontais":

        fig = px.bar(
            ranking_turmas,
            x="Média",
            y="Turma",
            orientation="h",
            text="Média",
            color="Média",
            color_continuous_scale=cores
        )

        fig.update_traces(
            texttemplate="%{x:.2f}",
            textposition="outside"
        )

    elif tipo == "Barras Verticais":

        fig = px.bar(
            ranking_turmas,
            x="Turma",
            y="Média",
            text="Média",
            color="Média",
            color_continuous_scale=cores
        )

        fig.update_traces(
            texttemplate="%{y:.2f}",
            textposition="outside"
        )

    elif tipo == "Linha":

        aux = ranking_turmas.copy()

        aux["Posição"] = range(
            1,
            len(aux) + 1
        )

        fig = px.line(
            aux,
            x="Posição",
            y="Média",
            markers=True
        )

        fig.add_scatter(
            x=aux["Posição"],
            y=aux["Média"],
            mode="markers+text",
            text=[
                f"{v:.2f}"
                for v in aux["Média"]
            ],
            textposition="top center",
            showlegend=False
        )

    else:

        if tipo == "Pizza":

            fig = px.pie(
                ranking_turmas,
                names="Turma",
                values="Média",
                color="Turma"
            )

            fig.update_traces(
                textinfo="percent+label+value"
            )

        elif tipo == "Rosca":

            fig = px.pie(
                ranking_turmas,
                names="Turma",
                values="Média",
                hole=0.45,
                color="Turma"
            )

            fig.update_traces(
                textinfo="percent+label+value"
            )

        else:

            aux = ranking_turmas.copy()

            aux["Posição"] = range(
                1,
                len(aux) + 1
            )

            fig = px.area(
                aux,
                x="Posição",
                y="Média"
            )

            fig.add_scatter(
                x=aux["Posição"],
                y=aux["Média"],
                mode="markers+text",
                text=[
                    f"{v:.2f}"
                    for v in aux["Média"]
                ],
                textposition="top center",
                showlegend=False
            )

    fig.update_layout(
        height=700,
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()


    # ==================================================
    # RANKING ANALÍTICO DAS TURMAS
    # ==================================================

    st.subheader("📋 Ranking Analítico das Turmas")

    # ==================================================
    # LIMPEZA DOS DADOS
    # ==================================================

    base_analitica = df_filtrado.copy()

    base_analitica["Turma"] = (
        base_analitica["Turma"]
        .astype(str)
        .str.strip()
    )

    base_analitica = base_analitica[
        base_analitica["Turma"].notna()
    ]

    base_analitica = base_analitica[
        base_analitica["Turma"] != ""
        ]

    base_analitica = base_analitica[
        base_analitica["Turma"] != "nan"
        ]

    # ==================================================
    # AGRUPAMENTO
    # ==================================================

    ranking_analitico = (
        base_analitica
        .groupby(
            [
                "Escola",
                "Turma"
            ]
        )
        .agg(
            Qtde_Alunos=("Aluno", "count"),
            Acertos=("Acertos", "sum"),
            Média=("Acertos", "mean")
        )
        .reset_index()
    )

    ranking_analitico["Média"] = (
        ranking_analitico["Média"]
        .round(2)
    )

    # ==================================================
    # CLASSIFICAÇÃO
    # ==================================================

    def classificar(media):

        if media >= 16:
            return "🟢 Excelente"

        elif media >= 13:
            return "🔵 Bom"

        elif media >= 10:
            return "🟠 Atenção"

        else:
            return "🔴 Crítico"

    ranking_analitico["Classificação"] = (
        ranking_analitico["Média"]
        .apply(classificar)
    )

    # ==================================================
    # ORDENAÇÃO
    # ==================================================

    ranking_analitico = ranking_analitico.sort_values(
        "Média",
        ascending=False
    )

    ranking_analitico.insert(
        0,
        "Posição",
        range(
            1,
            len(ranking_analitico) + 1
        )
    )

    ranking_analitico["Acertos"] = (
        ranking_analitico["Acertos"]
        .astype(int)
    )

    # ==================================================
    # ORGANIZAÇÃO DAS COLUNAS
    # ==================================================

    ranking_analitico = ranking_analitico[
        [
            "Posição",
            "Escola",
            "Turma",
            "Qtde_Alunos",
            "Acertos",
            "Média",
            "Classificação"
        ]
    ]

    ranking_analitico.columns = [
        "Posição",
        "Escola",
        "Turma",
        "Qtde Alunos",
        "Acertos",
        "Média",
        "Classificação"
    ]

    # ==================================================
    # TABELA
    # ==================================================

    st.caption(
        f"Total de turmas analisadas: {len(ranking_analitico)}"
    )

    st.dataframe(
        ranking_analitico,
        use_container_width=True,
        hide_index=True,
        height=min(
            (len(ranking_analitico) * 35) + 40,
            2000
        )
    )

    st.divider()

    # ==================================================
    # LEGENDA EXPLICATIVA
    # ==================================================

    st.info("""
        ### 📖 Como interpretar a classificação

        🟢 **Excelente** → Média maior ou igual a 16 acertos

        🔵 **Bom** → Média entre 13 e 15,99 acertos

        🟠 **Atenção** → Média entre 10 e 12,99 acertos

        🔴 **Crítico** → Média abaixo de 10 acertos

        A classificação permite identificar rapidamente quais turmas apresentam melhor desempenho e quais necessitam de acompanhamento pedagógico prioritário.
        """)

    st.divider()

    # ==================================================
    # DISTRIBUIÇÃO DAS TURMAS
    # ==================================================

    st.subheader("📊 Distribuição das Turmas")

    # ==================================================
    # CLASSIFICAÇÃO
    # ==================================================

    dist_turmas = (
        df_filtrado
        .groupby("Turma")["Acertos"]
        .mean()
        .reset_index(name="Média")
    )

    dist_turmas["Categoria"] = (
        dist_turmas["Média"]
        .apply(classificar)
    )


    # ==================================================
    # AGRUPAMENTO
    # ==================================================

    dist_graf = (
        dist_turmas
        .groupby("Categoria")
        .size()
        .reset_index(name="Quantidade")
    )

    # ==================================================
    # ORDEM DAS CATEGORIAS
    # ==================================================

    ordem = [
        "🟢 Excelente",
        "🔵 Bom",
        "🟠 Atenção",
        "🔴 Crítico"
    ]

    dist_graf["Categoria"] = pd.Categorical(
        dist_graf["Categoria"],
        categories=ordem,
        ordered=True
    )

    dist_graf = dist_graf.sort_values(
        "Categoria"
    )

    # ==================================================
    # ESCOLHA DO GRÁFICO
    # ==================================================

    tipo_dist = st.selectbox(
        "Tipo de gráfico",
        [
            "Pizza",
            "Rosca",
            "Barras",
            "Área"
        ],
        key="grafico_distribuicao_turmas"
    )

    # ==================================================
    # CORES
    # ==================================================

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
            dist_graf,
            names="Categoria",
            values="Quantidade",
            color="Categoria",
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
            dist_graf,
            names="Categoria",
            values="Quantidade",
            hole=0.45,
            color="Categoria",
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
            dist_graf,
            x="Categoria",
            y="Quantidade",
            text="Quantidade",
            color="Categoria",
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
            dist_graf,
            x="Categoria",
            y="Quantidade",
            color="Categoria",
            color_discrete_map=cores_dist
        )

        fig_dist.add_scatter(
            x=dist_graf["Categoria"],
            y=dist_graf["Quantidade"],
            mode="markers+text",
            text=dist_graf["Quantidade"],
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


    st.divider()

    # ==================================================
    # TURMAS DESTAQUE E TURMAS EM ATENÇÃO
    # ==================================================

    st.subheader(
        "🏆 Turmas Destaque e ⚠️ Turmas que Requerem Atenção"
    )

    qtde_top = st.selectbox(
        "Quantidade de turmas",
        [5, 10, 15, 20],
        index=1,
        key="qtde_top_turmas"
    )

    ranking_turmas_top = (
        df_filtrado
        .groupby("Turma")["Acertos"]
        .mean()
        .sort_values(ascending=False)
        .reset_index(name="Média")
    )

    ranking_turmas_top["Média"] = (
        ranking_turmas_top["Média"]
        .round(2)
    )

    # ==================================================
    # TOP TURMAS
    # ==================================================

    top_turmas = (
        ranking_turmas_top
        .head(qtde_top)
        .sort_values(
            "Média",
            ascending=False
        )
        .copy()
    )

    # ==================================================
    # TURMAS EM ATENÇÃO
    # ==================================================

    bottom_turmas = (
        ranking_turmas_top
        .tail(qtde_top)
        .sort_values(
            "Média",
            ascending=True
        )
        .copy()
    )

    col1, col2 = st.columns(2)

    # ==================================================
    # MELHORES TURMAS
    # ==================================================

    with col1:

        st.success(
            f"🏆 Top {qtde_top} Turmas"
        )

        fig_top = px.bar(
            top_turmas,
            x="Média",
            y="Turma",
            orientation="h",
            text="Média",
            color="Média",
            color_continuous_scale="Greens"
        )

        fig_top.update_traces(
            texttemplate="%{x:.2f}",
            textposition="outside",
            cliponaxis=False
        )

        fig_top.update_yaxes(
            categoryorder="array",
            categoryarray=top_turmas["Turma"][::-1]
        )

        fig_top.update_layout(
            height=500,
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig_top,
            use_container_width=True
        )

    # ==================================================
    # TURMAS EM ATENÇÃO
    # ==================================================

    with col2:

        st.error(
            f"⚠️ {qtde_top} Turmas que Requerem Atenção"
        )

        fig_bottom = px.bar(
            bottom_turmas,
            x="Média",
            y="Turma",
            orientation="h",
            text="Média",
            color="Média",
            color_continuous_scale="Reds"
        )

        fig_bottom.update_traces(
            texttemplate="%{x:.2f}",
            textposition="outside",
            cliponaxis=False
        )

        fig_bottom.update_yaxes(
            categoryorder="array",
            categoryarray=bottom_turmas["Turma"][::-1]
        )

        fig_bottom.update_layout(
            height=500,
            coloraxis_showscale=False
        )

        st.plotly_chart(
            fig_bottom,
            use_container_width=True
        )
    st.divider()
