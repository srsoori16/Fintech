import mysql.connector
conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'hello123',
    database = 'Fintech'
)
cursor = conn.cursor()