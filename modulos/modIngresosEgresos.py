import sqlite3

def registrarIngreso(concepto, total):
    conn = sqlite3.connect("datos/lavanderia.db")
    cursor=conn.cursor()
    instruccion= f"INSERT INTO ingresosYegresos VALUES ('{concepto}',{total}, {0} )"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()

def registrarEgreso(concepto, total):
    conn = sqlite3.connect("datos/lavanderia.db")
    cursor=conn.cursor()
    instruccion= f"INSERT INTO ingresosYegresos VALUES ('{concepto}',{0}, {total} )"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()
