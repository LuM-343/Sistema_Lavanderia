import datetime, random
import sqlite3
from backend import utilidades

# Lista global de clientes en memoria
clientes = []

# ============================================================
# CLASE CLIENTE
# ============================================================
class Cliente:
    def __init__(self, idCliente, nombre, telefono, direccion, extra="", servicios=0):
        self.idCliente = idCliente
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.extra = extra
        self.servicios = servicios

    def __str__(self):
        return f"Id:{self.idCliente} | Nombre:{self.nombre} | Tel:{self.telefono} | Servicios:{self.servicios} | Dirección:{self.direccion}"


# ============================================================
# CREAR CLIENTE
# ============================================================
def crearCliente(nombre, telefono, direccion="", extra=""):
    """Crea y valida un nuevo cliente desde la GUI."""
    nombre = nombre.strip().title()
    direccion = direccion.strip()
    extra = extra.strip()

    if not nombre:
        raise ValueError("Debe ingresar un nombre.")
    if not telefono or not str(telefono).isdigit():
        raise ValueError("El teléfono debe contener solo números.")
    telefono = int(telefono)
    if not (10000000 <= telefono <= 99999999):
        raise ValueError("El teléfono debe tener 8 dígitos válidos.")
    if not direccion:
        raise ValueError("Debe ingresar una dirección.")

    conn = sqlite3.connect("lavanderia.db")
    cur = conn.cursor()

    # Verificar duplicados
    cur.execute("SELECT COUNT(*) FROM clientes WHERE telefono=?", (telefono,))
    if cur.fetchone()[0] > 0:
        conn.close()
        raise ValueError("Ya existe un cliente con ese número de teléfono.")
    cur.execute("SELECT COUNT(*) FROM clientes WHERE LOWER(nombre)=?", (nombre.lower(),))
    if cur.fetchone()[0] > 0:
        conn.close()
        raise ValueError("Ya existe un cliente con ese nombre.")
    conn.close()

    # Crear ID único
    now = datetime.datetime.now()
    idCliente = f"Cli_{now.strftime('%y%m%d_%H%M%S')}_{random.randint(100,999)}"

    cliente = Cliente(idCliente, nombre, telefono, direccion, extra)
    insertarCliente(cliente)
    clientes.append(cliente)
    return cliente


# ============================================================
# INSERTAR CLIENTE
# ============================================================
def insertarCliente(cliente):
    conn = sqlite3.connect("lavanderia.db")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO clientes (idCliente, nombre, telefono, direccion, extra, servicios)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (cliente.idCliente, cliente.nombre, cliente.telefono, cliente.direccion, cliente.extra, cliente.servicios))
    conn.commit()
    conn.close()


# ============================================================
# ACTUALIZAR CLIENTE (VERSIÓN FINAL)
# ============================================================
def actualizarCliente(idCliente, nombre, telefono, direccion, extra):
    """Actualiza la información de un cliente y refresca la lista global."""
    with sqlite3.connect("lavanderia.db") as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE clientes
            SET nombre=?, telefono=?, direccion=?, extra=?
            WHERE idCliente=?
        """, (nombre, telefono, direccion, extra, idCliente))
        conn.commit()

    # Refrescar la lista global
    cargarClientes()

    print(f"Cliente {idCliente} actualizado correctamente.")


# ============================================================
# ELIMINAR CLIENTE
# ============================================================
def eliminarCliente(idCliente):
    """
    Verifica si el cliente tiene servicios antes de eliminarlo.
    Devuelve un diccionario con:
        {"estado": "bloqueado" / "ok" / "no_existe", "nombre": nombre_cliente}
    """
    conn = sqlite3.connect("lavanderia.db")
    cur = conn.cursor()

    # Obtener nombre del cliente
    cur.execute("SELECT nombre FROM clientes WHERE idCliente=?", (idCliente,))
    fila = cur.fetchone()
    if not fila:
        conn.close()
        return {"estado": "no_existe", "nombre": None}
    nombre = fila[0]

    # Verificar si tiene servicios
    cur.execute("SELECT COUNT(*) FROM servicios WHERE idCliente=?", (idCliente,))
    tieneServ = cur.fetchone()[0]

    if tieneServ > 0:
        conn.close()
        return {"estado": "bloqueado", "nombre": nombre}

    # Eliminar si no tiene servicios
    cur.execute("DELETE FROM clientes WHERE idCliente=?", (idCliente,))
    conn.commit()
    conn.close()

    # Quitar de lista global
    global clientes
    clientes = [c for c in clientes if c.idCliente != idCliente]

    print(f"Cliente {idCliente} eliminado correctamente.")
    return {"estado": "ok", "nombre": nombre}



# ============================================================
# CARGAR CLIENTES
# ============================================================
def cargarClientes():
    """Carga todos los clientes desde SQLite y actualiza la lista global."""
    global clientes
    clientes.clear()

    conn = sqlite3.connect("lavanderia.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM clientes")
    registros = cur.fetchall()
    conn.close()

    for fila in registros:
        cliente = Cliente(
            idCliente=fila[0],
            nombre=fila[1],
            telefono=fila[2],
            direccion=fila[3],
            extra=fila[4],
            servicios=fila[5]
        )
        clientes.append(cliente)

    return clientes


# ============================================================
# LISTAR CLIENTES (CONSOLA)
# ============================================================
def listarClientes():
    lista = cargarClientes()
    print("\nLista de Clientes:")
    if not lista:
        print("No hay clientes registrados.\n")
        return
    for c in lista:
        print(c)
    print()