import streamlit as st
import pandas as pd

# Importa a função que faz o scraping
from src.scraper import get_jobs

# Configuração da página
st.set_page_config(
    page_title="Job Scraper ETL Dashboard",
    page_icon="💼",
    layout="wide"
)

# Título e descrição
st.title("💼 Job Scraper ETL Dashboard")
st.write("Visualização simples e organizada das vagas coletadas.")

st.markdown("### Pesquise vagas")
st.caption("Exemplos de busca: Python, Java, HTML ou clique em All para ver todas.")

# Cria a variável da busca na sessão, para ela não sumir a cada clique
if "search_term" not in st.session_state:
    st.session_state.search_term = ""

# Cria 4 colunas para os botões
col1, col2, col3, col4 = st.columns(4)

# Botões rápidos de filtro
if col1.button("Python"):
    st.session_state.search_term = "Python"

if col2.button("Java"):
    st.session_state.search_term = "Java"

if col3.button("HTML"):
    st.session_state.search_term = "HTML"

# Botão para limpar o filtro e mostrar tudo
if col4.button("All"):
    st.session_state.search_term = ""

# Campo de texto para busca manual
search_term = st.text_input(
    "Buscar vagas por título",
    key="search_term",
    placeholder="Ex: Python, Java, HTML"
)

# Cacheia os dados por 1 hora para não fazer scraping toda hora
@st.cache_data(ttl=3600)
def load_jobs():
    jobs = get_jobs()
    return pd.DataFrame(jobs)

# Carrega todas as vagas
df = load_jobs()

# Se tiver busca digitada, filtra
if search_term:
    df = df[df["title"].str.contains(search_term, case=False, na=False)]

# Exibe os resultados
if not df.empty:
    st.metric("Total de vagas encontradas", len(df))

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Baixar vagas em CSV",
        data=csv,
        file_name="vagas_filtradas.csv",
        mime="text/csv"
    )
else:
    st.warning("Nenhuma vaga encontrada para esse termo neste dataset.")