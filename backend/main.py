import os

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI
from psycopg.rows import dict_row

load_dotenv()

app = FastAPI()


def get_connection():
    return psycopg.connect(os.getenv("DATABASE_URL"), row_factory=dict_row)


@app.get("/")
def home():
    return {"message": "Hello, Job Tracker!"}


@app.get("/applications")
def get_applications():
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT applications.id, companies.name AS company,
                   applications.role, applications.status
            FROM applications
            JOIN companies ON applications.company_id = companies.id
            ORDER BY applications.id
            """
        ).fetchall()
    return rows