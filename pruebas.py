import datetime
import random

def generar_id_unico_fecha():
    a = datetime.datetime.now()
    return int(f"{a.strftime("%y")}{a.strftime("%m")}{a.strftime("%d")}{a.strftime("%H")}{random.randint(100,999)}")

id_unico = generar_id_unico_fecha()
print(id_unico)
