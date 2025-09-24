import sqlite3

try:
    con = sqlite3.connect("database.db")
    cur = con.cursor()
except sqlite3.Error as e:
    print(f"Erro de conexion sqllite3: {e}")
