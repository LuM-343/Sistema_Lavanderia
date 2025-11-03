#MODULO DE LAVADAS

class Lavada:
    def __init__(self, idLavada, pesoLB, precio, fecha, estado="Pendiente", pago="Pendiente"):
        self.idLavada = idLavada
        self.pesoLB = pesoLB
        self.precio = precio
        self.fecha = fecha  # string o datetime
        self.estado = estado  # Pendiente / Finalizado / Olvidado
        self.pago=pago

    def marcarFinalizado(self):
        self.estado = "Finalizado"
    
    def marcarOlvidado(self):
        self.estado = "Olvidado"

    def aDiccionario(self):
        return {
            "id_lavada": self.idLavada,
            "pesoLB": self.pesoLB,
            "precio": self.precio,
            "fecha": self.fecha,
            "estado": self.estado
        }

    @staticmethod
    def deDicionario(data):
        return Lavada(
            data["idLavada"],
            data["pesoLB"],
            data["precio"],
            data["fecha"],
            data["estado"]
        )
