import os, yaml

from . import constants

def read_migration_file(filename, query_type="all"):
    queries = {}
    with open(os.path.join(constants.MIGRATIONS_PATH, "{}.yml".format(filename)), 'r') as file:
        queries = yaml.safe_load(file)
    
    if query_type != "up" and query_type != "down":
        return queries
    
    return queries[query_type]

def create_migration_file(filename):
    file_path = os.path.join(constants.MIGRATIONS_PATH,"{}.yml".format(filename))
    
    os.umask(0)
    
    with open(file_path, 'w', opener=file_opener) as fs:
        yaml.dump({'up': "", "down": ""}, fs, default_flow_style=False, sort_keys=False)

def file_opener(file_path, flags):
    return os.open(file_path, flags, 0o777)

