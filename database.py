import sqlite3

class Database:


    def __init__(self, database_name:str):
        self.conn = sqlite3.connect(database_name)
        
    

    def __del__(self):
        self.conn.close
    

    def create_table(self, sql:str):
        
        self.cursor = self.conn.cursor()
        self.cursor.execute(sql)
        self.conn.commit()
    
