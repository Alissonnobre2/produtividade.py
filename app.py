import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração da Página e Estilo (Tema Claro e Visível)
st.set_page_config(page_title="Dashboard Produtividade - Março", layout="wide")

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

# --- 2. DADOS DE MARÇO ---
cores_equipe = {"Amanda": "#EC4899", "Alisson": "#3B82F6", "Gabriele": "#10B981"}
cores_categorias = ["#6366F1", "#F59E0B", "#8B5CF6"]

data_detalhado_marco = {
    "Responsável": ["Alisson", "Alisson", "Alisson", "Amanda", "Amanda", "Amanda", "Gabriele", "Gabriele", "Gabriele"],
    "Categoria": ["Boleto", "Outros Poderes", "Rh Bahia", "Boleto", "Outros Poderes", "Rh Bahia", "Boleto", "Outros Poderes", "Rh Bahia"],
    "Quantidade": [25, 40, 85, 15, 10, 60, 45, 30, 70] 
}
df_detalhado = pd.DataFrame(data_detalhado_marco)

# Dados Diários Março (31 dias)
datas_marco = [f"{i:02d}/03" for i in range(1, 32)]
df_diaria = pd.DataFrame({
    "Data": datas_marco,
    "Amanda": [4,5,0,0,6,8,2, 3,4,0,0,5,7,3, 6,2,0,0,4,5,8, 3,5,0,0,4,6,2, 5,4,3],
    "Alisson": [2,3,0,0,4,5,7, 8,2,0,0,3,4,6, 5,7,0,0,2,3,4, 6,8,0,0,5,3,2, 4,6,5],
    "Gabriele": [1,2,0,0,10,12,5, 4,8,0,0,9,11,6, 3,10,0,0,12,8,4, 9,7,0,0,10,12,5, 8,9,10],
})

# Dividindo os 31 dias em 4 semanas
def definir_semana(dia):
    if dia <= 7: return "Semana 1"
    elif dia <= 14: return "Semana 2"
    elif dia <= 21: return "Semana 3"
    else: return "Semana 4"

df_diaria['DiaNum'] = range(1, 32)
df_diaria['Semana'] = df_diaria['DiaNum'].apply(definir_semana)

# --- 3. CABEÇALHO ---
st.title("📊 Demonstrativo de Produtividade - Março")
c1, c2, c3, c4 = st.columns(4)
total_marco = df_detalhado["Quantidade"].sum()
c1.metric("Total Março", f"{total_marco}")
c2.metric("Líder Março", "Gabriele")
c3.metric("Setor Crítico", "Rh Bahia")
c4.metric("Status", "Finalizado")

st.markdown("---")

# --- 4. GRÁFICOS SUPERIORES (MANTIDOS) ---
col_l, col_r = st.columns(2)
with col_l:
    st.subheader("Atividades por Responsável (Março)")
    fig_barra = px.bar(df_detalhado, x="Responsável", y="Quantidade", color="Categoria", 
                       text_auto=True, barmode="stack", color_discrete_sequence=cores_categorias)
    fig_barra.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=350)
    st.plotly_chart(fig_barra, use_container_width=True)

with col_r:
    st.subheader("Volume por Categoria (Março)")
    fig_pie = px.pie(df_detalhado, values="Quantidade", names="Categoria", hole=0.5, 
                     color_discrete_sequence=cores_categorias)
    fig_pie.update_layout(height=350)
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# --- 5. 4 GRÁFICOS SEMANAIS (AGORA EM BARRAS) ---
st.subheader("📈 Evolução Diária - Março (Por Semana)")
cols_semanas = st.columns(4)
semanas = ["Semana 1", "Semana 2", "Semana 3", "Semana 4"]

for i, sem in enumerate(semanas):
    with cols_semanas[i]:
        df_fatia = df_diaria[df_diaria["Semana"] == sem]
        df_fatia_melt = df_fatia.drop(columns='DiaNum').melt(id_vars=["Data", "Semana"], var_name="Colaborador", value_name="Produção")
        
        # Aqui está a mudança: px.bar e barmode="group"
        fig_sem = px.bar(df_fatia_melt, x="Data", y="Produção", color="Colaborador",
                         title=sem, color_discrete_map=cores_equipe, barmode="group")
        
        fig_sem.update_layout(
            plot_bgcolor='#FAFAFA', paper_bgcolor='white', height=300,
            xaxis_title=None, yaxis_title=None, showlegend=False,
            margin=dict(l=10, r=10, t=50, b=10),
            bargap=0.15 # Espaçamento entre os dias para ficar mais clean
        )
        fig_sem.update_yaxes(showgrid=True, gridcolor="#E5E7EB", range=[0, 15])
        st.plotly_chart(fig_sem, use_container_width=True)

# Legenda atualizada para combinar com gráficos de barra
st.markdown(f"""
    <div style='text-align: center; padding: 10px; background-color: #FFFFFF; border-radius: 8px; border: 1px solid #E5E7EB;'>
        <span style='color: {cores_equipe['Amanda']}; font-weight: bold;'>■ Amanda</span> &nbsp;&nbsp;&nbsp;&nbsp;
        <span style='color: {cores_equipe['Alisson']}; font-weight: bold;'>■ Alisson</span> &nbsp;&nbsp;&nbsp;&nbsp;
        <span style='color: {cores_equipe['Gabriele']}; font-weight: bold;'>■ Gabriele</span>
    </div>
""", unsafe_allow_html=True)
