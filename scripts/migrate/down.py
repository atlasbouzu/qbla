from . import utils

def execute(db_conn, opts={}, args=[]):
    print("[PROCESSING] Preparing to execute migration files...")
    
    print("[PROCESSING] Gathering migration history...")
    
    limit = get_rollback_limit(opts)
    
    execute_down_queries(db_conn, get_migration_history(db_conn, limit))

def get_migration_history(db_conn, limit=0):
    history = []
    
    try:
        with db_conn.cursor() as cur:
            
            if limit:
                print("Limited")
                cur.execute("SELECT * FROM schema_migrations ORDER BY name DESC LIMIT %s", (limit,))
            else:
                cur.execute("SELECT * FROM schema_migrations ORDER BY name DESC")
            history = list(map(lambda record: record[0], cur.fetchall()))
            print(history)
            db_conn.commit()
    except:
        db_conn.rollback()

    return history 

def execute_down_queries(db_conn, queue):
    try:
        with db_conn.cursor() as cur:
            for filename in queue:
                down_query = utils.read_migration_file(filename, "down")
                
                if down_query:
                    cur.execute(down_query)
                    cur.execute("DELETE FROM schema_migrations WHERE name=%s", (filename,))
                else:
                    print("[ERROR] No rollback query found in {}. Terminating process as this may fail the rollback.".format(filename))
                    raise Exception("Malformed migration file found!")
            
            db_conn.commit()

        print("[SUCCESS] Database rollback successful!")
    except:
        print("[ERROR] Database rollback failed. Reverting database to previous state...")
        db_conn.rollback()

def get_rollback_limit(opts):
    if "steps" in opts and opts["steps"].isdigit():
        return int(opts["steps"])
    
    return 0

