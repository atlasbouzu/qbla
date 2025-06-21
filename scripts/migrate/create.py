import os

from datetime import datetime

from . import utils

def execute(args, opts):
    if not args_is_valid(args):
        return False
    
    full_filename = "{timestamp}-{filename}".format(
        filename=args[0],
        timestamp=int(round(datetime.timestamp(datetime.now())))
    )
    
    print("Creating {}...".format(full_filename))
    
    utils.create_migration_file(full_filename)
    
    print("[SUCCESS] {} created!".format(full_filename))

def args_is_valid(args):
    if len(args) == 0:
        print("[ERROR] Migration file name cannot be empty!")
        return False
    
    return True
