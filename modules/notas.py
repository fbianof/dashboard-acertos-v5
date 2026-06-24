from cProfile import label

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


def mostrar_notas(df):
    st.header("📝 NOTAS")

    st.subheader("📖 Análise das Questões")

    escolas_notas = ["Todas as Escolas"] + sorted(
        df["Escola"].dropna().unique().tolist()
    )

    escola_nota = st.selectbox(
        "🏫 Escola",
        escolas_notas
    )

    if escola_nota != "Todas as Escolas":
        df_notas = df[
            df["Escola"] == escola_nota
        ].copy()
    else:
        df_notas = df.copy()

    # ==================================================
    # KPIs
    # ==================================================

    questoes = [
        c for c in df_notas.columns
        if c.startswith("B1. Q")
    ]

    total_questoes = len(questoes)

    # ==================================================
    # PERCENTUAIS POR QUESTÃO
    # ==================================================

    percentuais = {
        q: (
            df_notas[q].sum()
            / len(df_notas)
        ) * 100
        for q in questoes
    }

    # ==================================================
    # QUESTÃO MAIS FÁCIL
    # ==================================================

    questao_facil = max(
        percentuais,
        key=percentuais.get
    )

    perc_questao_facil = (
        percentuais[questao_facil]
    )

    # ==================================================
    # QUESTÃO MAIS DIFÍCIL
    # ==================================================

    questao_dificil = min(
        percentuais,
        key=percentuais.get
    )

    perc_questao_dificil = (
        percentuais[questao_dificil]
    )

    # ==================================================
    # APROVEITAMENTO GERAL
    # ==================================================

    aproveitamento_geral = (
        df_notas[questoes]
        .sum()
        .sum()
        /
        (
            len(df_notas)
            * total_questoes
        )
    ) * 100

    # ==================================================
    # KPIs
    # ==================================================

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "📖 Total de Questões",
        total_questoes,
        help="Quantidade total de questões avaliadas na prova."
    )

    c2.metric(
        "🏆 Questão Mais Fácil",
        f"{questao_facil.replace('B1. ', '')} ({perc_questao_facil:.1f}%)",
        help="Questão com o maior percentual de acertos entre os alunos avaliados."
    )

    c3.metric(
        "⚠️ Questão Mais Difícil",
        f"{questao_dificil.replace('B1. ', '')} ({perc_questao_dificil:.1f}%)",
        help="Questão com o menor percentual de acertos entre os alunos avaliados."
    )

    c4.metric(
        "📊 Aproveitamento Geral",
        f"{aproveitamento_geral:.1f}%",
        help="Percentual médio de acertos. Fórmula: (Total de Acertos ÷ Total de Respostas Possíveis) × 100."
    )

    st.divider()

    # ==================================================
    # DESEMPENHO POR QUESTÃO
    # ==================================================

    questoes = [
        c for c in df_notas.columns
        if c.startswith("B1. Q")
    ]

    questoes_df = pd.DataFrame({
        "Questão": [
            q.replace("B1. ", "")
            for q in questoes
        ],
        "% Acerto": [
            (
                    df_notas[q].sum()
                    / len(df_notas)
            ) * 100
            for q in questoes
        ]
    })

    questoes_df = (
        questoes_df
        .sort_values(
            "% Acerto",
            ascending=False
        )
        .reset_index(drop=True)
    )

    st.subheader("📈 Desempenho por Questão")

    # ==================================================
    # SELETOR DE TIPO DE GRÁFICO
    # ==================================================

    c1, c2 = st.columns(2)

    with c1:
        tipo_grafico = st.selectbox(
            "📊 Tipo de Gráfico",
            [
                "Barra Vertical",
                "Barra Horizontal"
            ]
        )

    # ==================================================
    # SELETOR DE CORES
    # ==================================================

    with c2:
        paleta = st.selectbox(
            "🎨 Paleta",
            [
                "Colorido",
                "Escala Azul",
                "Escala Verde",
                "Escala Laranja",
                "Escala Vermelho",
                "Escala Roxo"
            ]
        )

        if paleta == "Colorido":
            cores = px.colors.qualitative.Set3

        elif paleta == "Escala Azul":
            cores = px.colors.sequential.Blues

        elif paleta == "Escala Verde":
            cores = px.colors.sequential.Greens

        elif paleta == "Escala Laranja":
            cores = px.colors.sequential.Oranges

        elif paleta == "Escala Vermelho":
            cores = px.colors.sequential.Reds

        else:
            cores = px.colors.sequential.Purples


    # ==================================================
    # TIPO DE GRÁFICO BARRA VERTICAL
    # ==================================================

    if tipo_grafico == "Barra Vertical":

        fig = px.bar(
            questoes_df,
            x="Questão",
            y="% Acerto",
            color="% Acerto",
            color_continuous_scale=cores,
            text="% Acerto"
        )

        fig.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="auto"
        )

        fig.update_layout(
            title="📊 Percentual de Acertos por Questão",
            xaxis_title="Questão",
            yaxis_title="% Acerto",
            coloraxis_showscale=False,
            template="plotly",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        fig.update_yaxes(
            range=[0, 105]
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ==================================================
    # BARRA HORIZONTAL
    # ==================================================

    elif tipo_grafico == "Barra Horizontal":

        fig = px.bar(
            questoes_df,
            y="Questão",
            x="% Acerto",
            orientation="h",
            color="% Acerto",
            color_continuous_scale=cores,
            text="% Acerto"
        )

        fig.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="auto"
        )

        fig.update_layout(
            title="📊 Percentual de Acertos por Questão",
            xaxis_title="% Acerto",
            yaxis_title="Questão",
            coloraxis_showscale=False,
            template="plotly",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        fig.update_xaxes(
            range=[0, 105]
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # ==================================================
    # TOP 5 QUESTÕES MAIS FÁCEIS E MAIS DIFÍCEIS
    # ==================================================

    top_facil = (
        questoes_df
        .sort_values("% Acerto", ascending=False)
        .head(5)
        .sort_values("% Acerto", ascending=True)
    )

    top_dificil = (
        questoes_df
        .sort_values("% Acerto", ascending=True)
        .head(5)
    )

    st.divider()

    c1, c2 = st.columns(2)

    # ==================================================
    # TOP 5 MAIS FÁCEIS
    # ==================================================

    with c1:

        st.subheader("🏆 Top 5 Questões Mais Fáceis")

        fig_facil = px.bar(
            top_facil,
            y="Questão",
            x="% Acerto",
            orientation="h",
            color="% Acerto",
            color_continuous_scale=cores,
            text="% Acerto"
        )

        fig_facil.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="auto"
        )

        fig_facil.update_layout(
            xaxis_title="Percentual de Acertos (%)",
            yaxis_title="Questões",
            coloraxis_showscale=False,
            template="plotly",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(
                t=0,
                b=20,
                l=20,
                r=20
            )
        )

        fig_facil.update_xaxes(
            range=[0, 100]
        )

        st.plotly_chart(
            fig_facil,
            use_container_width=True
        )

    # ==================================================
    # TOP 5 MAIS DIFÍCEIS
    # ==================================================

    with c2:

        st.subheader("⚠️ Top 5 Questões Mais Difíceis")

        fig_dificil = px.bar(
            top_dificil,
            y="Questão",
            x="% Acerto",
            orientation="h",
            color="% Acerto",
            color_continuous_scale=cores,
            text="% Acerto"
        )

        fig_dificil.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="auto"
        )

        fig_dificil.update_layout(
            xaxis_title="Percentual de Acertos (%)",
            yaxis_title="Questões",
            coloraxis_showscale=False,
            template="plotly",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(
                t=0,
                b=20,
                l=20,
                r=20
            )
        )

        fig_dificil.update_xaxes(
            range=[0, 100]
        )

        st.plotly_chart(
            fig_dificil,
            use_container_width=True
        )

    st.divider()

    # ==================================================
    # TABELA ANALÍTICA DAS QUESTÕES
    # ==================================================

    st.subheader(
        "📋 Tabela Analítica das Questões",
        help="""
        Análise detalhada do desempenho de cada questão.

        % Acerto = (Acertos ÷ Total de Alunos) × 100

        % Erro = (Erros ÷ Total de Alunos) × 100
        """
    )

    # ==================================================
    # CLASSIFICAÇÃO DAS QUESTÕES
    # ==================================================

    def classificar_questao(percentual):

        if percentual >= 80:
            return "🟢 Excelente"

        elif percentual >= 60:
            return "🔵 Bom"

        elif percentual >= 40:
            return "🟡 Atenção"

        else:
            return "🔴 Crítico"

    # ==================================================
    # MONTA DATAFRAME
    # ==================================================

    analitico_df = pd.DataFrame({
        "Questão": [
            q.replace("B1. ", "")
            for q in questoes
        ],
        "Acertos": [
            int(df_notas[q].sum())
            for q in questoes
        ]
    })

    # ==================================================
    # CÁLCULOS
    # ==================================================

    analitico_df["Erros"] = (
            len(df_notas)
            - analitico_df["Acertos"]
    )

    analitico_df["% Acerto"] = (
            analitico_df["Acertos"]
            / len(df_notas)
            * 100
    )

    analitico_df["% Erro"] = (
            100
            - analitico_df["% Acerto"]
    )

    analitico_df["Situação"] = (
        analitico_df["% Acerto"]
        .apply(classificar_questao)
    )

    # ==================================================
    # ORDENAÇÃO
    # ==================================================

    analitico_df = (
        analitico_df
        .sort_values(
            "% Acerto",
            ascending=False
        )
        .reset_index(drop=True)
    )

    # ==================================================
    # POSIÇÃO
    # ==================================================

    analitico_df.insert(
        0,
        "Posição",
        range(
            1,
            len(analitico_df) + 1
        )
    )

    # ==================================================
    # FORMATAÇÃO
    # ==================================================

    analitico_df["% Acerto"] = (
        analitico_df["% Acerto"]
        .map(lambda x: f"{x:.2f}%")
    )

    analitico_df["% Erro"] = (
        analitico_df["% Erro"]
        .map(lambda x: f"{x:.2f}%")
    )

    # ==================================================
    # EXIBIÇÃO
    # ==================================================

    altura = min(
        900,
        (len(analitico_df) + 1) * 35
    )

    st.dataframe(
        analitico_df,
        use_container_width=True,
        hide_index=True,
        height=altura
    )

    st.markdown("""
    <div style="
        padding:10px;
        border-radius:10px;
        background-color:rgba(128,128,128,0.08);
        text-align:justify;
        font-weight:400;
    ">
    📌 CRITÉRIOS DE CLASSIFICAÇÃO<BR>
    🟢 Excelente ≥ 80% &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
    🔵 Bom 60% - 79,99% &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
    🟡 Atenção 40% - 59,99% &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
    🔴 Crítico &lt; 40%
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ==================================================
    # DISTRIBUIÇÃO DAS NOTAS
    # ==================================================

    st.subheader(
        "📈 Distribuição das Notas",
        help="""
        Distribuição da quantidade de alunos por número de acertos obtidos na avaliação.
        """
    )

    nota_mais_frequente = (
        df_notas["Acertos"]
        .mode()[0]
    )

    qtde_moda = (
        (df_notas["Acertos"] == nota_mais_frequente)
        .sum()
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📌 Nota Mais Frequente",
            f"{nota_mais_frequente} acertos"
        )

    with col2:
        st.metric(
            "👥 Alunos nessa Nota",
            qtde_moda
        )

    with col3:
        st.metric(
            "📊 Média Geral",
            f"{df_notas['Acertos'].mean():.1f}"
        )

    st.divider()

    # ==================================================
    # CONFIGURAÇÃO DO GRÁFICO
    # ==================================================

    ordem_grafico = st.radio(
        "📊 Ordenação do Gráfico",
        ["Número de Acertos", "Quantidade de Alunos"],
        horizontal=True
    )

    # Distribuição das notas
    dist_notas = (
        df_notas.groupby("Acertos")
        .size()
        .reset_index(name="Quantidade")
    )

    # Ordenação
    if ordem_grafico == "Número de Acertos":
        dist_notas = dist_notas.sort_values(
            "Acertos",
            ascending=True
        )
    else:
        dist_notas = dist_notas.sort_values(
            "Quantidade",
            ascending=True
        )

    # Texto do eixo Y
    dist_notas["Rotulo"] = (
            "Acertos: "
            + dist_notas["Acertos"].astype(str)
            + " | Alunos: "
            + dist_notas["Quantidade"].astype(str)
    )

    # ==================================================
    # GRÁFICO
    # ==================================================

    fig = px.bar(
        dist_notas,
        x="Quantidade",
        y="Rotulo",
        orientation="h",
        text="Quantidade",
        title="Distribuição de Alunos por Número de Acertos"
    )


    fig.update_traces(
        marker_color="#3B82F6",
        textposition="outside",
        hovertemplate=(
                "<b>Acertos:</b> "
                + dist_notas["Acertos"].astype(str)
                + "<br><b>Alunos:</b> "
                + dist_notas["Quantidade"].astype(str)
        )
    )

    fig.update_layout(
        height=750,
        showlegend=False,
        margin=dict(l=20, r=80, t=60, b=20),

        title_font=dict(size=22),

        xaxis_title="Quantidade de Alunos",
        yaxis_title="Total de acertos na Prova",

        xaxis=dict(
            tickfont=dict(size=13),
            title_font=dict(size=15)
        ),

        yaxis=dict(
            tickfont=dict(size=13),
            title_font=dict(size=15)
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    with st.expander("ℹ️ Como interpretar este gráfico"):
        st.markdown("""
    **Este gráfico mostra a distribuição dos alunos pelo total de acertos obtidos na prova.**

    **Exemplo:**
    - **13 acertos | 308 alunos** → significa que **308 alunos concluíram a avaliação com 13 acertos**.
    - O número **13** representa o **total de acertos na prova**, **não** a **Questão 13**.

    Para analisar o desempenho de cada questão, consulte os gráficos da seção **Desempenho por Questão**.
    """)

    st.divider()

    # ==================================================
    # FAIXAS DE DESEMPENHO DOS ALUNOS
    # ==================================================

    st.subheader(
        "🎯 Faixas de Desempenho dos Alunos",
        help="""
        Classificação dos alunos conforme o total de acertos obtidos na avaliação.
        Permite identificar rapidamente os grupos que necessitam de maior acompanhamento pedagógico.
        """
    )

    # Classificação das faixas de desempenho
    def classificar_desempenho(acertos):
        if acertos <= 5:
            return "🔴 Crítico"
        elif acertos <= 9:
            return "🟠 Básico"
        elif acertos <= 13:
            return "🟡 Intermediário"
        elif acertos <= 16:
            return "🟢 Adequado"
        else:
            return "🔵 Excelente"

    df_faixas = df_notas.copy()
    df_faixas["Faixa"] = df_faixas["Acertos"].apply(classificar_desempenho)

    faixas = (
        df_faixas
        .groupby("Faixa")
        .size()
        .reset_index(name="Quantidade")
    )

    # ==================================================
    # KPIs DAS FAIXAS DE DESEMPENHO
    # ==================================================

    # Garante que todas as faixas existam
    ordem_faixas = [
        "🔴 Crítico",
        "🟠 Básico",
        "🟡 Intermediário",
        "🟢 Adequado",
        "🔵 Excelente"
    ]

    faixas = (
        faixas
        .set_index("Faixa")
        .reindex(ordem_faixas, fill_value=0)
        .reset_index()
    )

    total_alunos = faixas["Quantidade"].sum()

    # Seis KPIs
    col_total, col1, col2, col3, col4, col5 = st.columns(6)

    # KPI Total de Alunos
    with col_total:
        st.metric(
            label="👥 Total",
            value=f"{total_alunos:,}".replace(",", "."),
            delta="100% dos alunos"
        )

    # KPIs das faixas
    for coluna, (_, linha) in zip(
            [col1, col2, col3, col4, col5],
            faixas.iterrows()
    ):
        percentual = (
            linha["Quantidade"] / total_alunos * 100
            if total_alunos > 0 else 0
        )

        with coluna:
            st.metric(
                label=linha["Faixa"],
                value=f'{linha["Quantidade"]:,}'.replace(",", "."),
                delta=f"{percentual:.1f}% dos alunos"
            )

    st.divider()
    # ==================================================
    # GRÁFICO - FAIXAS DE DESEMPENHO
    # ==================================================

    # Calcula o percentual
    faixas["Percentual"] = (
            faixas["Quantidade"] / total_alunos * 100
    ).round(1)

    fig = px.bar(
        faixas,
        x="Quantidade",
        y="Faixa",
        orientation="h",
        text="Quantidade",
        title="Distribuição dos Alunos por Faixa de Desempenho"
    )

    fig.update_traces(
        marker_color="#3B82F6",
        textposition="outside",
        textfont=dict(size=13),
        hovertemplate=(
            "<b>Faixa:</b> %{y}<br>"
            "<b>Alunos:</b> %{x}<br>"
            "<b>Percentual:</b> %{customdata:.1f}%"
            "<extra></extra>"
        ),
        customdata=faixas["Percentual"]
    )

    fig.update_layout(
        height=450,
        showlegend=False,
        margin=dict(l=20, r=80, t=60, b=20),

        xaxis_title="Quantidade de Alunos",
        yaxis_title="Faixa de Desempenho",

        title_font=dict(size=22),

        xaxis=dict(
            tickfont=dict(size=13),
            title_font=dict(size=15)
        ),

        yaxis=dict(
            tickfont=dict(size=14),
            title_font=dict(size=15),
            categoryorder="array",
            categoryarray=[
                "🔴 Crítico",
                "🟠 Básico",
                "🟡 Intermediário",
                "🟢 Adequado",
                "🔵 Excelente"
            ]
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


st.divider()

