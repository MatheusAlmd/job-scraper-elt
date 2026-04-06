# Streamlit = interface web simples
import streamlit as st

# Pandas = manipulação de dados
import pandas as pd

# Requests = faz requisições HTTP
import requests

# URL da API online
API_URL = "https://job-scraper-elt.onrender.com/jobs"

# Configuração da página
st.set_page_config(
    page_title="Job Scraper Dashboard",
    page_icon="💼",
    layout="wide"
)

# Título principal
st.title("💼 Job Scraper ETL Dashboard")

# Descrição
st.write("Visualização simples e organizada das vagas coletadas pela API.")

# Texto explicativo
st.markdown("### Pesquise vagas")
st.caption("Exemplos de busca: Python, Java, HTML")

# Cria 3 colunas para botões rápidos
col1, col2, col3 = st.columns(3)

# Guarda valor digitado
if "search_term" not in st.session_state:
    st.session_state.search_term = ""

# Botões de busca rápida
if col1.button("Python"):
    st.session_state.search_term = "Python"

if col2.button("Java"):
    st.session_state.search_term = "Java"

if col3.button("HTML"):
    st.session_state.search_term = "HTML"

# Campo de texto
search_term = st.text_input(
    "Buscar vagas por título",
    value=st.session_state.search_term,
    placeholder="Ex: Python, Java, HTML"
)

# Função para chamar API
def load_jobs(title=None):
    try:
        if title:
            response = requests.get(API_URL, params={"title": title}, timeout=30)
        else:
            response = requests.get(API_URL, timeout=30)

        response.raise_for_status()

        return response.json(), None

    except requests.exceptions.RequestException as e:
        return None, f"Erro ao conectar com a API: {e}"


# Chama função
jobs, error = load_jobs(search_term if search_term else None)

# Se erro
if error:
    st.error(error)

# Se sucesso
else:
    if jobs:
        df = pd.DataFrame(jobs)

        # Mostra quantidade
        st.metric("Total de vagas encontradas", len(df))

        # Mostra tabela
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        # Botão de download
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Baixar vagas em CSV",
            data=csv,
            file_name="vagas_filtradas.csv",
            mime="text/csv"
        )

    else:
        st.warning("Nenhuma vaga encontrada para esse termo neste dataset.")