import os,sys,importlib,re,json
import psycopg2

from . import constants, utils

def execute(db_conn, opts={}, args=[]):
    print("[PROCESSING] Preparing to execute migration files...")
    
    migration_queue = get_migrations_queue(db_conn)
    
    print("[PROCESSING] Found {} migration file/s".format(len(migration_queue)))
    
    persist_schema_modifications(db_conn, migration_queue)

def get_migrations_queue(db_conn):
    past_migrations = get_migration_records(db_conn)
    
    file_queue = [
        re.search(r"^(.+)\.json$", file).group(1) for file in os.listdir(constants.MIGRATIONS_PATH) if os.path.isfile(os.path.join(constants.MIGRATIONS_PATH, file))
    ]
    
    return list(set(file_queue) - set(past_migrations))


def get_migration_records(db_conn):
    past_migrations = []
    
    try:
        with db_conn.cursor() as cur:
            cur.execute("SELECT * FROM schema_migrations")
            past_migrations = list(map(lambda record: record[0], cur.fetchall()))
            db_conn.commit()
            
    except psycopg2.errors.DatabaseError as excp:
            print("[ERROR] Failed to retrieve migration records!")
            db_conn.rollback()
    
    return past_migrations

def read_migration_file(file_path):
    file = open(file_path, 'r')
    queries = json.load(file)
        
    file.close()

    return queries

def persist_schema_modifications(db_conn, queue):
    if not len(queue):
        print("[ERROR] No files to migrate. Exiting...")
        
        return
    
    for filename in queue:
        print("[PROCESSING] Migrating {}...".format(filename))
        
        migration_queries = utils.read_migration_file(filename)
        
        if not migration_queries["up"]:
            print("[ERROR] Cannot process current migration file: Empty query string.")
            continue
        
        execute_modification(db_conn, migration_queries["up"], filename)

def execute_modification(db_conn, query, mig_filename):
    
    try:
        with db_conn.cursor() as cur:
            cur.execute(query)
            cur.execute("INSERT INTO schema_migrations (name) VALUES (%s);", (mig_filename,))
            
            db_conn.commit()

        print("[SUCCESS] {} succesfully migrated!".format(mig_filename))
    except psycopg2.errors.DatabaseError as excp:
        print("[ERROR]", repr(excp))
        print("[ERROR] Migrating {} encountered an error!".format(mig_filename))
        db_conn.rollback()

