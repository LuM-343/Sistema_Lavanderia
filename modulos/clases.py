import datetime, random
import utilidades

#listas provisionales
clientes=[]
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
        #Actualizar info en base de datos

    def cambiarEntregado(self, pagado):
        self.estado="Entregado"
        print(f"Servicio con el id")
        if pagado:
            self.pago="Cancelado"
            #Llamar a la función de registrar pago de una a la base de datos
        #Actualizar info en base de datos

    def verificarTardanza(self):
        actual=datetime.datetime.now()
        diferencia= actual-self.fecha
        if diferencia.days > 15 and self.estado !="Olvidado":
            self.estado="Olvidado"
            #enviar mensaje whatsapp 
            #Actualizar info en base de datos

    def cambiarPago(self):
        self.pago="Cancelado"
        #Registrar pago
        #Actualizar base de datos

    def __str__(self):
        return f"{self.idServicio} | Cliente: {self.idCliente} | Fecha: {self.fecha} | Q{self.precio} | {self.estado}"

class Cliente:
    def __init__(self, idCliente, nombre, telefono, direccion, extra="", servicios=0):
        self.idCliente = idCliente
        self.nombre = nombre
        self.__telefono = telefono
        self.__direccion = direccion
        self.extra = extra
        self.servicios = servicios

    def modificar(self, telefono, direccion, extra):
        self.__telefono=telefono
        self.__direccion=direccion
        self.extra=extra

    def __str__(self):
        return f"Id:{self.idCliente} | Nombre:{self.nombre} | Tel:{self.__telefono} | Servicios:{self.servicios} | Dirección: {self.__direccion}"

def registrarCliente(): #Creación de Clientes, me imagino que esto lo modificaras, solo toma las comprobaciones
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
            print("\nCliente registrado exitosamente\n")
            print(cliente)
            break
        except Exception as e:
            print("Error:", e)
            print("Vuelve a intentarlo.")


def registrarServicio():
    while True:
        try:
            if not clientes:
                raise ValueError("Primero registra un cliente")

            now = datetime.datetime.now()
            id = f"Ser_{now.strftime('%y%m%d_%H')}_{random.randint(100,999)}"

            print("\nClientes disponibles:")
            for c in clientes:
                print(c)

            idCliente = input("Ingresa el ID del cliente: ").strip()
            pos = utilidades.busquedaSecuencial(clientes, idCliente, "idCliente")
            if pos == -1:
                raise ValueError("ID de cliente no existe")

            precio = float(input("Precio del servicio: Q"))
            if precio <= 0:
                raise ValueError("Precio inválido")

            obs = input("Observaciones: ").strip()

            servicio = Servicio(id, idCliente, now, precio, obs)
            servicios.append(servicio)

            clientes[pos].servicios += 1  # +1 servicio al cliente

            print("\nServicio registrado")
            print(servicio)
            break
        except Exception as e:
            print("Error:", e)
            print("Vuelve a intentarlo.")
