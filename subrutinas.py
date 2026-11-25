# subrutinas.py  -> aquí van TODAS las funciones
import csv
import random
import unicodedata
from datetime import datetime, timedelta

# =====================================================================
# SECCIÓN JUSTIN - Ítem 1: clasificar tipo de zona y leer ubicaciones
# =====================================================================
CANTONES_COSTEROS = {"Puntarenas", "Esparza", "Montes de Oro", "Osa", "Quepos", "Golfito",
    "Parrita", "Corredores", "Garabito", "Liberia", "Nicoya", "Santa Cruz", "Bagaces",
    "Carrillo", "Cañas", "Abangares", "Nandayure", "La Cruz", "Hojancha", "Limón", "Pococí",
    "Siquirres", "Talamanca", "Matina", "Guácimo"}

CANTONES_MONTANOSOS = {"Tarrazú", "Aserrí", "Mora", "Acosta", "Turrubares", "Dota",
    "Pérez Zeledón", "León Cortés", "Puriscal", "San Ramón", "Zarcero", "Poás", "Valverde Vega",
    "Paraíso", "Jiménez", "Turrialba", "Alvarado", "Oreamuno", "El Guarco", "Barva",
    "Santa Bárbara", "San Rafael", "San Isidro", "Tilarán", "Buenos Aires", "Coto Brus"}

POBLADOS_INSULARES = {"Isla del Coco", "Isla Chira", "Isla Venado", "Isla Caballo",
    "Isla San Lucas", "Isla Tortuga", "Isla Cedros", "Isla Jesucita", "Isla Berrugate"}


def normalizar(texto: str) -> str:
    """Quita tildes, espacios extra y pasa a minúscula para comparar sin errores."""
    texto = unicodedata.normalize("NFD", str(texto or ""))
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return " ".join(texto.lower().split())


_COSTEROS = {normalizar(c) for c in CANTONES_COSTEROS}
_MONTANOSOS = {normalizar(c) for c in CANTONES_MONTANOSOS}
_INSULARES = {normalizar(p) for p in POBLADOS_INSULARES}


def clasificar_tipo_zona(provincia: str, canton: str, poblado: str) -> str:
    """Orden: primero isla, luego costa, luego montaña; si no, Urbana."""
    if normalizar(poblado) in _INSULARES:
        return "Insular"
    if normalizar(canton) in _COSTEROS:
        return "Costera"
    if normalizar(canton) in _MONTANOSOS:
        return "Montañosa"
    return "Urbana"


def leer_ubicaciones_csv(ruta: str) -> list:
    """Lee ubicaciones.csv y devuelve una lista de diccionarios con tipo_zona agregado.
    OJO: revisen los nombres de columnas de SU csv y ajusten COLUMNAS si cambian."""
    COLUMNAS = {"provincia": "provincia", "canton": "canton",
                "distrito": "distrito", "poblado": "poblado"}
    ubicaciones = []
    with open(ruta, encoding="utf-8-sig", newline="") as archivo:
        muestra = archivo.read(2048)
        archivo.seek(0)
        separador = ";" if muestra.count(";") > muestra.count(",") else ","
        lector = csv.DictReader(archivo, delimiter=separador)
        for fila in lector:
            fila = {normalizar(k): (v or "").strip() for k, v in fila.items() if k}
            provincia = fila.get(COLUMNAS["provincia"], "")
            canton = fila.get(COLUMNAS["canton"], "")
            distrito = fila.get(COLUMNAS["distrito"], "")
            poblado = fila.get(COLUMNAS["poblado"], fila.get("localidad", ""))
            fila["tipo_zona"] = clasificar_tipo_zona(provincia, canton, poblado)
            ubicaciones.append(fila)
    return ubicaciones


# =====================================================================
# SECCIÓN EMILY - Ítem 2: CRUD de categorias_fenomeno y observadores
# =====================================================================
def insertar_categoria(bd, _id: int, nombre: str, descripcion: str):
    return bd.categorias_fenomeno.insert_one(
        {"_id": _id, "nombre": nombre, "descripcion": descripcion})


def modificar_categoria(bd, _id: int, cambios: dict):
    return bd.categorias_fenomeno.update_one({"_id": _id}, {"$set": cambios})


def borrar_categoria(bd, _id: int):
    return bd.categorias_fenomeno.delete_one({"_id": _id})


def insertar_observador(bd, _id: int, alias: str, rol: str, confiabilidad: float):
    if not 0.0 <= confiabilidad <= 1.0:
        raise ValueError("indice_confiabilidad debe estar entre 0.0 y 1.0")
    return bd.observadores.insert_one({"_id": _id, "alias_o_estacion": alias,
                                       "rol": rol, "indice_confiabilidad": confiabilidad})


def modificar_observador(bd, _id: int, cambios: dict):
    if "indice_confiabilidad" in cambios and not 0.0 <= cambios["indice_confiabilidad"] <= 1.0:
        raise ValueError("indice_confiabilidad debe estar entre 0.0 y 1.0")
    return bd.observadores.update_one({"_id": _id}, {"$set": cambios})


def borrar_observador(bd, _id: int):
    return bd.observadores.delete_one({"_id": _id})


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



