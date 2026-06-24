import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO


def mostrar_escolas(df, df_ideb):

    st.header("🏫 ESCOLAS")

    if df is None or len(df) == 0:
        st.warning("Nenhum dado encontrado.")
        return

    # ==================================================
    # DADOS
    # ==================================================

    ranking = (
        df.groupby("Escola")["Acertos"]
        .mean()
        .sort_values(ascending=False)
    )

    ranking_df = ranking.reset_index()
    ranking_df.columns = ["Escola", "Média"]

    total_escolas = len(ranking_df)

    media_rede = ranking_df["Média"].mean()

    melhor_escola = ranking_df.iloc[0]["Escola"]
    pior_escola = ranking_df.iloc[-1]["Escola"]

    nota_melhor = ranking_df.iloc[0]["Média"]
    nota_pior = ranking_df.iloc[-1]["Média"]

    perc_acima_media = (
        (ranking_df["Média"] > media_rede).mean() * 100
    )

    media_ideb = "-"

    if (
        df_ideb is not None
        and "IDEB_Escola" in df_ideb.columns
    ):
        media_ideb = f"{df_ideb['IDEB_Escola'].mean():.2f}"

    # ==================================================
    # KPIs
    # ==================================================

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "🏫 Total de Escolas",
        total_escolas,
        help="Quantidade total de escolas consideradas nos filtros aplicados."
    )

    c2.metric(
        "📊 Média da Rede",
        f"{media_rede:.2f}",
        help="Média de acertos das escolas selecionadas."
    )

    c3.metric(
        "🏆 Nota da Melhor Escola",
        f"{nota_melhor:.2f}",
        help="Maior média de acertos entre as escolas selecionadas."
    )

    c4, c5, c6 = st.columns(3)

    c4.metric(
        "⚠️ Nota da Escola Crítica",
        f"{nota_pior:.2f}",
        help="Menor média de acertos entre as escolas selecionadas."
    )

    c5.metric(
        "📚 Média IDEB",
        media_ideb,
        help="Média do IDEB das escolas selecionadas."
    )

    c6.metric(
        "🎯 % Acima da Média",
        f"{perc_acima_media:.1f}%",
        help="Percentual de escolas com média superior à média geral da rede."
    )

    st.info(
        f"🏆 Melhor Escola da Rede: {melhor_escola}"
    )

    st.warning(
        f"⚠️ Escola que requer maior atenção: {pior_escola}"
    )

    st.divider()

    # ==================================================
    # GRÁFICO PRINCIPAL
    # ==================================================

    st.subheader("📊 Ranking das Escolas")

    ranking_df["Média"] = ranking_df["Média"].round(2)

    col1, col2 = st.columns(2)

    with col1:

        tipo = st.selectbox(
            "Tipo de gráfico",
            [
                "Barras Horizontais",
                "Barras Verticais",
                "Linha",
                "Área",
                "Pizza",
                "Rosca"
            ]
        )

    with col2:

        paleta = st.selectbox(
            "Paleta de cores",
            [
                "Colorido",
                "Escala Azul",
                "Escala Verde",
                "Escala Vermelha"
            ]
        )

    if paleta == "Colorido":

        cores = px.colors.qualitative.Bold

    elif paleta == "Escala Azul":

        cores = px.colors.sequential.Blues

    elif paleta == "Escala Verde":

        cores = px.colors.sequential.Greens

    else:

        cores = px.colors.sequential.Reds

    # ==================================================
    # BARRAS HORIZONTAIS
    # ==================================================

    if tipo == "Barras Horizontais":

        fig = px.bar(
            ranking_df,
            x="Média",
            y="Escola",
            orientation="h",
            text="Média",
            color="Média",
            color_continuous_scale=cores
        )

        fig.update_traces(
            texttemplate="%{x:.2f}",
            textposition="auto",
            textfont_size=18
        )

        fig.update_layout(
            height=max(
                700,
                len(ranking_df) * 40
            ),
            bargap=0.10,
            coloraxis_showscale=False
        )

        fig.update_yaxes(
            categoryorder="total ascending"
        )

    # ==================================================
    # BARRAS VERTICAIS
    # ==================================================

    elif tipo == "Barras Verticais":

        fig = px.bar(
            ranking_df,
            x="Escola",
            y="Média",
            text="Média",
            color="Média",
            color_continuous_scale=cores
        )

        fig.update_traces(
            texttemplate="%{y:.2f}",
            textposition="auto",
            textfont_size=16
        )

        fig.update_layout(
            height=650,
            coloraxis_showscale=False
        )

    # ==================================================
    # LINHA
    # ==================================================

    elif tipo == "Linha":

        aux = ranking_df.copy()

        aux["Posição"] = range(
            1,
            len(aux) + 1
        )

        cor_linha = (
            cores[-1]
            if paleta != "Colorido"
            else "#2563EB"
        )

        fig = px.line(
            aux,
            x="Posição",
            y="Média",
            markers=True
        )

        fig.update_traces(
            line=dict(width=4, color=cor_linha),
            marker=dict(size=10, color=cor_linha)
        )

        fig.add_scatter(
            x=aux["Posição"],
            y=aux["Média"],
            mode="text",
            text=[f"{v:.2f}" for v in aux["Média"]],
            textposition="top center",
            showlegend=False
        )

        fig.update_layout(
            height=650
        )

    # ==================================================
    # ÁREA
    # ==================================================

    elif tipo == "Área":

        aux = ranking_df.copy()

        aux["Posição"] = range(
            1,
            len(aux) + 1
        )

        cor_area = (
            cores[-1]
            if paleta != "Colorido"
            else "#16A34A"
        )

        fig = px.area(
            aux,
            x="Posição",
            y="Média",
            color_discrete_sequence=[cor_area]
        )

        fig.add_scatter(
            x=aux["Posição"],
            y=aux["Média"],
            mode="markers+text",
            text=[f"{v:.2f}" for v in aux["Média"]],
            textposition="top center",
            showlegend=False
        )

        fig.update_layout(
            height=650
        )

    # ==================================================
    # PIZZA
    # ==================================================

    elif tipo == "Pizza":

        fig = px.pie(
            ranking_df,
            names="Escola",
            values="Média",
            color_discrete_sequence=cores
        )

        fig.update_traces(
            textinfo="percent+label",
            textposition="auto"
        )

        fig.update_layout(
            height=700
        )

    # ==================================================
    # ROSCA
    # ==================================================

    else:

        fig = px.pie(
            ranking_df,
            names="Escola",
            values="Média",
            hole=0.45,
            color_discrete_sequence=cores
        )

        fig.update_traces(
            textinfo="percent+label",
            textposition="auto"
        )

        fig.update_layout(
            height=700
        )

    # ==================================================
    # EXIBIR
    # ==================================================

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # ==================================================
    # EXIBIÇÃO
    # ==================================================

    st.caption(f"Total de escolas: {len(ranking_df)}")

    st.dataframe(
        ranking_df,
        use_container_width=True,
        hide_index=True,
        height=min(35 * len(ranking_df) + 40, 2000)
    )
    st.divider()

    # ==================================================
    # DISTRIBUIÇÃO DAS ESCOLAS
    # ==================================================

    st.subheader("📊 Distribuição das Escolas")

    def classificar(valor):

        if valor >= 16:
            return "🟢 Excelente (≥16)"

        elif valor >= 13:
            return "🔵 Bom (13-15,99)"

        elif valor >= 10:
            return "🟠 Atenção (10-12,99)"

        return "🔴 Crítico (<10)"

    dist = ranking_df.copy()

    dist["Categoria"] = dist["Média"].apply(classificar)

    dist_graf = (
        dist.groupby("Categoria")
        .size()
        .reset_index(name="Quantidade")
    )

    # Ordenação fixa

    ordem = [
        "🟢 Excelente (≥16)",
        "🔵 Bom (13-15,99)",
        "🟠 Atenção (10-12,99)",
        "🔴 Crítico (<10)"
    ]

    dist_graf["Categoria"] = pd.Categorical(
        dist_graf["Categoria"],
        categories=ordem,
        ordered=True
    )

    dist_graf = dist_graf.sort_values("Categoria")

    # Escolha do gráfico

    tipo_dist = st.selectbox(
        "Tipo de gráfico da distribuição",
        [
            "Pizza",
            "Rosca",
            "Barras",
            "Área"
        ]
    )

    # Paleta de cores

    cores = {
        "🟢 Excelente (≥16)": "#22C55E",
        "🔵 Bom (13-15,99)": "#3B82F6",
        "🟠 Atenção (10-12,99)": "#F59E0B",
        "🔴 Crítico (<10)": "#EF4444"
    }

    if tipo_dist == "Pizza":

        fig_dist = px.pie(
            dist_graf,
            names="Categoria",
            values="Quantidade",
            color="Categoria",
            color_discrete_map=cores
        )

        fig_dist.update_traces(
            textinfo="percent+label+value",
            textfont_size=16
        )

    elif tipo_dist == "Rosca":

        fig_dist = px.pie(
            dist_graf,
            names="Categoria",
            values="Quantidade",
            hole=0.45,
            color="Categoria",
            color_discrete_map=cores
        )

        fig_dist.update_traces(
            textinfo="percent+label+value",
            textfont_size=16
        )

    elif tipo_dist == "Barras":

        fig_dist = px.bar(
            dist_graf,
            x="Categoria",
            y="Quantidade",
            text="Quantidade",
            color="Categoria",
            color_discrete_map=cores
        )

        fig_dist.update_traces(
            textposition="outside",
            textfont_size=18
        )

    else:

        fig_dist = px.area(
            dist_graf,
            x="Categoria",
            y="Quantidade",
            color="Categoria",
            color_discrete_map=cores
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

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.success("""
    🟢 Excelente

    ≥ 16,00
    """)

    with col2:
        st.info("""
    🔵 Bom

    13,00 a 15,99
    """)

    with col3:
        st.warning("""
    🟠 Atenção

    10,00 a 12,99
    """)

    with col4:
        st.error("""
    🔴 Crítico

    < 10,00
    """)


    st.divider()





