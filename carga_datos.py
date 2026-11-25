from conexion import obtener_bd
from subrutinas import leer_ubicaciones_csv

def cargar_ubicaciones(bd, ruta="ubicaciones.csv"):
    datos = leer_ubicaciones_csv(ruta)
    bd.ubicaciones.delete_many({})
    bd.ubicaciones.insert_many(datos)
    print(f"Ubicaciones cargadas: {len(datos)}")

def cargar_categorias(bd):
    bd.categorias_fenomeno.delete_many({})
    categorias = [
        (1, "Luminaria estacionaria", "Luz fija en el cielo por varios minutos"),
        (2, "Eco radar no identificado", "Señal en radar sin aeronave registrada"),
        (3, "Estela luminosa", "Rastro de luz que cruza el cielo"),
        (4, "Objeto Volador NO Identificado", "Objeto con forma o movimiento inusual"),
        (5, "Alteración magnética", "Cambio brusco en brújulas o magnetómetros"),
    ]
    for _id, nombre, desc in categorias:          # insert_one (lo pide el examen)
        bd.categorias_fenomeno.insert_one({"_id": _id, "nombre": nombre, "descripcion": desc})
    print("Categorías cargadas:", len(categorias))


def cargar_observadores(bd):
    bd.observadores.delete_many({})
    observadores = [                               # insert_many (lo pide el examen)
        {"_id": 1, "alias_o_estacion": "Vigía Esparza", "rol": "Testigo ciudadano", "indice_confiabilidad": 0.62},
        {"_id": 2, "alias_o_estacion": "Radar Caldera", "rol": "Operador radar", "indice_confiabilidad": 0.91},
        {"_id": 3, "alias_o_estacion": "EM-Puntarenas", "rol": "Estación meteorológica", "indice_confiabilidad": 0.97},
        {"_id": 4, "alias_o_estacion": "Ojo de Nicoya", "rol": "Testigo ciudadano", "indice_confiabilidad": 0.45},
        {"_id": 5, "alias_o_estacion": "Radar Limón", "rol": "Operador radar", "indice_confiabilidad": 0.88},
        {"_id": 6, "alias_o_estacion": "EM-Cerro de la Muerte", "rol": "Estación meteorológica", "indice_confiabilidad": 0.95},
    ]
    bd.observadores.insert_many(observadores)
    print("Observadores cargados:", len(observadores))


if __name__ == "__main__":
    bd = obtener_bd()
    cargar_ubicaciones(bd)
    cargar_categorias(bd)
    cargar_observadores(bd)
