import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração inicial
st.set_page_config(page_title="Dashboard de Produtos de Inovação", layout="wide")
st.title("Dashboard de Produtos de Inovação")
st.markdown("### Análise das Invenções por Tipo de Propriedade Intelectual e Área de Conhecimento")

#CSS personalizado
st.markdown("""
    <style>
    .reportview-container {
        background-color: #f0f2f6;
    }
    .css-1aumxhk, .css-1d391kg {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 20px;
    }
    .st-dc {
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Carregar o dataset diretamente
dataset_path = "pro-xlsx-produtos-de-inovacao.xlsx"
try:
    df = pd.read_excel(dataset_path, engine="openpyxl")
except FileNotFoundError:
    st.error(f"Erro: O arquivo '{dataset_path}' não foi encontrado. Verifique o caminho.")
    st.stop()

# Resumo estatístico
st.sidebar.header("📊 Resumo Estatístico")
st.sidebar.write(f"**Total de registros:** {len(df)}")
st.sidebar.write(f"**Tipos de PI únicos:** {df['tipo_pi'].nunique()}")
st.sidebar.write(f"**Centros/Unidades únicas:** {df['centro/unidade'].nunique()}")
st.sidebar.write(f"**Grandes Áreas únicas:** {df['grande_area_conhecimento'].nunique()}")

# Dividindo o layout em duas colunas
col1, col2 = st.columns(2)

# Gráfico interativo 1: Tipo de Propriedade Intelectual
with col1:
    st.subheader("Distribuição por Tipo de Propriedade Intelectual")
    tipo_pi_counts = df["tipo_pi"].value_counts()
    fig_tipo_pi = px.bar(
        tipo_pi_counts, 
        x=tipo_pi_counts.index, 
        y=tipo_pi_counts.values,
        labels={"x": "Tipo de PI", "y": "Quantidade"},
        title="Tipo de Propriedade Intelectual",
        color=tipo_pi_counts.index,
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    st.plotly_chart(fig_tipo_pi, use_container_width=True)

# Gráfico interativo 2: Grande Área de Conhecimento
with col2:
    st.subheader("Distribuição por Grande Área de Conhecimento")
    grande_area_counts = df["grande_area_conhecimento"].value_counts()
    fig_grande_area = px.bar(
        grande_area_counts, 
        x=grande_area_counts.index, 
        y=grande_area_counts.values,
        labels={"x": "Grande Área", "y": "Quantidade"},
        title="Grande Área de Conhecimento",
        color=grande_area_counts.index,
        color_discrete_sequence=px.colors.sequential.Plasma
    )
    st.plotly_chart(fig_grande_area, use_container_width=True)

# Gráfico de barras agrupadas
st.subheader("Quantidade de Invenções por Unidade e Tipo de PI")
fig_unidade_tipo = px.histogram(
    df, 
    x="centro/unidade", 
    color="tipo_pi", 
    title="Invenções por Unidade e Tipo de Propriedade Intelectual",
    labels={"x": "Centro/Unidad", "y": "Quantidade", "color": "Tipo de PI"},
    barmode="group",
    color_discrete_sequence=px.colors.sequential.Viridis
)
fig_unidade_tipo.update_layout(xaxis={'categoryorder': 'total ascending'})
st.plotly_chart(fig_unidade_tipo, use_container_width=True)

# Filtros interativos
st.subheader("Filtragem de Dados")
filtro_unidade = st.multiselect("Selecione Centro/Unidade:", df["centro/unidade"].unique())
filtro_tipo_pi = st.multiselect("Selecione Tipo de Propriedade Intelectual:", df["tipo_pi"].unique())

# Aplicar os filtros
filtro_df = df.copy()
if filtro_unidade:
    filtro_df = filtro_df[filtro_df["centro/unidade"].isin(filtro_unidade)]
if filtro_tipo_pi:
    filtro_df = filtro_df[filtro_df["tipo_pi"].isin(filtro_tipo_pi)]

# Exibir tabela filtrada
if not filtro_df.empty:
    st.dataframe(filtro_df)
else:
    st.warning("Nenhum dado encontrado com os filtros selecionados.")

# Botão de download dos dados filtrados
st.subheader("Baixar Dados Filtrados")
csv = filtro_df.to_csv(index=False).encode("utf-8")
st.download_button("Baixar como CSV", data=csv, file_name="dados_filtrados.csv", mime="text/csv")
