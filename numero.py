import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard de Produtividade - Abril", layout="wide")

# --- 1. BASE DE DADOS (Aqui você poderá adicionar os dados diários depois) ---
data_pessoas = {
    "Colaborador": ["Amanda", "Alisson", "Gabriele"],
    "Total": [96, 64, 164]
}

data_categorias = {
    "Categoria": ["Boleto", "RH Bahia", "Outros Poderes"],
    "Total": [89, 167, 64]
}

df_pessoas = pd.DataFrame(data_pessoas)
df_categorias = pd.DataFrame(data_categorias)

# --- 2. CABEÇALHO ---
st.title("📊 Demonstrativo de Produtividade - Abril 2025")
st.markdown("---")

# --- 3. MÉTRICAS EM DESTAQUE ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Geral", sum(data_pessoas["Total"]))
col2.metric("Líder do Mês", "Gabriele")
col3.metric("Setor mais Ativo", "RH Bahia")

st.markdown("---")

# --- 4. GRÁFICOS ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Produção por Colaborador")
    fig_bar = px.bar(
        df_pessoas, 
        x="Colaborador", 
        y="Total", 
        color="Colaborador",
        text_auto=True,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    st.subheader("Distribuição por Categoria")
    fig_pie = px.pie(
        df_categorias, 
        values="Total", 
        names="Categoria",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# --- 5. ESPAÇO PARA EXPANSÃO (Produtividade Diária / Comparações) ---
st.markdown("---")
st.subheader("📈 Próximos Passos: Produtividade Diária e Comparativo")
st.info("Nesta seção, poderemos carregar tabelas de 2023 e 2024 para gerar gráficos de linhas comparando o crescimento anual.")

# Exemplo de como ficaria uma tabela de dados brutos
if st.checkbox("Mostrar tabela de dados brutos"):
    st.write(df_pessoas)