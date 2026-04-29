import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(page_title="Dashboard de Produtividade - Abril", layout="wide")

# Estilização CSS
st.markdown("""
<style>
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        border: 1px solid #e6e9ef;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Demonstrativo de Produtividade - Abril")
st.markdown("---")

# --- 1. DADOS ---
# Dados de volume por pessoa e setor
data_detalhado = {
    "Responsável": ["Alisson", "Alisson", "Alisson", "Amanda", "Amanda", "Amanda", "Gabriele", "Gabriele", "Gabriele"],
    "Categoria": ["Boleto", "Outros Poderes", "Rh Bahia", "Boleto", "Outros Poderes", "Rh Bahia", "Boleto", "Outros Poderes", "Rh Bahia"],
    "Quantidade": [12, 23, 29, 9, 3, 81, 68, 38, 58]
}
df_detalhado = pd.DataFrame(data_detalhado)

# Dados de Produtividade Diária (Bruta)
datas_abril = [f"{i:02d}/04" for i in range(1, 31)]
prod_amanda = [7, 7, 0, 0, 0, 7, 3, 6, 4, 5, 2, 0, 3, 5, 6, 7, 3, 4, 0, 4, 2, 1, 7, 2, 2, 0, 3, 4, 2, 0]
prod_alisson = [5, 4, 0, 0, 0, 2, 5, 6, 5, 0, 0, 0, 0, 3, 7, 8, 4, 0, 0, 2, 0, 3, 3, 1, 0, 0, 2, 3, 1, 0]
prod_gabriele = [3, 0, 0, 0, 0, 9, 10, 11, 11, 10, 0, 0, 11, 8, 10, 8, 12, 0, 0, 5, 5, 9, 9, 4, 0, 0, 10, 11, 8, 0]

df_diaria = pd.DataFrame({
    "Data": datas_abril,
    "Amanda": prod_amanda,
    "Alisson": prod_alisson,
    "Gabriele": prod_gabriele
})
df_diaria_melt = df_diaria.melt(id_vars=["Data"], var_name="Colaborador", value_name="Produção")

# --- 2. LINHA DE KPIS ---
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
total_geral = df_detalhado["Quantidade"].sum()
col_kpi1.metric(label="Total Geral (2025)", value=total_geral)
col_kpi2.metric(label="Líder do Mês", value="Gabriele")
col_kpi3.metric(label="Setor mais Ativo", value="Rh Bahia")
col_kpi4.metric(label="Crescimento vs 2024", value="1505%")

st.markdown("---")

# --- 3. LINHA DE GRÁFICOS (DETALHADO E CATEGORIA) ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("O que cada um fez?")
    fig_barra = px.bar(
        df_detalhado, x="Responsável", y="Quantidade", color="Categoria",
        text_auto=True, barmode="stack",
        color_discrete_map={"Boleto": "#EF553B", "Rh Bahia": "#636EFA", "Outros Poderes": "#00CC96"}
    )
    fig_barra.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_barra, use_container_width=True)

with col_right:
    st.subheader("Volume por Categoria")
    fig_pie = px.pie(
        df_detalhado, values="Quantidade", names="Categoria", hole=0.5,
        color_discrete_map={"Boleto": "#EF553B", "Rh Bahia": "#636EFA", "Outros Poderes": "#00CC96"}
    )
    fig_pie.add_annotation(text=f"{total_geral}", x=0.5, y=0.5, font_size=20, showarrow=False)
    fig_pie.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

#
