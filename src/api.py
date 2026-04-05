from fastapi import FastAPI
from sqlalchemy import create_engine
import pandas as pd
import os

from src.scraper import get_jobs

app = FastAPI()

DB_PATH = "data/jobs.db"
engine = create_engine(f"sqlite:///{DB_PATH}")


def initialize_database():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(DB_PATH):
        vacancies = get_jobs()

        df = pd.DataFrame(vacancies)

        df = df[df["title"].str.contains("Python", case=False)]

        df.to_sql("jobs", engine, if_exists="replace", index=False)


@app.on_event("startup")
def startup_event():
    initialize_database()


@app.get("/")
def home():
    return {"mensagem": "API de vagas rodando 🚀"}


@app.get("/jobs")
def get_all_jobs(title: str = None):
    query = "SELECT * FROM jobs"

    if title:
        query += f" WHERE title LIKE '%{title}%'"

    df = pd.read_sql(query, engine)
    return df.to_dict(orient="records")