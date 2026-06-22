import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

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
        total_turmas
    )

    c2.metric(
        "🎓 Total de Alunos",
        total_alunos
    )

    c3.metric(
        "📊 Média Geral",
        f"{media_geral:.2f}"
    )

    c4, c5, c6 = st.columns(3)

    c4.metric(
        "🏆 Nota da Melhor Turma",
        f"{nota_melhor:.2f}"
    )

    c5.metric(
        "⚠️ Nota da Turma Crítica",
        f"{nota_pior:.2f}"
    )

    c6.metric(
        "🎯 % Acima da Média",
        f"{perc_acima_media:.1f}%"
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
    # RANKING GERAL DAS TURMAS
    # ==================================================

    st.divider()

    st.subheader("🏅 Ranking Geral das Turmas")

    # Limpeza dos dados

    base_ranking = df_filtrado.copy()

    base_ranking["Turma"] = (
        base_ranking["Turma"]
        .astype(str)
        .str.strip()
    )

    base_ranking = base_ranking[
        base_ranking["Turma"].notna()
    ]

    base_ranking = base_ranking[
        base_ranking["Turma"] != ""
        ]

    base_ranking = base_ranking[
        base_ranking["Turma"] != "nan"
        ]

    # Agrupamento

    ranking_grid = (
        base_ranking
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

    # Ordenação alfabética

    ranking_grid = ranking_grid.sort_values(
        [
            "Escola",
            "Turma"
        ]
    )

    # Posição

    ranking_grid.insert(
        0,
        "Posição",
        range(
            1,
            len(ranking_grid) + 1
        )
    )

    # Formatação

    ranking_grid["Acertos"] = (
        ranking_grid["Acertos"]
        .round(0)
        .astype(int)
    )

    ranking_grid["Média"] = (
        ranking_grid["Média"]
        .round(2)
    )

    # Ordem das colunas

    ranking_grid = ranking_grid[
        [
            "Posição",
            "Escola",
            "Turma",
            "Qtde_Alunos",
            "Acertos",
            "Média"
        ]
    ]

    # Renomeia para exibição

    ranking_grid.columns = [
        "Posição",
        "Escola",
        "Turma",
        "Qtde Alunos",
        "Acertos",
        "Média"
    ]

    # Exibição

    st.dataframe(
        ranking_grid,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ==================================================
    # TOP 10 E PIORES 10 TURMAS
    # ==================================================

    st.subheader("📊 Desempenho das Turmas")

    ranking_top = (
        df_filtrado
        .groupby("Turma")["Acertos"]
        .mean()
        .sort_values(ascending=False)
    )

    top10 = (
        ranking_top
        .head(10)
        .reset_index(name="Média")
    )

    bottom10 = (
        ranking_top
        .tail(10)
        .reset_index(name="Média")
    )

    # ==================================================
    # PALETA
    # ==================================================

    paleta_top_turmas = st.selectbox(
        "🎨 Paleta dos gráficos",
        [
            "Colorido",
            "Escala Azul",
            "Escala Verde",
            "Escala Vermelha",
            "Escala Laranja"
        ],
        key="paleta_top_bottom_turmas"
    )

    if paleta_top_turmas == "Colorido":

        cores_top = px.colors.qualitative.Bold

    elif paleta_top_turmas == "Escala Azul":

        cores_top = px.colors.sequential.Blues

    elif paleta_top_turmas == "Escala Verde":

        cores_top = px.colors.sequential.Greens

    elif paleta_top_turmas == "Escala Vermelha":

        cores_top = px.colors.sequential.Reds

    else:

        cores_top = px.colors.sequential.Oranges

    # ==================================================
    # RÓTULOS
    # ==================================================

    top10["Rotulo"] = top10["Média"].apply(
        lambda x: f"{x:.2f}"
    )

    bottom10["Rotulo"] = bottom10["Média"].apply(
        lambda x: f"{x:.2f}"
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
        .groupby("Turma")
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
            "Turma",
            "Qtde_Alunos",
            "Acertos",
            "Média",
            "Classificação"
        ]
    ]

    ranking_analitico.columns = [
        "Posição",
        "Turma",
        "Qtde Alunos",
        "Acertos",
        "Média",
        "Classificação"
    ]



    # ==================================================
    # TABELA
    # ==================================================

    st.dataframe(
        ranking_analitico,
        use_container_width=True,
        hide_index=True,
        height=min(
            600,
            (len(ranking_analitico) * 35) + 40
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

    def classificar_turma(media):

        if media >= 16:
            return "🟢 Excelente"

        elif media >= 13:
            return "🔵 Bom"

        elif media >= 10:
            return "🟠 Atenção"

        else:
            return "🔴 Crítico"

    dist_turmas = (
        df_filtrado
        .groupby("Turma")["Acertos"]
        .mean()
        .reset_index(name="Média")
    )

    dist_turmas["Categoria"] = (
        dist_turmas["Média"]
        .apply(classificar_turma)
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

    # ==================================================
    # INSIGHTS IA DAS TURMAS
    # ==================================================

    st.subheader("🤖 Insights IA das Turmas")

    # ==================================================
    # CÁLCULOS
    # ==================================================

    media_escola = (
        ranking_analitico["Média"]
        .mean()
    )

    melhor_turma = (
        ranking_analitico
        .iloc[0]["Turma"]
    )

    melhor_media = (
        ranking_analitico
        .iloc[0]["Média"]
    )

    pior_turma = (
        ranking_analitico
        .iloc[-1]["Turma"]
    )

    pior_media = (
        ranking_analitico
        .iloc[-1]["Média"]
    )

    diferenca = (
            melhor_media
            - pior_media
    )

    qtde_excelente = (
        ranking_analitico["Classificação"]
        .str.contains("Excelente")
        .sum()
    )

    qtde_bom = (
        ranking_analitico["Classificação"]
        .str.contains("Bom")
        .sum()
    )

    qtde_atencao = (
        ranking_analitico["Classificação"]
        .str.contains("Atenção")
        .sum()
    )

    qtde_critico = (
        ranking_analitico["Classificação"]
        .str.contains("Crítico")
        .sum()
    )

    perc_acima_meta = (
            (
                    ranking_analitico["Média"] >= 13
            ).mean() * 100
    )

    # ==================================================
    # LAYOUT
    # ==================================================

    col1, col2 = st.columns(2)

    # ==================================================
    # POSITIVOS
    # ==================================================

    with col1:

        st.success(
            "Pontos Positivos"
        )

        st.markdown(f"""
    ✅ Melhor turma da escola: **{melhor_turma}**

    ✅ Média da melhor turma: **{melhor_media:.2f}**

    ✅ Média geral das turmas: **{media_escola:.2f}**

    ✅ Turmas classificadas como Excelente: **{qtde_excelente}**

    ✅ Turmas classificadas como Bom: **{qtde_bom}**

    ✅ {perc_acima_meta:.1f}% das turmas estão acima da meta pedagógica

    ✅ Estrutura de desempenho consolidada para acompanhamento

    ✅ Indicadores disponíveis para tomada de decisão

    ✅ Comparação entre turmas realizada automaticamente

    ✅ Monitoramento contínuo do desempenho escolar
    """)

    # ==================================================
    # ATENÇÃO
    # ==================================================

    with col2:

        st.error(
            "Pontos de Atenção"
        )

        st.markdown(f"""
    ⚠️ Turma que requer maior atenção: **{pior_turma}**

    ⚠️ Média da turma crítica: **{pior_media:.2f}**

    ⚠️ Diferença entre melhor e pior turma: **{diferenca:.2f}**

    ⚠️ Turmas em Atenção: **{qtde_atencao}**

    ⚠️ Turmas em situação Crítica: **{qtde_critico}**

    ⚠️ Possível desigualdade de desempenho entre turmas

    ⚠️ Necessidade de acompanhamento pedagógico focalizado

    ⚠️ Recomendado monitoramento das turmas abaixo da meta

    ⚠️ Avaliar estratégias de recuperação da aprendizagem

    ⚠️ Priorizar intervenções nas turmas classificadas como Críticas
    """)

    st.divider()

    # ==================================================
    # RELATÓRIO EXECUTIVO DAS TURMAS
    # ==================================================

    st.subheader("📄 Relatório Executivo das Turmas")

    if st.button(
            "🤖 Gerar Relatório das Turmas",
            key="relatorio_turmas"
    ):
        relatorio = f"""
    A escola {escola_selecionada} possui {total_turmas} turmas avaliadas.

    A média geral das turmas foi de {media_escola:.2f} acertos.

    A turma com melhor desempenho foi {melhor_turma},
    atingindo média de {melhor_media:.2f} acertos.

    A turma que requer maior atenção é {pior_turma},
    com média de {pior_media:.2f} acertos.

    A diferença entre a melhor e a pior turma foi de
    {diferenca:.2f} pontos.

    Foram identificadas:

    • {qtde_excelente} turmas classificadas como Excelente;

    • {qtde_bom} turmas classificadas como Bom;

    • {qtde_atencao} turmas classificadas como Atenção;

    • {qtde_critico} turmas classificadas como Crítico.

    O percentual de turmas acima da meta pedagógica foi de
    {perc_acima_meta:.1f}%.

    Recomenda-se manter o acompanhamento das turmas com melhor desempenho e priorizar ações pedagógicas para as turmas classificadas como Atenção e Crítico, visando reduzir desigualdades internas e elevar os indicadores de aprendizagem.
    """

        st.text_area(
            "Relatório Gerado",
            relatorio,
            height=350
        )

    st.divider()

    # ==================================================
    # EXPORTAÇÃO
    # ==================================================

    st.subheader("📥 Exportação")

    st.caption(
        "Exporta os principais indicadores das turmas da escola selecionada."
    )

    buffer = BytesIO()

    with pd.ExcelWriter(
            buffer,
            engine="openpyxl"
    ) as writer:

        # Ranking Analítico

        ranking_analitico.to_excel(
            writer,
            sheet_name="Ranking Analitico",
            index=False
        )

        # Ranking Visual

        ranking_analitico.to_excel(
            writer,
            sheet_name="Ranking Visual",
            index=False
        )

        # Distribuição

        dist_graf.to_excel(
            writer,
            sheet_name="Distribuicao",
            index=False
        )

    st.download_button(
        label="📥 Exportar Relatório Completo",
        data=buffer.getvalue(),
        file_name=(
            f"turmas_"
            f"{escola_selecionada}.xlsx"
        ),
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        key="download_relatorio_turmas"
    )

    st.divider()
