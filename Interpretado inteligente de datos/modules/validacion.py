
import math


def validar_nombre(nombre):
    if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError("El nombre no puede estar vacío.")

    return nombre.strip()


def validar_numero(valor, nombre_variable):
    try:
        numero = float(valor)

    except (ValueError, TypeError):
        raise ValueError(
            f"{nombre_variable} debe ser numérico."
        )

    if not math.isfinite(numero):
        raise ValueError(
            f"{nombre_variable} debe ser un número finito."
        )

    return numero


def validar_punto(x, y, datos):
    x = validar_numero(x, "X")
    y = validar_numero(y, "Y")

    # Evitar valores de X repetidos
    if x in datos["x"]:
        raise ValueError(
            "Ya existe un punto con ese valor de X."
        )

    # Validar la distancia respecto al último X ingresado
    ultimo_x = datos["ultimo_x"]

    if ultimo_x is not None and abs(x - ultimo_x) > 12:
        raise ValueError(
            "El nuevo valor de X no puede estar a más "
            "de 12 unidades del último X ingresado."
        )

    return x, y
