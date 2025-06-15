import os, json

from . import constants

def read_migration_file(filename):
    file = open(os.path.join(constants.MIGRATIONS_PATH, "{}.json".format(filename)), 'r')
    queries = json.load(file)
    
    file.close()
    
    return queries

