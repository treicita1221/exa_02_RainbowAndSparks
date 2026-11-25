# consultas_fenomenos.py  -> RESPONSABLE: Tracy (Ítem 4)
from datetime import datetime
from conexion import obtener_bd
from subrutinas import formatear_fecha


def consulta_filtro_proyeccion(bd, provincia="Puntarenas"):
    print(f"\n=== 1) Avistamientos en {provincia} ===")
    cursor = (bd.avistamientos
              .find({"ubicacion.provincia": {"$eq": provincia}},
                    {"_id": 0, "codigo_reporte": 1, "fecha_evento": 1,
                     "duracion_seg": 1, "ubicacion.localidad": 1})
              .sort([("duracion_seg", -1), ("fecha_evento", 1)])
              .limit(10))
    for d in cursor:
        print(d["codigo_reporte"], d["duracion_seg"], "s",
              formatear_fecha(d["fecha_evento"]), d["ubicacion"]["localidad"])


def consulta_rango_fechas(bd, desde, hasta):
    print(f"\n=== 2) Reportes entre {formatear_fecha(desde)} y {formatear_fecha(hasta)} ===")
    cursor = bd.avistamientos.find({"fecha_evento": {"$gte": desde, "$lte": hasta}}).sort("fecha_evento", 1)
    total = 0
    for d in cursor:
        total += 1
        if total <= 15:
            print(d["codigo_reporte"], "-", formatear_fecha(d["fecha_evento"]))
    print("Total encontrados:", total)


def agregacion_lookup(bd, limite=10):
    print("\n=== 3) Reporte con $lookup ===")
    pipeline = [
        {"$lookup": {"from": "categorias_fenomeno", "localField": "id_categoria",
                     "foreignField": "_id", "as": "categoria"}},
        {"$lookup": {"from": "observadores", "localField": "id_observador",
                     "foreignField": "_id", "as": "observador"}},
        {"$unwind": "$categoria"},
        {"$unwind": "$observador"},
        {"$project": {"_id": 0, "codigo": "$codigo_reporte", "duracion_seg": 1,
                      "fenomeno": "$categoria.nombre", "observador": "$observador.alias_o_estacion",
                      "localidad": "$ubicacion.localidad"}},
    ]
    resultados = list(bd.avistamientos.aggregate(pipeline))
    for r in resultados[:limite]:
        print(f"{r['codigo']} | {r['fenomeno']:<30} | {r['observador']:<22} | {r['localidad']}")
    return resultados


def filtro_python(resultados):
    print("\n=== 4) Reportes con duración > 200 s (list comprehension y filter+lambda) ===")
    largos = [r for r in resultados if r["duracion_seg"] > 200]
    largos2 = list(filter(lambda r: r["duracion_seg"] > 200, resultados))
    print("Con list comprehension:", len(largos), "| con filter+lambda:", len(largos2))
    for r in largos[:5]:
        print(r["codigo"], r["duracion_seg"], "s")


if __name__ == "__main__":
    bd = obtener_bd()
    consulta_filtro_proyeccion(bd, "Puntarenas")
    consulta_rango_fechas(bd, datetime(2025, 10, 1), datetime(2025, 10, 3, 23, 59, 59))
    res = agregacion_lookup(bd)
    filtro_python(res)
