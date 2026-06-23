import psycopg2

def connect_db():
    conn = psycopg2.connect(
        host="localhost",
        database="warehouse",
        user="postgres",
        password="123456"
    )
    return conn