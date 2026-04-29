import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Produtividade Integrado", layout="wide")

st.title("📊 Dashboard de Produtividade Detalhado - Abril")
st.markdown("---")

# --- 1. DADOS REAIS EXTRAÍDOS DA PLANILHA ---

# O que cada um fez por categoria
data_detalhado = {
    "Responsável": ["Alisson", "Alisson", "Alisson", "Amanda", "Amanda", "Amanda", "Gabriele", "Gabriele", "Gabriele"],
    "Categoria": ["Boleto", "Outros Poderes", "Rh Bahia", "Boleto", "Outros Poderes", "Rh Bahia", "Boleto", "Outros Poderes", "Rh Bahia"],
    "Quantidade": [12, 23, 29, 9, 3, 81, 68, 38, 58] # Ajustado conforme sua planilha
}
df_detalhado = pd.DataFrame(data_detalhado)

# Produtividade Anual (Total de Abril em cada ano)
data_anos = {
    "Ano": ["2023", "2024", "2025"],
    "Total": [0, 20, 324] # Conforme os totais das abas IR_2023, 2024 e 2025
}
df_anos = pd.DataFrame(data_anos)

# --- 2. ÁREA DE MÉTRICAS ---
totais = df_detalhado.groupby("Responsável")["Quantidade"].sum()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Geral (2025)", "321")
c2.metric("Média p/ Pessoa", "107")
c3.metric("Maior Volume", "Gabriele (164)")
c4.metric("Crescimento vs 2024", "+1520%")

st.markdown("---")

# --- 3. GRÁFICOS PRINCIPAIS ---
col_prod, col_setor = st.columns(2)

with col_prod:
    st.subheader("O que cada um fez? (Por Categoria)")
    # Gráfico que diferencia o tipo de trabalho por pessoa
    fig_barra = px.bar(
        df_detalhado, 
        x="Responsável", 
        y="Quantidade", 
        color="Categoria",
        barmode="group",
        text_auto=True,
        color_discrete_map={"Boleto": "#EF553B", "Rh Bahia": "#636EFA", "Outros Poderes": "#00CC96"}
    )
    st.plotly_chart(fig_barra, use_container_width=True)

with col_setor:
    st.subheader("Volume Total por Setor")
    fig_pizza = px.pie(
        df_detalhado, 
        values="Quantidade", 
        names="Categoria", 
        hole=0.4,
        color="Categoria",
        color_discrete_map={"Boleto": "#EF553B", "Rh Bahia": "#636EFA", "Outros Poderes": "#00CC96"}
    )
    st.plotly_chart(fig_pizza, use_container_width=True)

# --- 4. COMPARAÇÃO ANUAL ---
st.markdown("---")
st.subheader("📈 Evolução Anual - Mês de Abril")
fig_linha = px.line(
    df_anos, 
    x="Ano", 
    y="Total", 
    markers=True, 
    text="Total",
    title="Comparativo de Produtividade: 2023 vs 2024 vs 2025"
)
fig_linha.update_traces(line_color='#FF7F0E', textposition="top center")
st.plotly_chart(fig_linha, use_container_width=True)

st.success("✅ Dashboard atualizado com os dados da documentação de abril!")
