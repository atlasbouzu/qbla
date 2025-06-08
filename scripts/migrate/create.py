import os

from datetime import datetime

from . import constants

def execute(args, opts):
    if not args_is_valid(args):
        return False
    
    full_filename = "{timestamp}-{filename}".format(
        filename=args[0],
        timestamp=int(round(datetime.timestamp(datetime.now())))
    )
    
    print("Creating {}...".format(full_filename))
    
    file_path = os.path.join(constants.MIGRATIONS_PATH,"{}.json".format(full_filename))
    
    os.umask(0)
    
    with open(file_path, 'w', opener=file_opener) as fs:
        fs.write('{\n\t"up": "",\n\t"down": ""\n}')
    
    print("[SUCCESS] {} created!".format(full_filename))

def file_opener(file_path, flags):
    return os.open(file_path, flags, 0o777)

def args_is_valid(args):
    if len(args) == 0:
        print("[ERROR] Migration file name cannot be empty!")
        return False
    
    return True
