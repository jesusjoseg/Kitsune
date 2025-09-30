import sqlite3

try:
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = 1")
except sqlite3.Error as e:
    print(f"Erro de conexion sqllite3: {e}")
