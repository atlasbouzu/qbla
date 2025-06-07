import sys,os,re,json
import psycopg2

from dotenv import load_dotenv
from datetime import datetime

# Execute SQL queries to modify the database.
def up(dbConn, args_opts):
    print("Preparing to execute migration files...")
    
    migration_path = os.path.join(sys.path[0], "../db/migrations")
    
    migration_files = [
        file for file in os.listdir(migration_path) if os.path.isfile(os.path.join(migration_path, file))
    ]
    
    print("Found {} migration file/s".format(len(migration_files)))
    
    if not len(migration_files):
        print("No files to migrate. Exiting...")
        sys.exit(0)
    
    for json_file in migration_files:
        print("Migrating {}...".format(json_file))
        file_path = os.path.join(migration_path, json_file)
        
        mig_file = open(file_path, 'r')
        migration_queries = json.load(mig_file)
        
        mig_file.close()
        
        if not migration_queries["up"]:
            print("Cannot process current migration file: Empty query string.")
            continue
        
        try:
            with dbConn.cursor() as cur:
                cur.execute(migration_queries["up"])
                
                dbConn.commit()

            print("{} succesfully migrated!".format(json_file))
        except psycopg2.errors.DatabaseError as excp:
                print("Migration encountered an error!")
                dbConn.rollback()

# Execute SQL query to rollback changes on the database.
def down(dbConn, args_opts):
    print("Execute down functions of migration files")

def create(args_opts):
    full_filename = "{timestamp}-{filename}".format(
        filename=args_opts['args'][0],
        timestamp=int(round(datetime.timestamp(datetime.now())))
    )
    
    print("Creating {}...".format(full_filename))
    
    full_path = os.path.join(sys.path[0],"../db/migrations/{}.json".format(full_filename))
    
    file = open(full_path, 'x')
    file.write('{\n\t"up": "",\n\t"down": ""\n}')
    file.close()

    print("{} succesfully created!".format(full_filename))

# Check if schema_migrations table exists in the database.
def migration_table_exists(dbConn):
    print("Checking for migration table...")
    
    try:
        with dbConn.cursor() as cur:
            cur.execute("SELECT * FROM schema_migrations")
            dbConn.commit()

        print("schema_migrations table exists.")
        return True
    except psycopg2.errors.UndefinedTable as excp:
        print("schema_migrations table does not exist.")
        dbConn.rollback()
    
    return False

def create_migration_table(dbConn):
    print("Create schema_migrations table")
    
    try:
        with dbConn.cursor() as cur:
            cur.execute("CREATE TABLE schema_migrations (name VARCHAR(255));")
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
        create_migration_table(dbConn)

#TODO: downができてからこれが次
def get_args_opts(args):
    args_opts = args[1:]
    args = []
    opts = {}
    
    for input in args_opts:
        scan = re.search(r"^--([a-zA-Z_-]+)=(.*)", input)
        
        if scan:
            opts[scan.group(1)] = scan.group(2)
        else:
            args.append(input)
    
    return {
        'args': args,
        'opts': opts,
    }

def db_related(command):
    return command == "up" or command == "down"

def db_ops(command, args_opts):
    dbConn = create_db_conn()
    
    if not dbConn:
        sys.exit(1)
    
    prep_db_ops(dbConn)
    
    # TODO: try/Exceptionがなしにする
    try:
        if command == "up":
            up(dbConn, args_opts)
        elif command == "down":
            down(dbConn, args_opts)
        else:
            print("Invalid migration command.")
    except Exception as excp:
        print(excp)
        print("Error executing schema migration command. Please check the error logs for diagnosis and debugging.")
    finally:
        dbConn.close()

def util_ops(command, args_opts):
    if command == "create":
        create(args_opts)
    else:
        print("Unreconized migration command. Please check the migration section of the README.")

def main():
    cl_args = sys.argv[1:]
    command = cl_args[0]
    args_opts = get_args_opts(cl_args)
    
    if not len(cl_args):
        print("No valid commands/arguments provided. Please see the migration section of the README.")
        sys.exit(1)
    
    if not db_related(command):
        util_ops(command, args_opts)
    else:
        db_ops(command, args_opts)

if __name__ == "__main__":
    load_dotenv()
    main()
else:
    print("Cannot be called as a module yet.")
