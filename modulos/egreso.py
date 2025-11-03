#Modulo egresos
class Egreso:
    def __init__(self, id_egreso, monto, descripcion, fecha):
        self.id_egreso = id_egreso
        self.monto = monto
        self.descripcion = descripcion
        self.fecha = fecha

    def aDiccionario(self):
        return {
            "id_egreso": self.id_egreso,
            "monto": self.monto,
            "descripcion": self.descripcion,
            "fecha": self.fecha
        }

    @staticmethod
    def deDiccionario(data):
        return Egreso(
            data["id_egreso"],
            data["monto"],
            data["descripcion"],
            data["fecha"]
        )
