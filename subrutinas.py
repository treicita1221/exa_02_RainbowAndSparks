# subrutinas.py  -> aquí van TODAS las funciones
import csv
import random
import unicodedata
from datetime import datetime, timedelta

# =====================================================================
# SECCIÓN JUSTIN - Ítem 1: clasificar tipo de zona y leer ubicaciones
# =====================================================================
# (aquí va el código de Justin)


# =====================================================================
# SECCIÓN EMILY - Ítem 2: CRUD de categorias_fenomeno y observadores
# =====================================================================
# (aquí va el código de Emily)


# =====================================================================
# SECCIÓN FRESSHY - Ítem 3: 10 000 avistamientos sintéticos
# =====================================================================
# (aquí va el código de Fresshy)


# =====================================================================
# SECCIÓN TRACY - Ítem 4: función auxiliar de fecha
# =====================================================================
MESES = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
         7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}


def formatear_fecha(fecha: datetime) -> str:
    return f"{fecha.day:02d} de {MESES[fecha.month]} de {fecha.year}, {fecha:%H:%M}"



