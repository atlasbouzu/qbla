import psycopg2

class Database:
    def __init__(self, creds):
        self.conn = self.create_conn(creds)
        self.cursor = self.init_conn()
    
    def create_conn(self, creds):
        return psycopg2.connect(**creds)
    
    def init_conn(self):
        return self.conn.cursor()
    
    def test(self, message):
        print(message)
    
    def execute(self, query):
        try:
            return self.cursor.execute(query)
        except psycopg2.errors.UndefinedTable:
            return False

