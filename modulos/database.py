import sqlite3

def conectar():
    """Conecta con la base de datos principal."""
    return sqlite3.connect("lavanderia.db")

def crear_tablas():
    """Crea las tablas necesarias si no existen."""
    con = conectar()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS clientes(
        idCliente TEXT PRIMARY KEY,
        nombre TEXT NOT NULL,
        telefono INTEGER,
        direccion TEXT,
        extra TEXT,
        servicios INTEGER DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS servicios(
        idServicio TEXT PRIMARY KEY,
        idCliente TEXT,
        fecha TEXT,
        precio REAL,
        obs TEXT,
        estado TEXT,
        pago TEXT,
        FOREIGN KEY(idCliente) REFERENCES clientes(idCliente)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ingresosYegresos(
        concepto TEXT,
        ingreso REAL DEFAULT 0,
        egreso REAL DEFAULT 0
    )
    """)

    con.commit()
    con.close()
    print("✅ Tablas creadas correctamente")