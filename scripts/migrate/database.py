import os
import psycopg2

def create_db_conn():
    print("[PROCESSING] Creating database connection...")
    
    creds = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASS'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }
    
    try:
        return psycopg2.connect(**creds)
    except (
        psycopg2.errors.ConnectionException,
        psycopg2.errors.ConnectionFailure,
        psycopg2errors.TooManyConnections
    ) as conn_excp:
        print("[ERROR] Failed to create database connection!")
        print(conn_excp)

    return False

def init_migration(db_conn):
    if migration_table_exists(db_conn):
        print("[PROCESSING] Skipping schema_migrations table creation.")
    else:
        create_migration_table(db_conn)


def migration_table_exists(db_conn):
    print("[PROCESSING] Checking for migration table...")
    
    try:
        with db_conn.cursor() as cur:
            cur.execute("SELECT * FROM schema_migrations")
            db_conn.commit()
        
        print("[SUCCESS] Schema_migrations table exists.")
        return True
    except psycopg2.errors.UndefinedTable as excp:
        print("[ERROR] Schema_migrations table does not exist.")
        db_conn.rollback()
    
    return False

def create_migration_table(db_conn):
    print("Create schema_migrations table")
    
    try:
        with db_conn.cursor() as cur:
            cur.execute("CREATE TABLE schema_migrations (name VARCHAR(255));")
            db_conn.commit()
        
        print("[SUCCESS] Schema_migrations table has been created!")
    except (
        psycopg2.errors.DuplicateTable,
        psycopg2.errors.SyntaxError,
        psycopg2.errors.InvalidName,
        psycopg2.errors.InvalidColumnDefinition
    ) as excp:
        print("[ERROR]", repr(excp))
        print("[ERROR] Failed to create schema_migrations table.")
        
        db_conn.rollback()

