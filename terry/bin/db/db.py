import os
import psycopg2

from dotenv import load_dotenv

load_dotenv()


conn = psycopg2.connect(
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    host=os.getenv("DB_HOST")
)

cur = conn.cursor()


async def commit():
    conn.commit()


async def close():
    conn.close()


async def record(command, *values):
    cur.execute(command, tuple(values))

    try:
        return cur.fetchone()[0]
    except Exception:
        return None


async def records(command, *values):
    cur.execute(command, tuple(values))

    try:
        return cur.fetchall()
    except Exception:
        return None


async def execute(command, *values):
    cur.execute(command, tuple(values))
