from modules.datos import (
    agregar_punto,
    consultar_puntos,
    contar_puntos,
    crear_conjunto,
    mostrar_datos,
)
from modules.deteccion import (
    detectar_anomalias,
    detectar_cambios_tendencia,
    detectar_saltos_tiempo,
    evaluar_modelo_global,
)
from modules.analisis import (
    analizar
)
from modules.graficas import graficar_global, graficar_local

# Si el archivo de tu compañero ya tiene estas funciones listas, descomenta
# y ajusta los nombres si se llaman distinto en modules/analisis.py:
# from modules.analisis import analisis_global, analisis_local


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

    # --- Bloque de análisis, evaluación, detección y gráficas ---
    # Asegúrate de que `datos` tenga las claves "x" y "y" (o ajusta aquí si se llaman distinto).
    ventana = 4

    # Descomenta estas dos líneas cuando conecten modules/analisis.py:
    # resultado_global = analisis_global(datos)
    # resultados_locales = analisis_local(datos, ventana=ventana)

    # Por si aún no conectan analisis.py, evitamos que se rompa si no existen esas variables:
    if "resultado_global" in locals() and "resultados_locales" in locals():
        evaluacion = evaluar_modelo_global(datos, resultado_global)
        anomalias = detectar_anomalias(datos, resultado_global)
        cambios = detectar_cambios_tendencia(resultados_locales, datos, ventana=ventana)
        saltos = detectar_saltos_tiempo(datos)

        print(f"\nR² global: {evaluacion['r2']:.4f} | MAE: ${evaluacion['mae']:,.2f}")

        if saltos:
            print("\n--- Avisos de tiempo ---")
            for s in saltos:
                print("-", s["mensaje"])

        if anomalias:
            print("\n--- Anomalías detectadas ---")
            for a in anomalias:
                print("-", a["mensaje"])

        if cambios:
            print("\n--- Cambios de tendencia ---")
            for c in cambios:
                print("-", c["mensaje"])

        graficar_global(datos, resultado_global, anomalias=anomalias, evaluacion=evaluacion)
        graficar_local(
            datos,
            resultados_locales,
            anomalias=anomalias,
            cambios=cambios,
            resultado_global=resultado_global,
            ventana=ventana,
        )
    else:
        saltos = detectar_saltos_tiempo(datos)
        if saltos:
            print("\n--- Avisos de tiempo ---")
            for s in saltos:
                print("-", s["mensaje"])
        print("\nNota: conecta `resultado_global` y `resultados_locales` desde `modules.analisis` para activar detección completa y gráficas.")

    print("\n======================================")
    print("       PROGRAMA FINALIZADO")
    print("======================================")


if __name__ == "__main__":
    main()
