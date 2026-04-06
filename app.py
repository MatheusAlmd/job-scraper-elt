import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="Job Scraper Dashboard",
    page_icon="💼",
    layout="wide"
)

st.title("💼 Job Scraper ETL Dashboard")
st.write("Visualização simples e organizada das vagas coletadas.")

st.markdown("### Pesquise vagas")
st.caption("Exemplos de busca: Python, Java, HTML")

# conexão com banco local
conn = sqlite3.connect("data/jobs.db")

# botões
col1, col2, col3 = st.columns(3)

if "search_term" not in st.session_state:
    st.session_state.search_term = ""

if col1.button("Python"):
    st.session_state.search_term = "Python"

if col2.button("Java"):
    st.session_state.search_term = "Java"

if col3.button("HTML"):
    st.session_state.search_term = "HTML"

search_term = st.text_input(
    "Buscar vagas por título",
    value=st.session_state.search_term,
    placeholder="Ex: Python, Java, HTML"
)

# query SQL direto no banco
query = "SELECT * FROM jobs"

if search_term:
    query += f" WHERE lower(title) LIKE lower('%{search_term}%')"

df = pd.read_sql(query, conn)

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
    st.warning("Nenhuma vaga encontrada para esse termo.")