# Importa ferramentas para lidar com caminhos de arquivos
from pathlib import Path

# FastAPI = framework para criar APIs
from fastapi import FastAPI

# SQLAlchemy = conecta Python com banco de dados
from sqlalchemy import create_engine, text

# Pandas = manipulação de dados (tabela)
import pandas as pd

# Importa função que faz o scraping
from src.scraper import get_jobs

# Cria a aplicação da API
app = FastAPI()

# Define o caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Define pasta de dados
DATA_DIR = BASE_DIR / "data"

# Define caminho do banco SQLite
DB_PATH = DATA_DIR / "jobs.db"

# Cria conexão com banco
engine = create_engine(f"sqlite:///{DB_PATH}")


# Função para criar banco se não existir
def initialize_database():
    # Cria pasta data se não existir
    DATA_DIR.mkdir(exist_ok=True)

    # Verifica se a tabela "jobs" já existe
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='jobs'")
        ).fetchone()

    # Se não existir, cria banco com scraping
    if result is None:
        vacancies = get_jobs()  # coleta dados

        df = pd.DataFrame(vacancies)  # transforma em tabela

        # salva no banco
        df.to_sql("jobs", engine, if_exists="replace", index=False)


# Executa quando a API inicia
@app.on_event("startup")
def startup_event():
    initialize_database()


# Endpoint raiz (teste)
@app.get("/")
def home():
    return {"mensagem": "API de vagas rodando 🚀"}


# Endpoint principal
@app.get("/jobs")
def get_all_jobs(title: str = None):
    # garante que banco existe
    initialize_database()

    query = "SELECT * FROM jobs"
    params = {}

    # Se usuário pesquisar algo
    if title:
        query += " WHERE lower(title) LIKE lower(:title)"
        params["title"] = f"%{title}%"

    # executa consulta
    df = pd.read_sql(text(query), engine, params=params)

    # retorna em formato JSON
    return df.to_dict(orient="records")