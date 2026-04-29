import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página para ocupar a tela toda
st.set_page_config(page_title="Dashboard de Produtividade - Abril", layout="wide")

# Estilização CSS para aproximar do layout da imagem de referência
st.markdown("""
<style>
    .stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        border: 1px solid #e6e9ef;
    }
    div[data-testid="stMetricValue"] > div {
        font-size: 36px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Demonstrativo de Produtividade - Abril")
st.markdown("---")

# --- 1. PROCESSAMENTO DOS DADOS REAIS DA PLANILHA ---

# Dados de volume total por pessoa e setor (extraídos da documentação)
data_detalhado = {
    "Responsável": ["Alisson", "Alisson", "Alisson", "Amanda", "Amanda", "Amanda", "Gabriele", "Gabriele", "Gabriele"],
    "Categoria": ["Boleto", "Outros Poderes", "Rh Bahia", "Boleto", "Outros Poderes", "Rh Bahia", "Boleto", "Outros Poderes", "Rh Bahia"],
    "Quantidade": [12, 23, 29, 9, 3, 81, 68, 38, 58]
}
df_detalhado = pd.DataFrame(data_detalhado)

# Dados de comparação anual (para o KPI de crescimento)
data_anos = {
    "Ano": ["2023", "2024", "2025"],
    "Total": [0, 20, 321]
}
df_anos = pd.DataFrame(data_anos)

# --- 2. LINHA DE KPIS (CARDS SUPERIORES) ---
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

total_geral_2025 = df_detalhado["Quantidade"].sum()
col_kpi1.metric(label="Total Geral (2025)", value=f"{total_geral_2025}")

# Encontrar o líder e a categoria mais ativa
lider_nome = df_detalhado.groupby("Responsável")["Quantidade"].sum().idxmax()
lider_val = df_detalhado.groupby("Responsável")["Quantidade"].sum().max()
col_kpi2.metric(label="Líder do Mês", value=lider_nome, help=f"{lider_val} registros")

cat_ativa = df_detalhado.groupby("Categoria")["Quantidade"].sum().idxmax()
col_kpi3.metric(label="Setor mais Ativo", value=cat_ativa)

# Cálculo de crescimento simples
# Considerando 2024 = 20 e 2025 = 321, o crescimento é massivo.
crescimento = ((total_geral_2025 - 20) / 20) * 100
col_kpi4.metric(label="Crescimento vs 2024", value=f"{crescimento:.1f}%")

st.markdown("---")

# --- 3. LINHA DE GRÁFICOS DINÂMICOS ---
col_chart_left, col_chart_right = st.columns(2)

with col_chart_left:
    st.subheader("Produção Detalhada por Pessoa e Categoria")
    # Gráfico dinâmico de barras empilhadas para mostrar O QUE cada um fez
    fig_barra = px.bar(
        df_detalhado, 
        x="Responsável", 
        y="Quantidade", 
        color="Categoria", 
        title="O que cada um fez?",
        text_auto=True,
        # Mantendo as cores do padrão que definimos
        color_discrete_map={"Boleto": "#EF553B", "Rh Bahia": "#636EFA", "Outros Poderes": "#00CC96"},
        barmode="stack" # Empilhado para ver o total e a divisão
    )
    fig_barra.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_barra, use_container_width=True)

with col_chart_right:
    st.subheader("Distribuição do Volume por Categoria")
    # Gráfico dinâmico de rosca para ver a participação de cada setor
    fig_pie = px.pie(
        df_detalhado, 
        values="Quantidade", 
        names="Categoria", 
        title="Volume Total por Categoria",
        hole=0.5,
        color="Categoria",
        color_discrete_map={"Boleto": "#EF553B", "Rh Bahia": "#636EFA", "Outros Poderes": "#00CC96"}
    )
    # Adicionar o total no centro da rosca
    fig_pie.add_annotation(text=f"{total_geral_2025}", x=0.5, y=0.5, font_size=24, showarrow=False)
    fig_pie.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")
st.info("💡 Este dashboard utiliza Plotly, permitindo que você passe o mouse sobre os gráficos para ver os detalhes exatos.")
