import numpy as np
from sklearn.metrics import mean_absolute_error, r2_score


def evaluar_modelo_global(datos, resultado_global):
    """
    Evalúa el ajuste de la recta global de ganancias usando numpy y scikit-learn.
    """
    x = np.asarray(datos["x"], dtype=float)
    y = np.asarray(datos["y"], dtype=float)

    pendiente = resultado_global["pendiente"]
    intercepto = resultado_global["intercepción con eje y"]
    y_estimados = pendiente * x + intercepto

    if len(y) >= 2 and np.var(y) > 0:
        r2 = float(r2_score(y, y_estimados))
    else:
        r2 = 1.0 if np.allclose(y, y_estimados) else 0.0

    error_promedio = float(mean_absolute_error(y, y_estimados))

    return {
        "r2": r2,
        "mae": error_promedio,
        "y_estimados": y_estimados.tolist(),
    }


def detectar_anomalias(datos, resultado_global):
    """
    Detecta períodos con ganancias atípicas (muy por encima o por debajo
    de la recta de tendencia global) usando residuos y MAD con numpy.
    """
    x = np.asarray(datos["x"], dtype=float)
    y = np.asarray(datos["y"], dtype=float)
    nombre_x = datos.get("nombre_x", "Período")

    if len(x) < 3:
        return []

    pendiente = resultado_global["pendiente"]
    intercepto = resultado_global["intercepción con eje y"]

    y_estimados = pendiente * x + intercepto
    diferencias = y - y_estimados
    residuos = np.abs(diferencias)

    mediana = float(np.median(residuos))
    mad = float(np.median(np.abs(residuos - mediana)))

    if mad == 0 and mediana == 0:
        return []
    limite = mediana + 2 * 1.4826 * mad if mad > 0 else mediana * 1.5
    anomalias = []
    for i in range(len(x)):
        if residuos[i] > limite:
            tipo = (
                "Ganancia inusualmente alta"
                if diferencias[i] > 0
                else "Caída inusual de ganancia"
            )
            anomalias.append({
                "indice": i,
                "x": float(x[i]),
                "y": float(y[i]),
                "esperado": float(y_estimados[i]),
                "diferencia": float(diferencias[i]),
                "tipo": tipo,
                "mensaje": (
                    f"{tipo} en {nombre_x} {x[i]:g}: "
                    f"ganancia de ${y[i]:,.2f} (esperado según tendencia: ${y_estimados[i]:,.2f})."
                ),
            })

    return anomalias
def detectar_cambios_tendencia(resultados_locales, datos, ventana=4):
    """
    Compara ventanas locales consecutivas para identificar cambios
    de dirección en las ganancias (crecimiento <-> decrecimiento).
    """
    x = datos["x"]
    nombre_x = datos.get("nombre_x", "Período")
    cambios = []

    for i in range(1, len(resultados_locales)):
        anterior = resultados_locales[i - 1]
        actual = resultados_locales[i]
        m_ant = anterior["pendiente"]
        m_act = actual["pendiente"]
        inicio_act = actual.get("inicio", i)
        fin_act = min(actual.get("fin", i + ventana - 1), len(x) - 1)

        if m_ant > 0 and m_act < 0:
            cambios.append({
                "tipo": "Cambio de crecimiento a decrecimiento",
                "ventana": i + 1,
                "indice_inicio": inicio_act,
                "indice_fin": fin_act,
                "x_referencia": x[fin_act],
                "pendiente_anterior": m_ant,
                "pendiente_actual": m_act,
                "mensaje": (
                    f"Cambio de crecimiento a decrecimiento hacia {nombre_x} {x[fin_act]:g} "
                    f"(pendiente pasó de {m_ant:+.2f} a {m_act:+.2f})."
                ),
            })
        elif m_ant < 0 and m_act > 0:
            cambios.append({
                "tipo": "Cambio de decrecimiento a crecimiento",
                "ventana": i + 1,
                "indice_inicio": inicio_act,
                "indice_fin": fin_act,
                "x_referencia": x[fin_act],
                "pendiente_anterior": m_ant,
                "pendiente_actual": m_act,
                "mensaje": (
                    f"Cambio de decrecimiento a crecimiento hacia {nombre_x} {x[fin_act]:g} "
                    f"(pendiente pasó de {m_ant:+.2f} a {m_act:+.2f})."
                ),
            })

    return cambios


def detectar_saltos_tiempo(datos, umbral_salto=1.0):
    """
    Detecta saltos irregulares en el eje X (por ejemplo, pasar del año 1 al año 5).
    """
    x = np.asarray(datos["x"], dtype=float)
    nombre_x = datos.get("nombre_x", "Período")
    saltos = []

    if len(x) < 2:
        return saltos

    orden = np.argsort(x)
    x_ord = x[orden]
    deltas_x = np.diff(x_ord)

    for i, dx in enumerate(deltas_x):
        if dx > umbral_salto:
            saltos.append({
                "x_origen": float(x_ord[i]),
                "x_destino": float(x_ord[i + 1]),
                "salto": float(dx),
                "mensaje": (
                    f"Salto en {nombre_x}: de {x_ord[i]:g} a {x_ord[i + 1]:g} "
                    f"(separación de {dx:g} unidades en el eje horizontal)."
                ),
            })

    return saltos
