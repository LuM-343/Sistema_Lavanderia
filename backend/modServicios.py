import datetime, random
from backend import utilidades
import sqlite3
from backend import modClientes
from backend import modIngresosEgresos

# Listas provisionales
servicios = []
serviciosEliminados = []  # Para poder volver si se borra algún servicio por error

# ------------------------------------------------------------
# CLASE SERVICIO
# ------------------------------------------------------------
class Servicio:
    def __init__(self, idServicio, idCliente, fecha, precio, obs="", estado="Pendiente", pago="pendiente"):
        self.idServicio = idServicio
        self.idCliente = idCliente
        self.fecha = fecha
        self.precio = precio
        self.estado = estado    # Pendiente, Lavado, Entregado, Olvidado
        self.pago = pago        # Pendiente, Cancelado
        self.obs = obs
        self.verificarTardanza()

    def cambiarLavado(self):
        self.estado = "Lavado"
        actualizarServicio(self.idServicio, estado=self.estado)

    def cambiarEntregado(self, pagado):
        self.estado = "Entregado"
        if pagado:
            self.pago = "Cancelado"
            modIngresosEgresos.registrarIngreso(self.idServicio, self.precio)
            actualizarServicio(self.idServicio, pago=self.pago)
        actualizarServicio(self.idServicio, estado=self.estado)

    def verificarTardanza(self):
        actual = datetime.datetime.now()
        diferencia = actual - self.fecha
        if diferencia.days > 15 and self.estado != "Olvidado":
            self.estado = "Olvidado"
            actualizarServicio(self.idServicio, estado=self.estado)

    def cambiarPago(self):
        self.pago = "Cancelado"
        modIngresosEgresos.registrarIngreso(self.idServicio, self.precio)
        actualizarServicio(self.idServicio, pago=self.pago)

    def __str__(self):
        return f"{self.idServicio} | Cliente: {self.idCliente} | Fecha: {self.fecha} | Q{self.precio} | {self.estado}"


# ------------------------------------------------------------
# FUNCIONES PRINCIPALES
# ------------------------------------------------------------
def crearServicio():
    """Crea un nuevo servicio para un cliente existente (búsqueda por nombre)."""
    try:
        if not modClientes.clientes:
            raise ValueError("Primero registra un cliente")

        now = datetime.datetime.now()
        id_serv = f"Ser_{now.strftime('%y%m%d_%H')}_{random.randint(100,999)}"

        print("\nClientes disponibles:")
        for c in modClientes.clientes:
            print(c)

        nombreCliente = input("Nombre del cliente: ").strip().title()
        cliente = utilidades.busquedaBinariaPorNombre(modClientes.clientes, nombreCliente)

        if not cliente:
            raise ValueError("Cliente no encontrado")

        idCliente = cliente.idCliente
        precio = float(input("Precio Q: "))
        obs = input("Observaciones: ")

        servicio = Servicio(id_serv, idCliente, now, precio, obs)
        servicios.append(servicio)

        print("\nServicio creado")
        print(servicio)

        insertarServicio(servicio)
    except Exception as e:
        print("Error:", e)


def insertarServicio(servicio):
    """Inserta un nuevo servicio y actualiza el contador en clientes."""
    with sqlite3.connect("lavanderia.db") as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO servicios (idServicio, idCliente, fecha, precio, obs, estado, pago)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (servicio.idServicio, servicio.idCliente, servicio.fecha.isoformat(),
              servicio.precio, servicio.obs, servicio.estado, servicio.pago))
        conn.commit()

    # Incrementar contador en la tabla clientes
    with sqlite3.connect("lavanderia.db") as conn:
        cur = conn.cursor()
        cur.execute("UPDATE clientes SET servicios = servicios + 1 WHERE idCliente = ?", (servicio.idCliente,))
        conn.commit()


def eliminarServicio(idServicio):
    """Elimina un servicio permanentemente y actualiza el contador del cliente."""
    with sqlite3.connect("lavanderia.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT idCliente FROM servicios WHERE idServicio=?", (idServicio,))
        fila = cur.fetchone()

        if fila:
            idCliente = fila[0]
            cur.execute("DELETE FROM servicios WHERE idServicio=?", (idServicio,))
            cur.execute("UPDATE clientes SET servicios = servicios - 1 WHERE idCliente=?", (idCliente,))
            conn.commit()

    # Remover de la lista temporal
    for s in servicios:
        if s.idServicio == idServicio:
            servicios.remove(s)
            break

    print("Servicio eliminado correctamente.")


def eliminarServicioConPila(idServicio):
    """Elimina un servicio pero lo guarda en una pila para poder restaurarlo."""
    with sqlite3.connect("lavanderia.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM servicios WHERE idServicio=?", (idServicio,))
        dato = cur.fetchone()

        if not dato:
            print("Servicio no existe.")
            return

        servicio = Servicio(dato[0], dato[1], datetime.datetime.fromisoformat(dato[2]),
                            dato[3], dato[4], dato[5], dato[6])
        serviciosEliminados.append(servicio)

        cur.execute("DELETE FROM servicios WHERE idServicio=?", (idServicio,))
        cur.execute("UPDATE clientes SET servicios = servicios - 1 WHERE idCliente=?", (dato[1],))
        conn.commit()

    print("Servicio eliminado y guardado en pila (Control Z disponible).")


def deshacerEliminacionServicio():
    """
    Restaura el último servicio eliminado desde la pila.
    Devuelve:
      - "ok" si se restauró correctamente
      - "vacio" si no hay servicios por restaurar
      - "error" si ocurre algún problema
    """
    try:
        if not serviciosEliminados:
            print("No hay servicios para restaurar.")
            return "vacio"

        servicio = serviciosEliminados.pop()
        insertarServicio(servicio)
        print(f"Servicio {servicio.idServicio} restaurado desde la pila.")
        return "ok"

    except Exception as e:
        print(f"Error al restaurar servicio: {e}")
        return "error"



def cargarServicios():
    """Carga todos los servicios desde la base de datos."""
    servicios.clear()
    with sqlite3.connect("lavanderia.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM servicios")
        registros = cur.fetchall()

    for fila in registros:
        servicio = Servicio(
            idServicio=fila[0],
            idCliente=fila[1],
            fecha=datetime.datetime.fromisoformat(fila[2]),
            precio=fila[3],
            obs=fila[4],
            estado=fila[5],
            pago=fila[6]
        )
        servicios.append(servicio)

    return servicios


def listarServicios():
    lista = cargarServicios()
    print("\nLista de Servicios:")
    if not lista:
        print("No hay servicios registrados.\n")
        return
    for s in lista:
        print(s)
    print()


def actualizarServicio(idServicio, estado=None, pago=None, obs=None):
    """Actualiza los campos estado/pago/obs de un servicio."""
    with sqlite3.connect("lavanderia.db") as conn:
        cur = conn.cursor()
        if estado:
            cur.execute("UPDATE servicios SET estado=? WHERE idServicio=?", (estado, idServicio))
        if pago:
            cur.execute("UPDATE servicios SET pago=? WHERE idServicio=?", (pago, idServicio))
        if obs:
            cur.execute("UPDATE servicios SET obs=? WHERE idServicio=?", (obs, idServicio))
        conn.commit()

    for s in servicios:
        if s.idServicio == idServicio:
            if estado: s.estado = estado
            if pago: s.pago = pago
            if obs: s.obs = obs
            break

    print("Servicio actualizado.")


# ------------------------------------------------------------
# FUNCIÓN DE CONTEO DE SERVICIOS POR CLIENTE
# ------------------------------------------------------------
def contarServiciosPorCliente(idCliente):
    """Devuelve cuántos servicios tiene un cliente registrado."""
    with sqlite3.connect("lavanderia.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM servicios WHERE idCliente=?", (idCliente,))
        cantidad = cur.fetchone()[0]
    return cantidad
