import os, json, yaml

from . import constants

def read_migration_file(filename):
    file = open(os.path.join(constants.MIGRATIONS_PATH, "{}.json".format(filename)), 'r')
    queries = json.load(file)
    
    file.close()
    
    return queries

def create_migration_file(filename):
    file_path = os.path.join(constants.MIGRATIONS_PATH,"{}.yaml".format(filename))
    
    os.umask(0)
    
    with open(file_path, 'w', opener=file_opener) as fs:
        yaml.dump({'down': "", "up": ""}, fs, default_flow_style=False)

def file_opener(file_path, flags):
    return os.open(file_path, flags, 0o777)

