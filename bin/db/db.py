import psycopg2
from discord.ext.commands.core import command

from bin.bot.db_keys import dbName, dbUser, dbPass, dbHost


conn = psycopg2.connect(
    database=dbName,
    user=dbUser,
    password=dbPass,
    host=dbHost
)

cur = conn.cursor()


def commit():
    conn.commit()
    
def close():
    conn.close()
    
def field(command, *values):
    cur.execute(command, tuple(values))
    
    if (fetch := cur.fetchone()):
        return fetch[0]
    
def record(command, *values):
    cur.execute(command, tuple(values))
    
    return cur.fetchone()

def records(command, *values):
    cur.execute(command, tuple(values))
    
    return cur.fetchall()
