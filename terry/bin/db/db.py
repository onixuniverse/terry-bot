import psycopg2

from terry.resources.data.tokens.db_keys import dbHost, dbName, dbPass, dbUser

conn = psycopg2.connect(
    database=dbName,
    user=dbUser,
    password=dbPass,
    host=dbHost
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
