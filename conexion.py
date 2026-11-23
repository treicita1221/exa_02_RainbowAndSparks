# conexion.py  -> RESPONSABLE: Tracy (Paso 0)
from pymongo import MongoClient

URI = "mongodb://localhost:27017/"   # cambiar si usan MongoDB Atlas
NOMBRE_BD = "rcofa"

def obtener_bd():
    cliente = MongoClient(URI)
    return cliente[NOMBRE_BD]
