import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração da Página e Estilo Clean
st.set_page_config(page_title="Dashboard Produtividade - Abril", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; color: #1F2937; }
    .stMetric {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        border: 1px solid #E5E7EB;
    }
    [data-testid="stMetricValue"] { color: #1E40AF !important; }
    h1, h2, h3 { color: #111827 !important; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# --- 2. DEFINIÇÃO DE CORES (SOLICITADO) ---
# Colaboradores
cores_equipe = {
    "Alisson": "#22C55E",   # Verde
    "Gabriele": "#EF4444",  # Vermelho
    "Amanda": "#3B82F6"     # Azul
}

# Categorias baseadas na paleta da foto enviada (Azuis e Roxo da imagem)
cores_categorias = {
    "Rh Bahia": "#5B21B6",        # Roxo escuro profundo
    "Boleto": "#1D4ED8",          # Azul Royal
    "Outros Poderes": "#60A5FA"   # Azul claro
}

# --- 3. DADOS DE ABRIL ---
data_detalhado_abril = {
    "Responsável": ["Alisson", "Alisson", "Alisson", "Amanda", "Amanda", "Amanda", "Gabriele", "Gabriele", "Gabriele"],
    "Categoria": ["Boleto", "Outros Poderes", "Rh Bahia", "Boleto", "Outros Poderes", "Rh Bahia", "Boleto", "Outros Poderes", "Rh Bahia"],
    "Quantidade": [12, 23, 29, 9, 3, 81, 68, 38, 58]
}
df_detalhado = pd.DataFrame(data_detalhado_abril)

# Dados Diários de Abril
datas_abril = [f"{i:02d}/04" for i in range(1, 31)]
df_diaria = pd.DataFrame({
    "Data": datas_abril,
    "Amanda": [7, 7, 0, 0, 0, 7, 3, 6, 4, 5, 2, 0, 3, 5, 6, 7, 3, 4, 0, 4, 2, 1, 7, 2, 2, 0, 3, 4, 5, 4],
    "Alisson": [5, 4, 0, 0, 0, 2, 5, 6, 5, 0, 0, 0, 0, 3, 7, 8, 4, 0, 0, 2, 0, 3, 3, 1, 0, 0, 2, 3, 4, 5],
    "Gabriele": [3, 0, 0, 0, 0, 9, 10, 11, 11, 10, 0, 0, 11, 8, 10, 8, 12, 0, 0, 5, 5, 9, 9, 4, 0, 0, 10, 11, 12, 10],
})

def definir_semana(dia):
    if dia <= 7: return "Semana 1"
    elif dia <= 14: return "Semana 2"
    elif dia <= 21: return "Semana 3"
    else: return "Semana 4"

df_diaria['DiaNum'] = range(1, 31)
df_diaria['Semana'] = df_diaria['DiaNum'].apply(definir_semana)

# --- 4. CABEÇALHO ---
st.title("📊 Demonstrativo de Produtividade - Abril")
c1, c2, c3, c4 = st.columns(4)
total_geral = df_detalhado["Quantidade"].sum()
c1.metric("Total Abril", f"{total_geral}")
c2.metric("Líder do Mês", "Gabriele")
c3.metric("Foco Setorial", "Rh Bahia")
c4.metric("Status", "Em Andamento")

st.markdown("---")

# --- 5. GRÁFICOS SUPERIORES ---
col_l, col_r = st.columns(2)
with col_l:
    st.subheader("Atividades por Responsável")
    fig_barra = px.bar(df_detalhado, x="Responsável", y="Quantidade", color="Categoria", 
                       text_auto=True, barmode="stack", color_discrete_map=cores_categorias)
    fig_barra.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=350)
    st.plotly_chart(fig_barra, use_container_width=True)

with col_r:
    st.subheader("Distribuição por Setor")
    fig_pie = px.pie(df_detalhado, values="Quantidade", names="Categoria", hole=0.5, 
                     color_discrete_map=cores_categorias)
    fig_pie.update_layout(height=350)
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# --- 6. 4 SEMANAS EM BARRAS AGRUPADAS ---
st.subheader("📈 Evolução Individual Diária - Abril (Por Semana)")
cols_semanas = st.columns(4)
semanas = ["Semana 1", "Semana 2", "Semana 3", "Semana 4"]

for i, sem in enumerate(semanas):
    with cols_semanas[i]:
        df_fatia = df_diaria[df_diaria["Semana"] == sem]
        df_fatia_melt = df_fatia.drop(columns='DiaNum').melt(id_vars=["Data", "Semana"], var_name="Colaborador", value_name="Produção")
        
        fig_sem = px.bar(df_fatia_melt, x="Data", y="Produção", color="Colaborador",
                         title=sem, color_discrete_map=cores_equipe, barmode="group")
        
        fig_sem.update_layout(
            plot_bgcolor='#FAFAFA', paper_bgcolor='white', height=300,
            xaxis_title=None, yaxis_title=None, showlegend=False,
            margin=dict(l=10, r=10, t=50, b=10),
            bargap=0.15
        )
        fig_sem.update_yaxes(showgrid=True, gridcolor="#E5E7EB", range=[0, 15])
        st.plotly_chart(fig_sem, use_container_width=True)

# Legenda Personalizada
st.markdown(f"""
    <div style='text-align: center; padding: 10px; background-color: #FFFFFF; border-radius: 8px; border: 1px solid #E5E7EB;'>
        <span style='color: {cores_equipe['Alisson']}; font-weight: bold;'>■ Alisson</span> &nbsp;&nbsp;&nbsp;&nbsp;
        <span style='color: {cores_equipe['Gabriele']}; font-weight: bold;'>■ Gabriele</span> &nbsp;&nbsp;&nbsp;&nbsp;
        <span style='color: {cores_equipe['Amanda']}; font-weight: bold;'>■ Amanda</span>
    </div>
""", unsafe_allow_html=True)
