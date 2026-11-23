# generar_avistamientos.py  -> RESPONSABLE: Fresshy (Ítem 3)
from conexion import obtener_bd
from subrutinas import generar_avistamientos

if __name__ == "__main__":
    total = generar_avistamientos(obtener_bd(), 10000)
    print(f"Avistamientos generados: {total}")
