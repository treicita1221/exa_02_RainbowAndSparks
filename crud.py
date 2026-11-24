from conexion import obtener_bd
from subrutinas import (insertar_categoria, modificar_categoria, borrar_categoria,
                        insertar_observador, modificar_observador, borrar_observador)


def menu():
    bd = obtener_bd()
    while True:
        print("\n--- CRUD RCOFA ---")
        print("1. Insertar categoría   2. Modificar categoría   3. Borrar categoría")
        print("4. Insertar observador  5. Modificar observador  6. Borrar observador")
        print("0. Salir")
        op = input("Opción: ").strip()
        try:
            if op == "1":
                insertar_categoria(bd, int(input("ID: ")), input("Nombre: "), input("Descripción: "))
                print("Listo.")
            elif op == "2":
                r = modificar_categoria(bd, int(input("ID: ")), {"nombre": input("Nuevo nombre: ")})
                print("Listo." if r.matched_count else "No existe una categoría con ese ID.")
            elif op == "3":
                r = borrar_categoria(bd, int(input("ID: ")))
                print("Listo." if r.deleted_count else "No existe una categoría con ese ID.")
            elif op == "4":
                insertar_observador(bd, int(input("ID: ")), input("Alias/estación: "),
                                    input("Rol: "), float(input("Confiabilidad (0-1): ")))
                print("Listo.")
            elif op == "5":
                r = modificar_observador(bd, int(input("ID: ")),
                                         {"indice_confiabilidad": float(input("Nueva confiabilidad: "))})
                print("Listo." if r.matched_count else "No existe un observador con ese ID.")
            elif op == "6":
                r = borrar_observador(bd, int(input("ID: ")))
                print("Listo." if r.deleted_count else "No existe un observador con ese ID.")
            elif op == "0":
                break
            else:
                print("Opción inválida.")
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    menu()
