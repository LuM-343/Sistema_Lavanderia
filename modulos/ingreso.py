#Modulo de ingresos

class Ingreso:
    def __init__(self, idIngreso, monto, concepto, fecha):
        self.idIngreso = idIngreso
        self.monto = monto
        self.concepto = concepto
        self.fecha = fecha

    def aDiccionario(self):
        return {
            "id_ingreso": self.idIngreso,
            "monto": self.monto,
            "concepto": self.concepto,
            "fecha": self.fecha
        }

    @staticmethod
    def deDiccionario(data):
        return Ingreso(
            data["idIngreso"],
            data["monto"],
            data["concepto"],
            data["fecha"]
        )
