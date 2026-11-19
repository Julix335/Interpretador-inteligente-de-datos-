import math

def validar_nombre(nombre):
    """
    Comprueba que el nombre de una variable
    no esté vacío.
    """
    if not isinstance(nombre, str) or not nombre.strip():
        raise ValueError("El nombre no puede estar vacío.")

    return nombre.strip()


def validar_numero(valor, nombre_variable):
    """
    Comprueba que el valor ingresado sea
    un número válido y finito.
    """
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
    """
    Valida las coordenadas X y Y y evita
    que se repita un valor de X.
    """
    x = validar_numero(x, "X")
    y = validar_numero(y, "Y")

    if x in datos["x"]:
        raise ValueError(
            "Ya existe un punto con ese valor de X."
        )

    return x, y
