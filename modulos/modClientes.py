import datetime, random
import sqlite3
import modulos.utilidades as utilidades

clientes=[]
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

    def modificar(self, telefono, direccion, extra):
        self.telefono=telefono
        self.direccion=direccion
        self.extra=extra

def crearCliente(): 
    while True:
        try:
            print("\nIngreso de Clientes")
            now = datetime.datetime.now()
            id = f"Cli_{now.strftime('%y%m%d_%H')}_{random.randint(100,999)}"

            nombre = input("Nombre del cliente: ").strip().title()
            if not nombre:
                raise ValueError("Debes ingresar un nombre")

            telefono = int(input("Teléfono: "))
            if not (10000000 <= telefono <= 99999999):
                raise ValueError("Teléfono inválido")

            direccion = input("Dirección: ").strip()
            extra = input("Info extra: ").strip()

            cliente = Cliente(id, nombre, telefono, direccion, extra)
            clientes.append(cliente)
            print("\nCliente registrado en memoria")
            print(cliente)

            insertarCliente(cliente)  
            break

        except Exception as e:
            print("Error:", e)
            print("Vuelve a intentarlo.")

def actualizarCliente(idCliente, nuevoTelefono=None, nuevaDireccion=None, nuevoExtra=None):
    conn = sqlite3.connect("lavanderia.db")
    cursor = conn.cursor()

    if nuevoTelefono is not None:
        cursor.execute("UPDATE clientes SET telefono=? WHERE idCliente=?", (nuevoTelefono, idCliente))

    if nuevaDireccion is not None:
        cursor.execute("UPDATE clientes SET direccion=? WHERE idCliente=?", (nuevaDireccion, idCliente))

    if nuevoExtra is not None:
        cursor.execute("UPDATE clientes SET extra=? WHERE idCliente=?", (nuevoExtra, idCliente))

    conn.commit()
    conn.close()


    for c in clientes:
        if c.idCliente == idCliente:
            if nuevoTelefono: c.telefono = nuevoTelefono
            if nuevaDireccion: c.direccion = nuevaDireccion
            if nuevoExtra: c.extra = nuevoExtra
            break

    print("Cliente actualizado correctamente")


def insertarCliente(cliente):
    conn = sqlite3.connect("lavanderia.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clientes (idCliente,nombre,telefono,direccion,extra,servicios)
        VALUES (?,?,?,?,?,?)
    """, (cliente.idCliente, cliente.nombre, cliente.telefono, cliente.direccion, cliente.extra, cliente.servicios))
    conn.commit()
    conn.close()

def eliminarCliente(idCliente):
    conn = sqlite3.connect("lavanderia.db")
    cursor = conn.cursor()

    # Verificar si tiene servicios asociados
    cursor.execute("SELECT COUNT(*) FROM servicios WHERE idCliente=?", (idCliente,))
    tieneServ = cursor.fetchone()[0]

    if tieneServ > 0:
        print("No se puede eliminar el cliente, tiene servicios registrados.")
        conn.close()
        return

    cursor.execute("DELETE FROM clientes WHERE idCliente=?", (idCliente,))
    conn.commit()
    conn.close()

    # Quitar de lista temporal
    for c in clientes:
        if c.idCliente == idCliente:
            clientes.remove(c)
            break

    print("Cliente eliminado correctamente")

def cargarClientes():
    """Carga todos los clientes desde SQLite y los mete a la lista clientes[]"""
    clientes.clear()  # Limpia lista temporal

    conn = sqlite3.connect("lavanderia.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    registros = cursor.fetchall()
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

def buscarClientePorNombre(nombre): #Se recomienda aplicar un .strip() y .title() porque asi se guardaron los nombres
    cargarClientes()
    cliente=utilidades.busquedaSecuencial(clientes, nombre, "nombre")
    if cliente!=-1:
        return cliente
    else: return "Cliente no encontrado"

#Busqueda de ID por HASH
def busquedaID(idBuscar):
    tabla = utilidades.crearHash(clientes, "idCliente")
    cliente = utilidades.buscarHash(tabla, idBuscar)
    if cliente:
        print("Cliente encontrado:", cliente)
    else:
        print("Cliente no encontrado")

def mostrarClientesOrdenados(caracteristica):
    cargarClientes()
    clientesOrdenados=utilidades.bubbleSort(clientes,caracteristica)
    return clientesOrdenados    
