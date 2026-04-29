import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração
st.set_page_config(page_title="Dashboard Produtividade Bruta", layout="wide")

# --- DADOS DA PLANILHA (PRODUTIVIDADE DIÁRIA) ---
# Extraímos os números reais que você enviou para o mês de Abril/2025
datas_abril = pd.date_range(start="2026-04-01", periods=30)
df_diaria = pd.DataFrame({
    "Data": datas_abril,
    "Amanda": [7, 7, 0, 0, 0, 7, 3, 6, 4, 5, 2, 0, 3, 5, 6, 7, 3, 4, 0, 4, 2, 1, 7, 2, 2, 0, 3, 4, 2, 0],
    "Alisson": [5, 4, 0, 0, 0, 2, 5, 6, 5, 0, 0, 0, 0, 3, 7, 8, 4, 0, 0, 2, 0, 3, 3, 1, 0, 0, 2, 3, 1, 0],
    "Gabriele": [3, 0, 0, 0, 0, 9, 10, 11, 11, 10, 0, 0, 11, 8, 10, 8, 12, 0, 0, 5, 5, 9, 9, 4, 0, 0, 10, 11, 8, 0]
})

# Transformar dados para o formato de gráfico (Melt)
df_plot = df_diaria.melt(id_vars=["Data"], var_name="Colaborador", value_name="Produção")

# --- INTERFACE ---
st.title("🚀 Análise de Produtividade Bruta - Abril")
st.markdown("---")

# Linha de KPIS (Os cartões de cima)
c1, c2, c3 = st.columns(3)
c1.metric("Total de Registros", "324")
c2.metric("Pico de Produção (Dia)", "23 registros")
c3.metric("Média Diária Equipe", "10.8")

st.markdown("---")

# GRÁFICO DE ÁREA DINÂMICO
st.subheader("📈 Evolução da Produtividade Diária (Bruta)")
fig_area = px.area(
    df_plot, 
    x="Data", 
    y="Produção", 
    color="Colaborador",
    title="Volume de Trabalho Acumulado por Dia",
    line_group="Colaborador",
    color_discrete_map={"Amanda": "#FF9999", "Alisson": "#66B3FF", "Gabriele": "#99FF99"},
    symbol="Colaborador"
)

fig_area.update_layout(
    hovermode="x unified",
    yaxis_title="Quantidade de Processos",
    xaxis_title="Dias de Abril",
    legend_title="Equipe"
)

st.plotly_chart(fig_area, use_container_width=True)
