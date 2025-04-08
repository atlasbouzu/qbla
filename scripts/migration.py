import sys,os
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
    
    result = dbConn.execute("SELECT * FROM schema_migrations")
    
    if not result:
        return False
    
    return True

def init_migration_table(dbConn):
    dbConn.test("Create schema_migrations table")

def init_db_conn():
    creds = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASS'),
        'host': os.getenv('DB_HOST'),
        'port': '5432'
    }
    
    print("Initialize DB connection")
    return Database(creds)

#TODO: downができてからこれが次
def get_args_opts(args):
    return {}

def main():
    args = sys.argv[1:]
    args_opts = get_args_opts(args)
    
    dbConn = init_db_conn()
    
    if not migration_table_exists(dbConn):
        init_migration_table(dbConn)
    
    if args[0] == "up":
        up(dbConn, args_opts)
    elif args[0] == "down":
        down(dbConn, args_opts)
    elif args[0] == "create":
        create_migration(dbConn, args_opts)
    else:
        print("Error: Unknown migration command")

if __name__ == "__main__":
    load_dotenv()
    print("Starting migration task.")
    main()
else:
    print("Cannot be called as a module yet.")
