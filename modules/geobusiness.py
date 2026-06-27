
import pandas as pd
import folium
import streamlit as st
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import unicodedata
import re

def normalizar(texto):
    if pd.isna(texto):
        return ""
    texto = unicodedata.normalize("NFKD", str(texto)).encode("ASCII","ignore").decode()
    texto = texto.upper()
    for t in ["EMEB","EMEF","EMCEB","EMREF","ESCOLA MUNICIPAL DE EDUCACAO BASICA",
              "PROFESSORA","PROF.","PROF","PROFº","PROFª","PROF.ºª"]:
        texto = texto.replace(t," ")
    texto = re.sub(r"\s+"," ",texto).strip()
    return texto

def cor(media):
    if media >= 16:
        return "#22C55E","Excelente"
    elif media >= 13:
        return "#3B82F6","Bom"
    elif media >= 10:
        return "#F59E0B","Atenção"
    return "#EF4444","Crítico"

def mostrar_geobusiness():
    df_geo = pd.read_excel("data/escolas_geograficas.xlsx")
    df_acertos = pd.read_excel("data/Acertos_V7.xlsx")

    df_geo["CHAVE"] = df_geo["Escola"].apply(normalizar)
    df_acertos["CHAVE"] = df_acertos["Escola"].apply(normalizar)

    resumo = (
        df_acertos.groupby("CHAVE")
        .agg(Media=("Acertos","mean"),
             Alunos=("Aluno","count"))
        .reset_index()
    )

    df = df_geo.merge(resumo,on="CHAVE",how="left")
    df["Media"]=df["Media"].fillna(0)
    df["Alunos"]=df["Alunos"].fillna(0).astype(int)

    st.title("🗺️ GeoBusiness Intelligence")
    st.caption("Mapa Educacional da Rede Municipal")

    c1,c2,c3,c4=st.columns(4)
    c1.metric("🏫 Escolas",len(df))
    c2.metric("👨‍🎓 Alunos",int(df["Alunos"].sum()))
    c3.metric("📊 Média",f"{df['Media'].mean():.2f}")
    c4.metric("🟢 Excelentes",int((df["Media"]>=16).sum()))

    st.markdown("🟢 Excelente (≥16) &nbsp;&nbsp; 🔵 Bom (13–15,99) &nbsp;&nbsp; 🟠 Atenção (10–12,99) &nbsp;&nbsp; 🔴 Crítico (<10)")

    escolas=["Todas"]+sorted(df["Escola"].tolist())
    escolha=st.selectbox("🔍 Pesquisar escola",escolas)

    centro=[-16.4704,-54.6358]
    zoom=12
    if escolha!="Todas":
        r=df[df["Escola"]==escolha].iloc[0]
        centro=[r["Latitude"],r["Longitude"]]
        zoom=15

    mapa=folium.Map(location=centro,zoom_start=zoom,control_scale=True)
    cluster=MarkerCluster().add_to(mapa)

    tabela=[]
    for _,e in df.iterrows():
        if escolha!="Todas" and e["Escola"]!=escolha:
            continue
        color,status=cor(e["Media"])
        popup=f"""
        <b>{e['Escola']}</b><br>
        <b>INEP:</b> {e['Código INEP']}<br>
        <b>Status:</b> {status}<br>
        <b>Média:</b> {e['Media']:.2f}<br>
        <b>Alunos:</b> {e['Alunos']}<br>
        <b>Localização:</b> {e['Localização']}<br>
        <b>Endereço:</b> {e['Endereço']}
        """
        folium.CircleMarker(
            location=[e["Latitude"],e["Longitude"]],
            radius=8,color=color,fill=True,
            fill_color=color,fill_opacity=0.9,
            tooltip=e["Escola"],
            popup=folium.Popup(popup,max_width=350)
        ).add_to(cluster)
        tabela.append({
            "Escola":e["Escola"],
            "Média":round(e["Media"],2),
            "Alunos":e["Alunos"],
            "Classificação":status
        })

    st_folium(mapa,use_container_width=True,height=700)
    st.divider()
    st.subheader("Resumo das Escolas")
    st.dataframe(pd.DataFrame(tabela),use_container_width=True,hide_index=True)
