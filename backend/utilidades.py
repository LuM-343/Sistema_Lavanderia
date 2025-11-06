from backend import modClientes

# ============================================================
# UTILIDADES DE BÚSQUEDA Y ORDENAMIENTO
# ============================================================

# --- Método de ordenamiento: Bubble Sort ---
def ordenarServiciosPorNombreCliente(lista, case_insensitive=True):
    """
    Ordena una lista de objetos Servicio según el nombre del cliente asociado.
    """
    n = len(lista)
    for i in range(n - 1):
        for j in range(n - i - 1):
            # Obtener nombres de cliente asociados
            cliente1 = next((c for c in modClientes.clientes if c.idCliente == lista[j].idCliente), None)
            cliente2 = next((c for c in modClientes.clientes if c.idCliente == lista[j + 1].idCliente), None)

            if not cliente1 or not cliente2:
                continue  # Si no se encuentra el cliente, se salta

            nombre1 = cliente1.nombre.lower() if case_insensitive else cliente1.nombre
            nombre2 = cliente2.nombre.lower() if case_insensitive else cliente2.nombre

            # Intercambio manual
            if nombre1 > nombre2:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista



# --- Búsqueda binaria por nombre (insensible y parcial) ---
def busquedaBinariaPorNombreServicio(lista_servicios, texto, case_insensitive=True):
    """
    Busca servicios usando el nombre del cliente asociado (ya cargados en memoria).
    No recarga los clientes internamente.
    """
    if not lista_servicios or not modClientes.clientes:
        return []

    texto = texto.lower().strip()

    lista_ordenada = ordenarServiciosPorNombreCliente(lista_servicios[:], case_insensitive)
    izquierda, derecha = 0, len(lista_ordenada) - 1
    resultados = []

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        servicio = lista_ordenada[medio]

        cliente = next((c for c in modClientes.clientes if c.idCliente == servicio.idCliente), None)
        if not cliente:
            break

        nombre_actual = cliente.nombre.lower() if case_insensitive else cliente.nombre

        if texto in nombre_actual:
            resultados.append(servicio)

            # Buscar coincidencias a izquierda y derecha
            i = medio - 1
            while i >= 0:
                c_izq = next((c for c in modClientes.clientes if c.idCliente == lista_ordenada[i].idCliente), None)
                if not c_izq or texto not in c_izq.nombre.lower():
                    break
                resultados.append(lista_ordenada[i])
                i -= 1

            i = medio + 1
            while i < len(lista_ordenada):
                c_der = next((c for c in modClientes.clientes if c.idCliente == lista_ordenada[i].idCliente), None)
                if not c_der or texto not in c_der.nombre.lower():
                    break
                resultados.append(lista_ordenada[i])
                i += 1
            break

        elif nombre_actual < texto:
            izquierda = medio + 1
        else:
            derecha = medio - 1

    return resultados



# --- Búsqueda secuencial por nombre (insensible y parcial) ---
def busquedaSecuencialPorNombre(lista, texto, case_insensitive=True):
    texto = texto.lower().strip()
    return [cliente for cliente in lista if texto in cliente.nombre.lower()]


# --- Hash simple para búsqueda rápida por nombre ---
def crearTablaHash(clientes):
    """Crea una tabla hash con clave = nombre en minúsculas, valor = objeto cliente"""
    tabla = {}
    for c in clientes:
        tabla[c.nombre.lower().strip()] = c
    return tabla


def buscarHash(tabla, texto):
    """Devuelve cliente(s) cuyo nombre coincida parcial o completamente"""
    texto = texto.lower().strip()
    resultados = []
    for clave, cliente in tabla.items():
        if texto in clave:
            resultados.append(cliente)
    return resultados
