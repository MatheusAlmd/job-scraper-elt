# Biblioteca para manipular arquivos e pastas
import os

# Pandas = trabalhar com dados
import pandas as pd

# SQLAlchemy = banco de dados
from sqlalchemy import create_engine

# Importa função do scraper
from src.scraper import get_jobs

# Coleta vagas do site
vacancies = get_jobs()

# Transforma lista em tabela
df = pd.DataFrame(vacancies)

# Cria pasta data se não existir
os.makedirs("data", exist_ok=True)

# Salva em CSV (arquivo tipo Excel)
df.to_csv("data/vagas.csv", index=False, quoting=1)

# Cria banco SQLite
engine = create_engine("sqlite:///data/jobs.db")

# Salva dados no banco
df.to_sql("jobs", engine, if_exists="replace", index=False)

# Lê 5 registros do banco para teste
df_from_db = pd.read_sql("SELECT * FROM jobs LIMIT 5", engine)

print("\nDados vindos do banco:")
print(df_from_db)

print("\nPipeline completo com todas as vagas!")