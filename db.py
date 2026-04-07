from sqlite3 import Connection, connect
class Database:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.conn: Connection = None

    def connect(self):
        self.conn = connect(self.db_file)

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def execute(self, q: str, p: tuple = ()):
        if not self.conn:
            raise Exception("Database conn is not established.")
        cursor = self.conn.cursor()
        cursor.execute(q, p)
        self.conn.commit()
        return cursor
    def fetchall(self, q: str,  p: tuple = ()):
        cursor = self.execute(q, p)
        return cursor.fetchall()
    def fetchone(self, q: str, p: tuple = ()):
        cursor = self.execute(q, p)
        return cursor.fetchone()
    def __enter__(self):
        self.connect()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()