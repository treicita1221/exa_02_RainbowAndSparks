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
            elif op == "2":
                modificar_categoria(bd, int(input("ID: ")), {"nombre": input("Nuevo nombre: ")})
            elif op == "3":
                borrar_categoria(bd, int(input("ID: ")))
            elif op == "4":
                insertar_observador(bd, int(input("ID: ")), input("Alias/estación: "),
                                    input("Rol: "), float(input("Confiabilidad (0-1): ")))
            elif op == "5":
                modificar_observador(bd, int(input("ID: ")),
                                     {"indice_confiabilidad": float(input("Nueva confiabilidad: "))})
            elif op == "6":
                borrar_observador(bd, int(input("ID: ")))
            elif op == "0":
                break
            print("Listo.")
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    menu()
