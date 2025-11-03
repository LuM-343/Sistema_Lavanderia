#Modulo de clientes

class Cliente:
    def __init__(self, idCliente, nombre, telefono, direccion, extra):
        self.idCliente=idCliente
        self.nombre=nombre
        self.telefono=telefono
        self.direccion=direccion
        self.extra=extra
        self.lavadas=[]

    def agregarLavada(self,lavada):
        self.lavadas.append(lavada)

    def totalLavadas(self):
        return len(self.lavadas)
    
    def aDiccionario(self):
        return{
            "idCliente":self.idCliente,
            "nombre":self.nombre,
            "telefono":self.telefono,
            "direccion":self.direccion,
            "extra":self.extra,
            "lavadas":[lavada.aDictado() for lavada in self.lavadas]
        }
    
    @staticmethod
    def deDiccionario(data):
        cliente = Cliente(
            data["id_cliente"],
            data["nombre"],
            data["telefono"],
            data["direccion"]
        )
        from lavada import Lavada  
        cliente.lavadas = [Lavada.from_dict(d) for d in data["lavadas"]]
        return cliente