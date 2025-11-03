# =============================================
# Sistema de Control de Lavadas - Jave's Laundry
# Proyecto Final
# Luis Velásquez y Arenz Peláez
# =============================================

from datetime import datetime, timedelta

# Guardar datos en lista mientras se conecta a una base de datos
clientes = []
lavadas = []


# Clases a usar
class Cliente:
    def __init__(self, nombre, celular, direccion, extras=""):
        self.nombre = nombre
        self.celular = celular
        self.direccion = direccion
        self.extras = extras

class Lavada:
    def __init__(self, cliente, peso_kg):
        self.cliente = cliente
        self.peso_kg = peso_kg
        self.estado = "Recibida"
        self.fecha_registro = datetime.now()
        self.fecha_entrega = None

    def cambiar_estado(self, nuevo_estado):
        estados_validos = ["Recibida", "Lavada", "Entregada", "Olvidada"]
        if nuevo_estado not in estados_validos:
            print("Estado no válido. Los estados posibles son: Recibida, Lavada, Entregada, Olvidada.")
            return
        self.estado = nuevo_estado
        if nuevo_estado == "Entregada":
            self.fecha_entrega = datetime.now()
        print(f"Estado de lavada de {self.cliente.nombre} cambiado a: {self.estado}")
        simular_notificacion(self.cliente, f"Su ropa ahora está '{self.estado}'")


# Funciones de registro
def registrar_cliente():
    print("\n--- Registro de Cliente ---")
    nombre = input("Nombre del cliente: ").strip().title()
    if not nombre:
        print("Error: El nombre no puede estar vacío.\n")
        return

    celular = input("Celular: ").strip()
    if not celular.isdigit():
        print("Error: El número de celular debe contener solo dígitos.\n")
        return

    direccion = input("Dirección: ").strip()

    extras = input("Información adicional (opcional): ").strip()
    cliente = Cliente(nombre, celular, direccion, extras)
    clientes.append(cliente)
    print(f"Cliente '{nombre}' registrado exitosamente.\n")

def registrar_lavada():
    print("\n--- Registro de Lavada ---")
    if not clientes:
        print("No hay clientes registrados. Registre un cliente primero.\n")
        return

    for i, c in enumerate(clientes):
        print(f"{i+1}. {c.nombre} - {c.celular}")

    try:
        idx = int(input("Seleccione el número del cliente: ")) - 1
        if idx < 0 or idx >= len(clientes):
            print("Error: Opción fuera de rango.\n")
            return
    except ValueError:
        print("Error: Ingrese un número válido.\n")
        return

    cliente = clientes[idx]


    try:
        peso_kg = float(input("Peso estimado (kg): "))
        if peso_kg <= 0:
            print("Error: El peso debe ser mayor que cero.\n")
            return
    except ValueError:
        print("Error: Ingrese un número válido para el peso en kilogramos.\n")
        return

    lavada = Lavada(cliente, peso_kg)
    lavadas.append(lavada)
    print(f"Lavada registrada para {cliente.nombre} con estado '{lavada.estado}'.\n")

def cambiar_estado_lavada():
    print("\n--- Cambio de Estado de Lavada ---")
    if not lavadas:
        print("No hay lavadas registradas.\n")
        return

    for i, l in enumerate(lavadas):
        print(f"{i+1}. Cliente: {l.cliente.nombre} | Estado actual: {l.estado}")

    try:
        idx = int(input("Seleccione el número de la lavada: ")) - 1
        if idx < 0 or idx >= len(lavadas):
            print("Error: Opción fuera de rango.\n")
            return
    except ValueError:
        print("Error: Ingrese un número válido.\n")
        return

    lavada = lavadas[idx]
    nuevo_estado = input("Nuevo estado (Lavada / Entregada / Olvidada): ").capitalize().strip()
    lavada.cambiar_estado(nuevo_estado)
    print()

def simular_notificacion(cliente, mensaje):
    print(f"[Notificación simulada para {cliente.nombre} ({cliente.celular})]: {mensaje}")

def revisar_ropa_olvidada():
    print("\n--- Revisión de Ropa Olvidada ---")
    hoy = datetime.now()
    encontrado = False
    for lavada in lavadas:
        if lavada.estado != "Entregada":
            dias = (hoy - lavada.fecha_registro).days
            if dias > 15:
                lavada.cambiar_estado("Olvidada")
                print(f"Alerta: la ropa de {lavada.cliente.nombre} lleva {dias} días sin recoger.")
                encontrado = True
    if not encontrado:
        print("No hay ropa olvidada actualmente.\n")



def menu():
    while True:
        print("===== Sistema de Control de Lavadas =====")
        print("1. Registrar cliente")
        print("2. Registrar lavada")
        print("3. Cambiar estado de lavada")
        print("4. Revisar ropa olvidada (simulación 15 días)")
        print("5. Salir")
        op = input("Seleccione una opción: ").strip()

        if op == "1":
            registrar_cliente()
        elif op == "2":
            registrar_lavada()
        elif op == "3":
            cambiar_estado_lavada()
        elif op == "4":
            revisar_ropa_olvidada()
        elif op == "5":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente nuevamente.\n")

menu()
