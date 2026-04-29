import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuração da página e Estilo Visual (Cores extraídas da sua imagem)
st.set_page_config(page_title="Dashboard Produtividade Azul", layout="wide")

# Cores da paleta: Azul Escuro, Azul Médio, Azul Turquesa, Cinza Azulado
azul_fundo = "#f8f8ec"
azul_card = "#1B1E26"
azul_texto = "#E0E0E0"
paleta_azul = ["#004E92", "#0072FF", "#00C6FF", "#3A86FF", "#8ECAE6"]

st.markdown(f"""
<style>
    .stApp {{
        background-color: {azul_fundo};
        color: {azul_texto};
    }}
    .stMetric {{
        background-color: {azul_card};
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #2D3139;
    }}
    [data-testid="stMetricLabel"] {{
        color: #8ECAE6 !important;
    }}
    h1, h2, h3 {{
        color: #00C6FF !important;
    }}
</style>
""", unsafe_allow_html=True)

# --- 2. DADOS ---
data_detalhado = {
    "Responsável": ["Alisson", "Alisson", "Alisson", "Amanda", "Amanda", "Amanda", "Gabriele", "Gabriele", "Gabriele"],
    "Categoria": ["Boleto", "Outros Poderes", "Rh Bahia", "Boleto", "Outros Poderes", "Rh Bahia", "Boleto", "Outros Poderes", "Rh Bahia"],
    "Quantidade": [12, 23, 29, 9, 3, 81, 68, 38, 58]
}
df_detalhado = pd.DataFrame(data_detalhado)

datas_abril = [f"{i:02d}/04" for i in range(1, 31)]
df_diaria = pd.DataFrame({
    "Data": datas_abril,
    "Amanda": [7, 7, 0, 0, 0, 7, 3, 6, 4, 5, 2, 0, 3, 5, 6, 7, 3, 4, 0, 4, 2, 1, 7, 2, 2, 0, 3, 4, 2, 0],
    "Alisson": [5, 4, 0, 0, 0, 2, 5, 6, 5, 0, 0, 0, 0, 3, 7, 8, 4, 0, 0, 2, 0, 3, 3, 1, 0, 0, 2, 3, 1, 0],
    "Gabriele": [3, 0, 0, 0, 0, 9, 10, 11, 11, 10, 0, 0, 11, 8, 10, 8, 12, 0, 0, 5, 5, 9, 9, 4, 0, 0, 10, 11, 8, 0]
}).melt(id_vars=["Data"], var_name="Colaborador", value_name="Produção")

# --- 3. CABEÇALHO E MÉTRICAS ---
st.title("📊 Demonstrativo de Produtividade - Equipe")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Geral", "321")
c2.metric("Líder", "Gabriele")
c3.metric("Foco", "Rh Bahia")
c4.metric("Status", "Em Dia")

st.markdown("---")

# --- 4. GRÁFICOS SUPERIORES ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Atividades por Responsável")
    fig_barra = px.bar(
        df_detalhado, x="Responsável", y="Quantidade", color="Categoria",
        text_auto=True, barmode="stack",
        color_discrete_sequence=paleta_azul
    )
    fig_barra.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=azul_texto, height=350)
    st.plotly_chart(fig_barra, use_container_width=True)

with col_right:
    st.subheader("Distribuição por Setor")
    fig_pie = px.pie(
        df_detalhado, values="Quantidade", names="Categoria", hole=0.6,
        color_discrete_sequence=paleta_azul
    )
    fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color=azul_texto, height=350)
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# --- 5. GRÁFICO DIÁRIO (AZUL DINÂMICO) ---
st.subheader("📈 Evolução Diária da Produtividade")
fig_diaria = px.line(
    df_diaria, x="Data", y="Produção", color="Colaborador",
    markers=True, line_shape="spline",
    color_discrete_sequence=["#00C6FF", "#0072FF", "#8ECAE6"]
)
fig_diaria.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)', 
    font_color=azul_texto,
    height=380,
    xaxis={'tickangle': 45},
    hovermode="x unified"
)
fig_diaria.update_xaxes(showgrid=False)
fig_diaria.update_yaxes(showgrid=True, gridcolor="#2D3139")

st.plotly_chart(fig_diaria, use_container_width=True)
