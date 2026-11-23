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
def pon_ceros(numero: int, largo: int = 8) -> str:
    return str(numero).zfill(largo)


def fecha_aleatoria() -> datetime:
    """Crea una fecha como TEXTO y la convierte con datetime.strptime (lo pide el examen)."""
    inicio = datetime(2024, 1, 1)
    segundos = random.randint(0, 2 * 365 * 24 * 3600)
    texto = (inicio + timedelta(seconds=segundos)).strftime("%d/%m/%Y %H:%M:%S")
    return datetime.strptime(texto, "%d/%m/%Y %H:%M:%S")


def generar_avistamientos(bd, cantidad: int = 10000):
    ubicaciones = list(bd.ubicaciones.find({}, {"_id": 0}))
    categorias = [c["_id"] for c in bd.categorias_fenomeno.find({}, {"_id": 1})]
    observadores = list(bd.observadores.find())
    if not (ubicaciones and categorias and observadores):
        raise RuntimeError("Primero ejecute carga_datos.py")

    lote = []
    for i in range(1, cantidad + 1):
        u = random.choice(ubicaciones)
        obs = random.choice(observadores)
        codigo = "REP-" + pon_ceros(i)
        doc = {
            "_id": codigo,
            "codigo_reporte": codigo,
            "fecha_evento": fecha_aleatoria(),
            "duracion_seg": random.randint(1, 600),
            "id_categoria": random.choice(categorias),
            "id_observador": obs["_id"],
            "ubicacion": {
                "id_sector": "SEC-" + pon_ceros(random.randint(1, 999), 3),
                "provincia": u.get("provincia", ""),
                "canton": u.get("canton", ""),
                "distrito": u.get("distrito", ""),
                "localidad": u.get("poblado", u.get("localidad", "")),
            },
        }
        # --- Campos que NO todos los documentos tienen (documentos no uniformes) ---
        rol = obs.get("rol", "")
        if rol == "Estación meteorológica" or random.random() < 0.3:
            doc["telemetria_entorno"] = {
                "visibilidad_km": round(random.uniform(0.5, 30), 1),
                "nubosidad_pct": random.randint(0, 100),
                "viento_nudos": round(random.uniform(0, 40), 1)}
        if rol == "Operador radar":
            doc["frecuencia_mhz"] = round(random.uniform(30, 3000), 2)
            doc["eco_radar_db"] = round(random.uniform(-20, 60), 1)
        if rol == "Testigo ciudadano":
            doc["testigos_adicionales"] = random.randint(0, 5)
            if random.random() < 0.4:
                doc["evidencia"] = {"tipo": random.choice(["foto", "video", "audio"]),
                                    "archivos": random.randint(1, 4)}
        if random.random() < 0.15:
            doc["efecto_fauna"] = random.choice(
                ["aves inquietas", "perros ladrando", "ganado agitado", "silencio de insectos"])
        lote.append(doc)

    bd.avistamientos.delete_many({})
    bd.avistamientos.insert_many(lote)
    return len(lote)


# =====================================================================
# SECCIÓN TRACY - Ítem 4: función auxiliar de fecha
# =====================================================================
MESES = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
         7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}


def formatear_fecha(fecha: datetime) -> str:
    return f"{fecha.day:02d} de {MESES[fecha.month]} de {fecha.year}, {fecha:%H:%M}"



