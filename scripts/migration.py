import sys,os
import psycopg2

from dotenv import load_dotenv

sys.path.append(os.path.join(sys.path[0], 'utils'))

from db import Database

def create_migration(dbConn, args_opts):
    print("Create migration file")

def up(dbConn, args_opts):
    dbConn.test("Execute up functions of migration files")

def down(dbConn, args_opts):
    dbConn.test("Execute down functions of migration files")

def migration_table_exists(dbConn):
    print("Checking for migration table...")
    
    try:
        with dbConn.cursor() as cur:
            cur.execute("SELECT * FROM schema_migrations")
            cur.commit()

        print("schema_migrations table exists.")
        return True
    except psycopg2.errors.UndefinedTable as excp:
        print("schema_migrations table does not exists.")
        dbConn.rollback()
    
    return False

def init_migration_table(dbConn):
    print("Create schema_migrations table")
    
    try:
        with dbConn.cursor() as cur:
            cur.execute("CREATE TABL schema_migrations (name VARCHAR(255));")
            dbConn.commit()
        
        print("schema_migrations table has been created!")
    except (
        psycopg2.errors.DuplicateTable,
        psycopg2.errors.SyntaxError,
        psycopg2.errors.InvalidName,
        psycopg2.errors.InvalidColumnDefinition
    ) as excp:
        print("Error: Failed to create schema_migrations table.")
        print(excp)
        dbConn.rollback()

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
        errors.ConnectionException,
        errors.ConnectionFailuer,
        errors.TooManyConnections
    ) as conn_excp:
        print("Failed to create database connection")
        print(excp)

    return False


def prep_db_ops(dbConn):
    if migration_table_exists(dbConn):
        print("Skipping schema_migrations table creation.")
    else:
        init_migration_table(dbConn)


#TODO: downができてからこれが次
def get_args_opts(args):
    return {}

def db_related(command):
    return command == "up" or command == "down"

def db_ops(command, args_opts):
    dbConn = create_db_conn()
    
    if not dbConn:
        sys.exit(1)
    
    prep_db_ops(dbConn)
    
    try:
        if command == "up":
            up(dbConn, args_opts)
        elif command == "down":
            down(dbConn, args_opts)
        else:
            print("Invalid migration command.")
    except:
        print("Error executing schema migration command. Please check the error logs for diagnosis and debugging.")
    finally:
        dbConn.close()

def util_ops():
    #        create_migration(dbConn, args_opts)
    print("Migration utility processes")

def main():
    args = sys.argv[1:]
    args_opts = get_args_opts(args)
    
    if not db_related(args[0]):
        util_ops()
    else:
        db_ops(args[0], args_opts)

if __name__ == "__main__":
    load_dotenv()
    print("Starting migration task.")
    main()
else:
    print("Cannot be called as a module yet.")
