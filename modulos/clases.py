import datetime, random
import utilidades
import sqlite3
import modClientes

#listas provisionales
servicios=[]

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
            registrarIngreso(self.idServicio, self.precio)
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
        registrarIngreso(self.idServicio, self.precio)
        actualizarServicio("pago",self.estado, self.idServicio)

    def __str__(self):
        return f"{self.idServicio} | Cliente: {self.idCliente} | Fecha: {self.fecha} | Q{self.precio} | {self.estado}"


def crearServicio():
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

def eliminarUltimoServicio(): #Fila
    if not servicios:
        return None
    ultimo = servicios.pop()
    conn=sqlite3.connect("datos/lavanderia.db")
    cursor=conn.cursor()
    instruccion=f"DELETE from servicios WHERE idServicio={ultimo.idServicio}"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()
    return ultimo


def insertarServicio(servicio):
    conn = sqlite3.connect("datos/lavanderia.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO servicios (idServicio,idCliente,fecha,precio,obs,estado,pago)
        VALUES (?,?,?,?,?,?,?)
    """, (servicio.idServicio, servicio.idCliente, servicio.fecha, servicio.precio, servicio.obs, servicio.estado, servicio.pago))
    conn.commit()
    conn.close()

def cargarServicios():
    servicios.clear()

    conn = sqlite3.connect("datos/lavanderia.db")
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

def listarServicios():
    lista = cargarServicios()

    print("\nLista de Servicios:")
    if not lista:
        print("No hay servicios registrados.\n")
        return

    for s in lista:
        print(s)
    print()

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

def actualizarServicio(parte, cambio, idServicio):
    conn =sqlite3.connect("datos/lavanderia.db")
    cursor=conn.cursor()
    instruccion=f"UPDATE servicios SET {parte}='{cambio}' WHERE idServicio='{idServicio}'"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()