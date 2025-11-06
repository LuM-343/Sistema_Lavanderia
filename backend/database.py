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

def actualizar_cliente(idCliente, nombre, telefono, direccion, extra):
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        UPDATE clientes
        SET nombre=?, telefono=?, direccion=?, extra=?
        WHERE idCliente=?
    """, (nombre, telefono, direccion, extra, idCliente))
    con.commit()
    con.close()


def actualizar_servicio(idServicio, precio, obs, pago):
    con = conectar()
    cur = con.cursor()
    cur.execute("""
        UPDATE servicios
        SET precio=?, obs=?, pago=?
        WHERE idServicio=?
    """, (precio, obs, pago, idServicio))
    con.commit()
    con.close()