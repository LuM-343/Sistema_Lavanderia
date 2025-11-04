import datetime, random
import sqlite3
import utilidades

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

def actualizarCliente():
    try:
        print("\nClientes disponibles:")    #En esta parte lo mismo, seria mejor que muestre todos los clientes y seleccione
        for c in clientes:                  #nada mas el que va a actualizar
            print(c)

        idCliente = input("Ingresa el ID del cliente: ").strip()
        pos = utilidades.busquedaSecuencial(clientes, idCliente, "idCliente")
        if pos == -1:
            raise ValueError("ID de cliente no existe")
        
        nTelefono = int(input("ingresa el nuevo celular: "))
        if not (10000000 <= nTelefono <= 99999999):
            raise ValueError("Teléfono inválido")
        
        ndireccion= input("Ingresa la nueva dirección: ")

        if nTelefono!= clientes[pos].telefono or nTelefono!="":
            actualizarCliente("telefono", nTelefono, clientes[pos].idCliente)

        if ndireccion!=clientes[pos].direccion or ndireccion!="":
            actualizarCliente("direccion", ndireccion, clientes[pos].idClientes)
    except Exception as e:
            print("Error:", e)
            print("Vuelve a intentarlo.")

def insertarCliente(cliente):
    conn = sqlite3.connect("datos/lavanderia.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clientes (idCliente,nombre,telefono,direccion,extra,servicios)
        VALUES (?,?,?,?,?,?)
    """, (cliente.idCliente, cliente.nombre, cliente.telefono, cliente.direccion, cliente.extra, cliente.servicios))
    conn.commit()
    conn.close()

def actualizarCliente(parte, cambio, idCliente):
    conn =sqlite3.connect("datos/lavanderia.db")
    cursor=conn.cursor()
    instruccion=f"UPDATE clientes SET {parte}='{cambio}' WHERE idCliente='{idCliente}'"
    cursor.execute(instruccion)
    conn.commit()
    conn.close()

def cargarClientes():
    """Carga todos los clientes desde SQLite y los mete a la lista clientes[]"""
    clientes.clear()  # Limpia lista temporal

    conn = sqlite3.connect("datos/lavanderia.db")
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


def listarClientes():
    """Imprime clientes desde SQLite (consola)"""
    lista = cargarClientes()

    print("\nLista de Clientes:")
    if not lista:
        print("No hay clientes registrados.\n")
        return

    for c in lista:
        print(c)
    print()
