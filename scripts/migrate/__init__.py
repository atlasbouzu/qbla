from . import constants

def execute(args, opts):
    print(args)
    print(opts)
    print(constants.SCHEMA_TABLE)
    print(constants.MIGRATIONS_PATH)
