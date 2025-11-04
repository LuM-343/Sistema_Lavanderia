def busquedaSecuencial(lista, objetivo, atributo):
    for i in range(len(lista)):
        if getattr(lista[i], atributo) == objetivo:
            return i
    return -1
