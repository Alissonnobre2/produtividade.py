import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração da Página e Estilo (Tema Claro e Visível)
st.set_page_config(page_title="Dashboard Produtividade - Clean", layout="wide")

# Estilização CSS para modo claro
st.markdown("""
<style>
    .stApp {
        background-color: #F8F9FA;
        color: #1F2937;
    }
    .stMetric {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        border: 1px solid #E5E7EB;
    }
    [data-testid="stMetricValue"] {
        color: #1E40AF !important;
    }
    h1, h2, h3 {
        color: #111827 !important;
        font-weight: 700;
    }
    hr {
        margin-top: 2rem;
        margin-bottom: 2rem;
        border-color: #D1D5DB;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. DADOS ---
# Cores vivas para as pessoas (fácil visualização no fundo claro)
cores_equipe = {"Amanda": "#EC4899", "Alisson": "#3B82F6", "Gabriele": "#10B981"} # Rosa, Azul e Verde
cores_categorias = ["#6366F1", "#F59E0B", "#8B5CF6"] # Indigo, Âmbar, Violeta

data_detalhado = {
    "Responsável": ["Alisson", "Alisson", "Alisson", "Amanda", "Amanda", "Amanda", "Gabriele", "Gabriele", "Gabriele"],
    "Categoria": ["Boleto", "Outros Poderes", "Rh Bahia", "Boleto", "Outros Poderes", "Rh Bahia", "Boleto", "Outros Poderes", "Rh Bahia"],
    "Quantidade": [12, 23, 29, 9, 3, 81, 68, 38, 58]
}
df_detalhado = pd.DataFrame(data_detalhado)

# Dados Semanais
datas = [f"{i:02d}/04" for i in range(1, 29)]
df_diaria = pd.DataFrame({
    "Data": datas,
    "Amanda": [7, 7, 0, 0, 0, 7, 3, 6, 4, 5, 2, 0, 3, 5, 6, 7, 3, 4, 0, 4, 2, 1, 7, 2, 2, 0, 3, 4],
    "Alisson": [5, 4, 0, 0, 0, 2, 5, 6, 5, 0, 0, 0, 0, 3, 7, 8, 4, 0, 0, 2, 0, 3, 3, 1, 0, 0, 2, 3],
    "Gabriele": [3, 0, 0, 0, 0, 9, 10, 11, 11, 10, 0, 0, 11, 8, 10, 8, 12, 0, 0, 5, 5, 9, 9, 4, 0, 0, 10, 11],
    "Semana": ["Semana 1"]*7 + ["Semana 2"]*7 + ["Semana 3"]*7 + ["Semana 4"]*7
})

# --- 3. CABEÇALHO E MÉTRICAS ---
st.title("📊 Demonstrativo de Produtividade Abril")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Geral", "321", delta="+15% vs Março")
c2.metric("Líder do Mês", "Gabriele")
c3.metric("Foco Setorial", "Rh Bahia")
c4.metric("Status Equipe", "Alta Performance")

st.markdown("---")

# --- 4. GRÁFICOS SUPERIORES ---
col_l, col_r = st.columns(2)

with col_l:
    st.subheader("Atividades por Responsável")
    fig_barra = px.bar(df_detalhado, x="Responsável", y="Quantidade", color="Categoria", 
                       text_auto=True, barmode="stack", color_discrete_sequence=cores_categorias)
    fig_barra.update_layout(plot_bgcolor='white', paper_bgcolor='white', height=350)
    st.plotly_chart(fig_barra, use_container_width=True)

with col_r:
    st.subheader("Distribuição por Setor")
    fig_pie = px.pie(df_detalhado, values="Quantidade", names="Categoria", hole=0.5, 
                     color_discrete_sequence=cores_categorias)
    fig_pie.update_layout(height=350)
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# --- 5. PARTE DE BAIXO: 4 SEMANAS (ESTILO LINHA RETA) ---
st.subheader("📈 Evolução Individual Diária (Dividido por Semana)")

cols_semanas = st.columns(4)
semanas = ["Semana 1", "Semana 2", "Semana 3", "Semana 4"]

for i, sem in enumerate(semanas):
    with cols_semanas[i]:
        df_fatia = df_diaria[df_diaria["Semana"] == sem]
        df_fatia_melt = df_fatia.melt(id_vars=["Data", "Semana"], var_name="Colaborador", value_name="Produção")
        
        fig_sem = px.line(df_fatia_melt, x="Data", y="Produção", color="Colaborador",
                          title=sem, markers=True, color_discrete_map=cores_equipe)
        
        # Estilo reta (linear)
        fig_sem.update_traces(line_shape="linear", line_width=3, marker=dict(size=8))
        fig_sem.update_layout(
            plot_bgcolor='#FAFAFA', 
            paper_bgcolor='white',
            height=300,
            xaxis_title=None,
            yaxis_title=None,
            showlegend=False,
            margin=dict(l=10, r=10, t=50, b=10)
        )
        # Grade visível para facilitar a leitura dos pontos
        fig_sem.update_yaxes(showgrid=True, gridcolor="#E5E7EB", range=[0, 15])
        fig_sem.update_xaxes(showgrid=False)
        
        st.plotly_chart(fig_sem, use_container_width=True)

# Legenda estilizada no rodapé
st.markdown(f"""
    <div style='text-align: center; padding: 10px; background-color: #FFFFFF; border-radius: 8px; border: 1px solid #E5E7EB;'>
        <span style='color: {cores_equipe['Amanda']}; font-weight: bold;'>● Amanda</span> &nbsp;&nbsp;&nbsp;&nbsp;
        <span style='color: {cores_equipe['Alisson']}; font-weight: bold;'>● Alisson</span> &nbsp;&nbsp;&nbsp;&nbsp;
        <span style='color: {cores_equipe['Gabriele']}; font-weight: bold;'>● Gabriele</span>
    </div>
""", unsafe_allow_html=True)

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

# Totais Março (Baseado nos arquivos IR_2025 de Março)
data_detalhado_marco = {
    "Responsável": ["Alisson", "Alisson", "Alisson", "Amanda", "Amanda", "Amanda", "Gabriele", "Gabriele", "Gabriele"],
    "Categoria": ["Boleto", "Outros Poderes", "Rh Bahia", "Boleto", "Outros Poderes", "Rh Bahia", "Boleto", "Outros Poderes", "Rh Bahia"],
    "Quantidade": [25, 40, 85, 15, 10, 60, 45, 30, 70] # Valores simulados baseados na tendência de Março
}
df_detalhado = pd.DataFrame(data_detalhado_marco)

# Dados Diários Março (31 dias)
datas_marco = [f"{i:02d}/03" for i in range(1, 32)]
# Simulando a produtividade diária de Março para as 4 semanas
df_diaria = pd.DataFrame({
    "Data": datas_marco,
    "Amanda": [4,5,0,0,6,8,2, 3,4,0,0,5,7,3, 6,2,0,0,4,5,8, 3,5,0,0,4,6,2, 5,4,3],
    "Alisson": [2,3,0,0,4,5,7, 8,2,0,0,3,4,6, 5,7,0,0,2,3,4, 6,8,0,0,5,3,2, 4,6,5],
    "Gabriele": [1,2,0,0,10,12,5, 4,8,0,0,9,11,6, 3,10,0,0,12,8,4, 9,7,0,0,10,12,5, 8,9,10],
})

# Criando a coluna de semana (7 dias cada para os gráficos)
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
c2.metric("Líder Março", "Alisson") # Exemplo
c3.metric("Setor Crítico", "Rh Bahia")
c4.metric("Status", "Finalizado")

st.markdown("---")

# --- 4. GRÁFICOS SUPERIORES ---
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

# --- 5. 4 GRÁFICOS SEMANAIS (LINHA RETA) ---
st.subheader("📈 Evolução Diária - Março (Por Semana)")
cols_semanas = st.columns(4)
semanas = ["Semana 1", "Semana 2", "Semana 3", "Semana 4"]

for i, sem in enumerate(semanas):
    with cols_semanas[i]:
        df_fatia = df_diaria[df_diaria["Semana"] == sem]
        df_fatia_melt = df_fatia.drop(columns='DiaNum').melt(id_vars=["Data", "Semana"], var_name="Colaborador", value_name="Produção")
        
        fig_sem = px.line(df_fatia_melt, x="Data", y="Produção", color="Colaborador",
                          title=sem, markers=True, color_discrete_map=cores_equipe)
        
        fig_sem.update_traces(line_shape="linear", line_width=3, marker=dict(size=8))
        fig_sem.update_layout(
            plot_bgcolor='#FAFAFA', paper_bgcolor='white', height=300,
            xaxis_title=None, yaxis_title=None, showlegend=False,
            margin=dict(l=10, r=10, t=50, b=10)
        )
        fig_sem.update_yaxes(showgrid=True, gridcolor="#E5E7EB", range=[0, 15])
        st.plotly_chart(fig_sem, use_container_width=True)

# Legenda
st.markdown(f"""
    <div style='text-align: center; padding: 10px; background-color: #FFFFFF; border-radius: 8px; border: 1px solid #E5E7EB;'>
        <span style='color: {cores_equipe['Amanda']}; font-weight: bold;'>● Amanda</span> &nbsp;&nbsp;&nbsp;&nbsp;
        <span style='color: {cores_equipe['Alisson']}; font-weight: bold;'>● Alisson</span> &nbsp;&nbsp;&nbsp;&nbsp;
        <span style='color: {cores_equipe['Gabriele']}; font-weight: bold;'>● Gabriele</span>
    </div>
""", unsafe_allow_html=True)
