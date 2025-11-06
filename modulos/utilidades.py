#busquedas

def busquedaSecuencial(lista, objetivo, atributo):
    for i in range(len(lista)):
        if getattr(lista[i], atributo) == objetivo:
            return i
    return -1


def busquedaBinaria(lista, objetivo, atributo): #Se busca la coincidencia a partir del valor deseado
    inicio = 0
    listaOrdenada=selectionSort(lista)
    fin = len(listaOrdenada) - 1

    while inicio <= fin:
        medio = (inicio + fin) // 2
        valor = getattr(listaOrdenada[medio], atributo)

        if valor == objetivo:
            return listaOrdenada[medio]
        elif valor < objetivo:
            inicio = medio + 1
        else:
            fin = medio - 1
    return None


def crearHash(lista, atributo="idCliente"): #Función hash donde se guardaran para la búsqueda, se implemento así, 
    #porque ya se tenia creada la base de datos y hubiera sido más complicado re hacer eso
    tabla = {}
    for elemento in lista:
        clave = getattr(elemento, atributo)
        tabla[clave] = elemento
    return tabla

def buscarHash(tabla_hash, clave):  #Accedemos a la hash creada mediante un get al diccionario
    return tabla_hash.get(clave, None)


# Algoritmos de ordenamiento

def bubbleSort(lista, atributo):
    """Ordena usando Bubble Sort"""
    n = len(lista)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if getattr(lista[j], atributo) > getattr(lista[j + 1], atributo):
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista


def selectionSort(lista, atributo):
    n = len(lista)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if getattr(lista[j], atributo) < getattr(lista[min_idx], atributo):
                min_idx = j
        lista[i], lista[min_idx] = lista[min_idx], lista[i]
    return lista


def quickSort(lista, atributo):
    if len(lista) <= 1:
        return lista
    else:
        pivote = lista[len(lista)//2]
        menores = [x for x in lista if getattr(x, atributo) < pivote]
        iguales = [x for x in lista if getattr(x, atributo) == pivote]
        mayores = [x for x in lista if getattr(x, atributo) > pivote]

        return quickSort(menores, atributo) + iguales + quickSort(mayores, atributo)
    