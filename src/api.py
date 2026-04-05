from fastapi import FastAPI
from sqlalchemy import create_engine
import pandas as pd

app = FastAPI()

engine = create_engine("sqlite:///data/jobs.db")

@app.get("/")
def home():
    return {"mensagem": "API de vagas rodando 🚀"}

@app.get("/jobs")
def get_jobs(title: str = None):
    query = "SELECT * FROM jobs"

    if title:
        query += f" WHERE title LIKE '%{title}%'"

    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")