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

# Título
st.title("💼 Job Scraper ETL Dashboard")
st.write("Visualização simples e organizada das vagas coletadas.")

st.markdown("### Pesquise vagas")
st.caption("Exemplos de busca: Python, Java, HTML")


# Guarda o termo de busca na sessão
if "search_term" not in st.session_state:
    st.session_state.search_term = ""


# Botões rápidos
col1, col2, col3 = st.columns(3)

if col1.button("Python"):
    st.session_state.search_term = "Python"

if col2.button("Java"):
    st.session_state.search_term = "Java"

if col3.button("HTML"):
    st.session_state.search_term = "HTML"


# Campo de busca
search_term = st.text_input(
    "Buscar vagas por título",
    value=st.session_state.search_term,
    placeholder="Ex: Python, Java, HTML"
)


# Cacheia os dados para não fazer scraping toda hora
@st.cache_data(ttl=3600)
def load_jobs():
    jobs = get_jobs()
    return pd.DataFrame(jobs)


# Carrega todas as vagas
df = load_jobs()


# Filtra se houver termo digitado
if search_term:
    df = df[df["title"].str.contains(search_term, case=False, na=False)]


# Exibe resultados
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