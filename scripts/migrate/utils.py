import os
import psycopg2

def create_db_conn():
    print("Creating database connection...")
    
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
