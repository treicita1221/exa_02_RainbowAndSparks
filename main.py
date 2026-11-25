# main.py  -> menú general (Tracy integra al final)
from conexion import obtener_bd
import carga_datos, crud, consultas_fenomenos
from subrutinas import generar_avistamientos
from datetime import datetime

bd = obtener_bd()
while True:
    print("\n=== RCOFA ===\n1. Cargar datos\n2. CRUD\n3. Generar 10 000 avistamientos\n4. Consultas\n0. Salir")
    op = input("Opción: ").strip()
    if op == "1":
        carga_datos.cargar_ubicaciones(bd); carga_datos.cargar_categorias(bd); carga_datos.cargar_observadores(bd)
    elif op == "2":
        crud.menu()
    elif op == "3":
        print("Generados:", generar_avistamientos(bd, 10000))
    elif op == "4":
        consultas_fenomenos.consulta_filtro_proyeccion(bd, "Puntarenas")
        consultas_fenomenos.consulta_rango_fechas(bd, datetime(2025, 10, 1), datetime(2025, 10, 3, 23, 59, 59))
        consultas_fenomenos.filtro_python(consultas_fenomenos.agregacion_lookup(bd))
    elif op == "0":
        break
