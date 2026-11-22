from modules.validacion import (
    validar_nombre,
    validar_punto
)


def crear_conjunto(nombre_x, nombre_y):

    datos = {
        "nombre_x": validar_nombre(nombre_x),
        "nombre_y": validar_nombre(nombre_y),
        "x": [],
        "y": [],
        "matriz": [],
        "ultimo_x": None
    }

    return datos


def agregar_punto(datos, x, y):

    x, y = validar_punto(x, y, datos)
    datos["ultimo_x"] = x

    datos["x"].append(x)
    datos["y"].append(y)

    # Ordenar los puntos según X
    puntos = sorted(zip(datos["x"], datos["y"]))

    datos["x"] = [punto[0] for punto in puntos]
    datos["y"] = [punto[1] for punto in puntos]

    # Actualizar la matriz
    datos["matriz"] = [
        [punto[0], punto[1]]
        for punto in puntos
    ]

    return datos


def mostrar_datos(datos):

    print("\n========== DICCIONARIO ==========")
    print(datos)

    print("\n========== MATRIZ ==========")

    for fila in datos["matriz"]:
        print(fila)

def contar_puntos(datos):
    """
    Cuenta la cantidad de puntos registrados.
    """
    return len(datos["x"])


def consultar_puntos(datos):
    """
    Devuelve todos los puntos almacenados.
    """
    return list(zip(datos["x"], datos["y"]))
