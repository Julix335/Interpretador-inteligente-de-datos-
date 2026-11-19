from modules.datos import (
    crear_conjunto,
    agregar_punto,
    mostrar_datos,
    contar_puntos,
    consultar_puntos
)


def solicitar_cantidad():
    """
    Solicita la cantidad de puntos que se van a ingresar.
    """
    while True:
        try:
            cantidad = int(
                input("\n¿Cuántos puntos desea ingresar?: ")
            )

            if cantidad <= 0:
                print("La cantidad debe ser mayor que cero.")
                continue

            return cantidad

        except ValueError:
            print("Error: debe ingresar un número entero.")


def main():

    print("======================================")
    print("   INTERPRETADOR INTELIGENTE DE DATOS")
    print("======================================")

    # Solicitar nombres de las variables
    nombre_x = input("\nNombre de la variable X: ")
    nombre_y = input("Nombre de la variable Y: ")

    try:
        datos = crear_conjunto(nombre_x, nombre_y)

    except ValueError as error:
        print("\nError:", error)
        return

    # Solicitar cantidad de puntos
    cantidad = solicitar_cantidad()

    # Ingresar los puntos iniciales
    for i in range(cantidad):

        print(f"\n--- Punto {i + 1} ---")

        while True:
            try:
                x = input(f"Ingrese {nombre_x}: ")
                y = input(f"Ingrese {nombre_y}: ")

                agregar_punto(datos, x, y)

                print("Punto agregado correctamente.")
                break

            except ValueError as error:
                print("Error:", error)

    # Mostrar los datos almacenados
    mostrar_datos(datos)
    print("\n========== RESUMEN ==========")
    print("Cantidad de puntos:", contar_puntos(datos))
    print("Puntos registrados:", consultar_puntos(datos))

    # Permitir agregar nuevos puntos
    while True:

        respuesta = input(
            "\n¿Desea agregar otro punto? (s/n): "
        ).strip().lower()

        if respuesta == "n":
            break

        elif respuesta == "s":

            try:
                x = input(f"Ingrese {nombre_x}: ")
                y = input(f"Ingrese {nombre_y}: ")

                agregar_punto(datos, x, y)

                print("\nPunto agregado correctamente.")

                mostrar_datos(datos)

            except ValueError as error:
                print("Error:", error)

        else:
            print("Respuesta no válida. Escriba s o n.")

    print("\n======================================")
    print("       PROGRAMA FINALIZADO")
    print("======================================")


if __name__ == "__main__":
    main()
