import psycopg2
from data.db_keys import dbHost, dbName, dbPass, dbUser
from discord.ext.commands.core import command

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
    
async def field(command, *values):
    cur.execute(command, tuple(values))
    
    if cur.fetchone:
        return cur.fetchone()[0]
    
async def record(command, *values):
    cur.execute(command, tuple(values))
    
    if cur.fetchone:
        return cur.fetchone()[0]

async def records(command, *values):
    cur.execute(command, tuple(values))
    
    return cur.fetchall()

async def execute(command, *values):
	cur.execute(command, tuple(values))
