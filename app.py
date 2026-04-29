import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração e Estilo (Mantendo o que você já aprovou)
st.set_page_config(page_title="Dashboard Produtividade Azul", layout="wide")

azul_fundo = "#0E1117"
azul_card = "#1B1E26"
azul_texto = "#E0E0E0"
paleta_azul = ["#004E92", "#0072FF", "#00C6FF", "#3A86FF", "#8ECAE6"]

st.markdown(f"""
<style>
    .stApp {{ background-color: {azul_fundo}; color: {azul_texto}; }}
    .stMetric {{ background-color: {azul_card}; padding: 15px; border-radius: 10px; border: 1px solid #2D3139; }}
    [data-testid="stMetricLabel"] {{ color: #8ECAE6 !important; }}
    h1, h2, h3 {{ color: #00C6FF !important; }}
</style>
""", unsafe_allow_html=True)

# --- 2. DADOS (CIMA) ---
data_detalhado = {
    "Responsável": ["Alisson", "Alisson", "Alisson", "Amanda", "Amanda", "Amanda", "Gabriele", "Gabriele", "Gabriele"],
    "Categoria": ["Boleto", "Outros Poderes", "Rh Bahia", "Boleto", "Outros Poderes", "Rh Bahia", "Boleto", "Outros Poderes", "Rh Bahia"],
    "Quantidade": [12, 23, 29, 9, 3, 81, 68, 38, 58]
}
df_detalhado = pd.DataFrame(data_detalhado)

# --- 3. DADOS SEMANAIS (BAIXO) ---
# Simulando os 28 dias divididos em 4 semanas para o gráfico
datas = [f"{i:02d}/04" for i in range(1, 29)]
vendas = [7, 5, 3, 8, 2, 4, 6, 9, 10, 12, 5, 3, 4, 7, 8, 11, 15, 9, 6, 4, 3, 7, 8, 10, 12, 5, 4, 6]

df_semanal = pd.DataFrame({
    "Data": datas,
    "Produção": vendas,
    "Semana": ["Semana 1"]*7 + ["Semana 2"]*7 + ["Semana 3"]*7 + ["Semana 4"]*7
})

# --- 4. PARTE DE CIMA (NÃO MEXEMOS) ---
st.title("📊 Demonstrativo de Produtividade - Equipe")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Geral", "321")
c2.metric("Líder", "Gabriele")
c3.metric("Foco", "Rh Bahia")
c4.metric("Status", "Em Dia")

st.markdown("---")
col_left, col_right = st.columns(2)
with col_left:
    st.subheader("Atividades por Responsável")
    fig_barra = px.bar(df_detalhado, x="Responsável", y="Quantidade", color="Categoria", text_auto=True, barmode="stack", color_discrete_sequence=paleta_azul)
    fig_barra.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color=azul_texto, height=300)
    st.plotly_chart(fig_barra, use_container_width=True)
with col_right:
    st.subheader("Distribuição por Setor")
    fig_pie = px.pie(df_detalhado, values="Quantidade", names="Categoria", hole=0.6, color_discrete_sequence=paleta_azul)
    fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color=azul_texto, height=300)
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# --- 5. PARTE DE BAIXO (MODIFICADA: 4 GRÁFICOS EM LINHA RETA) ---
st.subheader("📈 Evolução de Produtividade por Semana")

# Criamos 4 colunas para os 4 gráficos
cols_semanas = st.columns(4)

semanas = ["Semana 1", "Semana 2", "Semana 3", "Semana 4"]

for i, sem in enumerate(semanas):
    with cols_semanas[i]:
        df_fatia = df_semanal[df_semanal["Semana"] == sem]
        
        # Gráfico de linha reta (sem spline)
        fig_sem = px.line(
            df_fatia, x="Data", y="Produção", 
            title=sem,
            markers=True
        )
        
        # Estilização para ficar idêntico à imagem (Linha azul neon e pontos)
        fig_sem.update_traces(line_color="#00C6FF", line_shape="linear", line_width=3)
        fig_sem.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)', 
            font_color=azul_texto,
            height=250,
            xaxis_title=None,
            yaxis_title=None,
            margin=dict(l=10, r=10, t=40, b=10)
        )
        fig_sem.update_xaxes(showgrid=False, color="#555")
        fig_sem.update_yaxes(showgrid=True, gridcolor="#2D3139", color="#555")
        
        st.plotly_chart(fig_sem, use_container_width=True)
