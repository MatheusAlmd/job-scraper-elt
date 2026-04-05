from pathlib import Path

from fastapi import FastAPI
from sqlalchemy import create_engine, text
import pandas as pd

from src.scraper import get_jobs

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "jobs.db"

engine = create_engine(f"sqlite:///{DB_PATH}")


def initialize_database():
    DATA_DIR.mkdir(exist_ok=True)

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='jobs'")
        ).fetchone()

    if result is None:
        vacancies = get_jobs()
        df = pd.DataFrame(vacancies)

        if not df.empty:
            df = df[df["title"].str.contains("Python", case=False, na=False)]

        df.to_sql("jobs", engine, if_exists="replace", index=False)


@app.on_event("startup")
def startup_event():
    initialize_database()


@app.get("/")
def home():
    return {"mensagem": "API de vagas rodando 🚀"}


@app.get("/jobs")
def get_all_jobs(title: str = None):
    initialize_database()

    query = "SELECT * FROM jobs"
    params = {}

    if title:
        query += " WHERE lower(title) LIKE lower(:title)"
        params["title"] = f"%{title}%"

    df = pd.read_sql(text(query), engine, params=params)
    return df.to_dict(orient="records")