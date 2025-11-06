import sqlite3
from datetime import datetime

# ============================================================
# MÓDULO: INGRESOS Y EGRESOS
# ------------------------------------------------------------
# Este módulo gestiona los registros financieros (ingresos y egresos)
# con su respectiva fecha y permite:
# - Crear la tabla si no existe o actualizarla
# - Registrar ingresos y egresos
# - Cargar y eliminar registros
# ============================================================

# ------------------------------------------------------------
# CREAR TABLA
# ------------------------------------------------------------
def crear_tabla():
    """
    Crea o actualiza la tabla 'ingresosYegresos' con la columna 'fecha'.
    Si la columna ya existe, no hace nada.
    """
    conn = sqlite3.connect("lavanderia.db")
    cursor = conn.cursor()

    # Crear tabla si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingresosYegresos (
            concepto TEXT NOT NULL,
            ingreso REAL DEFAULT 0,
            egreso REAL DEFAULT 0,
            fecha TEXT
        )
    """)

    # Verificar si la columna 'fecha' existe
    cursor.execute("PRAGMA table_info(ingresosYegresos)")
    columnas = [col[1] for col in cursor.fetchall()]
    if "fecha" not in columnas:
        # Agregar la columna sin valor por defecto (para evitar el error)
        cursor.execute("ALTER TABLE ingresosYegresos ADD COLUMN fecha TEXT")
        print("Columna 'fecha' agregada correctamente.")

    conn.commit()
    conn.close()


# ------------------------------------------------------------
# REGISTRAR INGRESO
# ------------------------------------------------------------
def registrarIngreso(concepto, total):
    """
    Inserta un nuevo ingreso en la tabla.
    """
    conn = sqlite3.connect("lavanderia.db")
    cursor = conn.cursor()
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO ingresosYegresos (concepto, ingreso, egreso, fecha)
        VALUES (?, ?, 0, ?)
    """, (concepto, total, fecha_actual))
    conn.commit()
    conn.close()


# ------------------------------------------------------------
# REGISTRAR EGRESO
# ------------------------------------------------------------
def registrarEgreso(concepto, total):
    """
    Inserta un nuevo egreso en la tabla.
    """
    conn = sqlite3.connect("lavanderia.db")
    cursor = conn.cursor()
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO ingresosYegresos (concepto, ingreso, egreso, fecha)
        VALUES (?, 0, ?, ?)
    """, (concepto, total, fecha_actual))
    conn.commit()
    conn.close()


# ------------------------------------------------------------
# CARGAR REGISTROS
# ------------------------------------------------------------
def cargarRegistros():
    """
    Devuelve todos los registros (ingresos y egresos).
    """
    conn = sqlite3.connect("lavanderia.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT rowid, concepto, ingreso, egreso, fecha
        FROM ingresosYegresos
        ORDER BY fecha DESC
    """)
    registros = cursor.fetchall()
    conn.close()
    return registros


# ------------------------------------------------------------
# ELIMINAR REGISTRO
# ------------------------------------------------------------
def eliminarRegistroPorConcepto(concepto, tipo):
    """
    Elimina un registro según el concepto y tipo ('ingreso' o 'egreso').
    """
    conn = sqlite3.connect("lavanderia.db")
    cursor = conn.cursor()
    if tipo == "ingreso":
        cursor.execute("DELETE FROM ingresosYegresos WHERE concepto=? AND ingreso>0", (concepto,))
    elif tipo == "egreso":
        cursor.execute("DELETE FROM ingresosYegresos WHERE concepto=? AND egreso>0", (concepto,))
    conn.commit()
    conn.close()
