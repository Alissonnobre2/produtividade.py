import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração e Estilo (Azul Profissional)
st.set_page_config(page_title="Dashboard Produtividade Equipe", layout="wide")

azul_fundo = "#0E1117"
azul_card = "#1B1E26"
azul_texto = "#E0E0E0"
# Paleta de azuis para as 3 pessoas
cores_equipe = {"Amanda": "#8ECAE6", "Alisson": "#0072FF", "Gabriele": "#00C6FF"}

st.markdown(f"""
<style>
    .stApp {{ background-color: {azul_fundo}; color: {azul_texto}; }}
    .stMetric {{ background-color: {azul_card}; padding: 15px; border-radius: 10px; border: 1px solid #2D3139; }}
    [data-testid="stMetricLabel"] {{ color: #8ECAE6 !important; }}
    h1, h2, h3 {{ color: #00C6FF !important; }}
</style>
""", unsafe_allow_html=True)

# --- 2. DADOS DE CIMA (FIXOS) ---
data_detalhado = {
    "Responsável": ["Alisson", "Alisson", "Alisson", "Amanda", "Amanda", "Amanda", "Gabriele", "Gabriele", "Gabriele"],
    "Categoria": ["Boleto", "Outros Poderes", "Rh Bahia", "Boleto", "Outros Poderes", "Rh Bahia", "Boleto", "Outros Poderes", "Rh Bahia"],
    "Quantidade": [12, 23, 29, 9, 3, 81, 68, 38, 58]
}
df_detalhado = pd.DataFrame(data_detalhado)

# --- 3. DADOS SEMANAIS (INDIVIDUAIS) ---
# Organizando os dados diários reais da sua planilha para 28 dias
datas = [f"{i:02d}/04" for i in range(1, 29)]
# Amanda
p1 = [7, 7, 0, 0, 0, 7, 3, 6, 4, 5, 2, 0, 3, 5, 6, 7, 3, 4, 0, 4, 2, 1, 7, 2, 2, 0, 3, 4]
# Alisson
p2 = [5, 4, 0, 0, 0, 2, 5, 6, 5, 0, 0, 0, 0, 3, 7, 8, 4, 0, 0, 2, 0, 3, 3, 1, 0, 0, 2, 3]
# Gabriele
p3 = [3, 0, 0, 0, 0, 9, 10, 11, 11, 10, 0, 0, 11, 8, 10, 8, 12, 0, 0, 5, 5, 9, 9, 4, 0, 0, 10, 11]

df_diaria = pd.DataFrame({
    "Data": datas,
    "Amanda": p1,
    "Alisson": p2,
    "Gabriele": p3,
    "Semana": ["Semana 1"]*7 + ["Semana 2"]*7 + ["Semana 3"]*7 + ["Semana 4"]*7
})

# --- 4. PARTE DE CIMA ---
st.title("📊 Demonstrativo de Produtividade - Equipe")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Geral", "321")
c2.metric("Líder", "Gabriele")
c3.metric("Foco", "Rh Bahia")
c4.metric("Status", "Em Dia")

st.markdown("---")
col_l, col_r = st.columns(2)
with col_l:
    st.subheader("Atividades por Responsável")
    fig_barra = px.bar(df_detalhado, x="Responsável", y="Quantidade", color="Categoria", text_auto=True, barmode="stack", 
                       color_discrete_sequence=["#004E92", "#0072FF", "#00C6FF"])
    fig_barra.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=azul_texto, height=300)
    st.plotly_chart(fig_barra, use_container_width=True)
with col_r:
    st.subheader("Distribuição por Setor")
    fig_pie = px.pie(df_detalhado, values="Quantidade", names="Categoria", hole=0.6, 
                     color_discrete_sequence=["#004E92", "#0072FF", "#00C6FF"])
    fig_pie.update_layout(paper_
