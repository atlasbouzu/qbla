from . import constants,utils,create,up

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
        print("Prepare migration process!")
        process_args["db_conn"] = utils.create_db_conn()
    
    processes[process_name].execute(**process_args)
    
    if "db_conn" in process_args:
        process_args["db_conn"].close()

