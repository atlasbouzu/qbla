import os,sys,importlib,re,json
import psycopg2

from . import constants

def execute(db_conn, opts={}, args=[]):
    print("[PROCESSING] Preparing to execute migration files...")
    
    print("Executing down queries from migrations...")
    migration_history = get_migration_history(db_conn)
    print(migration_history)


def get_migration_history(db_conn):
    past_migrations = []
    
    try:
        with db_conn.cursor() as cur:
            cur.execute("SELECT * FROM schema_migrations ORDER BY name DESC")
            past_migrations = list(map(lambda record: record[0], cur.fetchall()))
            db_conn.commit()
    except:
        db_conn.rollback()

    return past_migrations
