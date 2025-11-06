import datetime, random
import modulos.utilidades as utilidades
import sqlite3
import modulos.modClientes as modClientes
import modulos.modIngresosEgresos as modIngresosEgresos

# Cola de servicios /lavadas pendientees
colaServicios = []

#listas provisionales
servicios=[]
serviciosEliminados=[] #Para poder volver si se borra algun servicio por error
#Clase servicio

class Servicio:
    def __init__(self, idServicio, idCliente, fecha, precio, obs="", estado="Pendiente", pago="pendiente"):
        self.idServicio = idServicio
        self.idCliente = idCliente
        self.fecha = fecha
        self.precio = precio
        self.estado = estado    #Pendiente, Lavado, Entegado, Olvidado
        self.pago = pago    #Pendiente, Cancelado
        self.obs = obs
        self.verificarTardanza()

    def cambiarLavado(self):
        self.estado="Lavado"
        #enviar mensaje whasapp
        actualizarServicio("estado",self.estado, self.idServicio)

    def cambiarEntregado(self, pagado):
        self.estado="Entregado"
        print(f"Servicio con el id")
        if pagado:
            self.pago="Cancelado"
            modIngresosEgresos.registrarIngreso(self.idServicio, self.precio)
            actualizarServicio("pago",self.pago, self.idServicio)
            #Llamar a la función de registrar pago de una a la base de datos
        actualizarServicio("estado",self.estado, self.idServicio)

    def verificarTardanza(self):
        actual=datetime.datetime.now()
        diferencia= actual-self.fecha
        if diferencia.days > 15 and self.estado !="Olvidado":
            self.estado="Olvidado"
            actualizarServicio("estado",self.estado, self.idServicio)
            #enviar mensaje whatsapp 
            #Actualizar info en base de datos

    def cambiarPago(self):
        self.pago="Cancelado"
        modIngresosEgresos.registrarIngreso(self.idServicio, self.precio)
        actualizarServicio("pago",self.estado, self.idServicio)

    def __str__(self):
        return f"{self.idServicio} | Cliente: {self.idCliente} | Fecha: {self.fecha} | Q{self.precio} | {self.estado}"


def crearServicio():        #Cambiar para que ya no use la lista temporal, si no que use la lista creada a partir de la base de datos de clientes
    try:
        if not modClientes.clientes:
            raise ValueError("Primero registra un cliente")

        now = datetime.datetime.now()
        id = f"Ser_{now.strftime('%y%m%d_%H')}_{random.randint(100,999)}"

        print("\nClientes disponibles:")
        for c in modClientes.clientes:
            print(c)

        idCliente = input("ID Cliente: ").strip()
        pos = utilidades.busquedaSecuencial(modClientes.clientes, idCliente, "idCliente")
        if pos == -1:
            raise ValueError("Cliente no encontrado")

        precio = float(input("Precio Q: "))
        obs = input("Observaciones: ")

        servicio = Servicio(id, idCliente, now, precio, obs)
        servicios.append(servicio)
        modClientes.clientes[pos].servicios += 1

        print("\nServicio creado")
        print(servicio)

        insertarServicio(servicio)
    except Exception as e:
        print("Error:", e)

def eliminarServicio(idServicio):
    conn = sqlite3.connect("lavanderia.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM servicios WHERE idServicio=?", (idServicio,))
    conn.commit()
    conn.close()

    # Lista temporal
    for s in servicios:
        if s.idServicio == idServicio:
            servicios.remove(s)
            break

    print("Servicio eliminado correctamente")

def eliminarServicioConPila(idServicio):
    # Obtener servicio antes de borrar
    conn = sqlite3.connect("lavanderia.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM servicios WHERE idServicio=?", (idServicio,))
    dato = cur.fetchone()

    if not dato:
        print("Servicio no existe")
        return
    
    # Guardarlo en pila PERO como tu objeto
    servicio = Servicio(dato[0], dato[1], datetime.datetime.fromisoformat(dato[2]), dato[3], dato[4], dato[5], dato[6])
    serviciosEliminados.append(servicio)

    # Borrar en BD
    cur.execute("DELETE FROM servicios WHERE idServicio=?", (idServicio,))
    conn.commit()
    conn.close()

    print("Servicio eliminado y guardado en pila para un posible control Z")

def deshacerEliminacionServicio():
    if not serviciosEliminados:
        print("No hay servicios para restaurar")
        return
    
    servicio = serviciosEliminados.pop()

    insertarServicio(servicio)  # Volver a insertar el servicio a la base de datos
    print("Servicio restaurado desde la pila")

def insertarServicio(servicio):
    conn = sqlite3.connect("lavanderia.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO servicios (idServicio,idCliente,fecha,precio,obs,estado,pago)
        VALUES (?,?,?,?,?,?,?)
    """, (servicio.idServicio, servicio.idCliente, servicio.fecha, servicio.precio, servicio.obs, servicio.estado, servicio.pago))
    conn.commit()
    conn.close()

def cargarServicios():
    servicios.clear()

    conn = sqlite3.connect("lavanderia.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM servicios")
    registros = cursor.fetchall()
    conn.close()

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

def actualizarServicio(idServicio, estado=None, pago=None, obs=None):
    conn = sqlite3.connect("lavanderia.db")
    cursor = conn.cursor()

    if estado:
        cursor.execute("UPDATE servicios SET estado=? WHERE idServicio=?", (estado, idServicio))

    if pago:
        cursor.execute("UPDATE servicios SET pago=? WHERE idServicio=?", (pago, idServicio))

    if obs:
        cursor.execute("UPDATE servicios SET obs=? WHERE idServicio=?", (obs, idServicio))

    conn.commit()
    conn.close()

    # Actualizar lista temporal
    for s in servicios:
        if s.idServicio == idServicio:
            if estado: s.estado = estado
            if pago: s.pago = pago
            if obs: s.obs = obs
            break

    print("Servicio actualizado")

#COLA SERVICIOS, USAMOS BUBLE SORT
def cargarColaPendientes(): #Cargar los servicios que aparecen como pendiente
    global colaServicios
    colaServicios.clear()

    conn = sqlite3.connect("lavanderia.db")
    cur = conn.cursor()
    cur.execute("SELECT idServicio, idCliente, fecha, precio, obs, estado, pago FROM servicios WHERE estado='Pendiente'")
    datos = cur.fetchall()
    conn.close()

    colaServicios = [
        Servicio(
            idServicio=fila[0],
            idCliente=fila[1],
            fecha=datetime.datetime.fromisoformat(fila[2]),
            precio=fila[3],
            obs=fila[4],
            estado=fila[5],
            pago=fila[6]
        )
        for fila in datos
    ]
    colaServicios=utilidades.bubbleSort(colaServicios, "fecha")
    colaServicios.reverse()

def mostrarCola(): #Mostrar el estado actual de la Cola
    cargarColaPendientes()
    if not colaServicios:
        print("\nNo hay lavadas pendientes.")
        return
    print("\nLavadas pendientes:")
    for i, s in enumerate(colaServicios, 1):
        print(f"{i}. {s['idServicio']} - Cliente: {s['idCliente']} - Precio: Q{s['precio']} - Estado: {s['estado']}")
