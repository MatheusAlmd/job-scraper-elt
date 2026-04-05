import pandas as pd
import os
from sqlalchemy import create_engine
from src.scraper import get_jobs

# pega os dados
vacancies = get_jobs()

df = pd.DataFrame(vacancies)

# filtro
df = df[df["title"].str.contains("Python", case=False)]

# garante pasta
os.makedirs("data", exist_ok=True)

# salva CSV
df.to_csv("data/vagas_python.csv", index=False, quoting=1)

# banco
engine = create_engine("sqlite:///data/jobs.db")

# salva no banco
df.to_sql("jobs", engine, if_exists="replace", index=False)

# Ler do banco
df_from_db = pd.read_sql("SELECT * FROM jobs LIMIT 5", engine)

print("\nDados vindos do banco:")
print(df_from_db)

print("\nPipeline completo com leitura do banco!")