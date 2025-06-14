import sys

from . import constants,database,create,up

MIGRATE_PREP_MAP = {
    "create": False,
    "up": True,
    "down": True,
}

def execute(args, opts):
    process_name = args[0]
    process_args = { "args": args[1:], "opts": opts }
    
    processes = {
        "create": create,
        "up": up
    }
    
    if not process_name in processes:
        print("[ERROR] Unknown migrate process. Please check README for available processes.")
        return False
    
    if MIGRATE_PREP_MAP[process_name]:
        process_args["db_conn"] = database.create_db_conn()
        database.init_migration(process_args["db_conn"])
    
    processes[process_name].execute(**process_args)
    
    if "db_conn" in process_args:
        print("[TERMINATING] Closing database connection...")
        process_args["db_conn"].close()

