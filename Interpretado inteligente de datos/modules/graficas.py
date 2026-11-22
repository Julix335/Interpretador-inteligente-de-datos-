import matplotlib.pyplot as plt
import numpy as np

from modules.deteccion import (
    detectar_anomalias,
    detectar_cambios_tendencia,
    detectar_saltos_tiempo,
    evaluar_modelo_global,
)


def graficar_global(datos, resultado_global, anomalias=None, evaluacion=None):
    """
    Gráfica 1: Muestra las ganancias registradas, la recta lineal global
    y las posibles anomalías.
    """
    if evaluacion is None:
        evaluacion = evaluar_modelo_global(datos, resultado_global)

    if anomalias is None:
        anomalias = detectar_anomalias(datos, resultado_global)

    saltos = detectar_saltos_tiempo(datos)

    x = np.asarray(datos["x"], dtype=float)
    y = np.asarray(datos["y"], dtype=float)

    orden = np.argsort(x)
    x = x[orden]
    y = y[orden]

    nombre_x = datos.get("nombre_x", "Período")
    nombre_y = datos.get("nombre_y", "Ganancia ($)")

    pendiente = resultado_global["pendiente"]
    intercepto = resultado_global["intercepcion"]
    y_recta = pendiente * x + intercepto

    signo = "+" if intercepto >= 0 else "-"
    ecuacion = f"y = {pendiente:.2f}x {signo} {abs(intercepto):.2f}"

    plt.figure(figsize=(9, 5))

    plt.plot(x, y, marker="o", linestyle="-", color="#1f77b4", label="Ganancias registradas")
    plt.plot(
        x,
        y_recta,
        linestyle="--",
        linewidth=2,
        color="#2ca02c",
        label=f"Tendencia global ({ecuacion})",
    )

    if anomalias:
        x_anom = [a["x"] for a in anomalias]
        y_anom = [a["y"] for a in anomalias]
        plt.scatter(
            x_anom,
            y_anom,
            color="#d62728",
            s=120,
            zorder=5,
            label="Anomalías detectadas",
        )

    r2_mostrar = resultado_global.get("r2")
    if r2_mostrar is None:
        r2_mostrar = evaluacion["r2"]

    tendencia = resultado_global.get("tendencia", "")
    aviso_salto = " | Con saltos de tiempo" if saltos else ""

    plt.title(f"Balance Global de Ganancias — {tendencia} (R² = {r2_mostrar:.2f}){aviso_salto}")
    plt.xlabel(nombre_x)
    plt.ylabel(nombre_y)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.show(block=False)


def graficar_local(
    datos, resultados_locales, anomalias=None, cambios=None, resultado_global=None, ventana=4
):
    """
    Gráfica 2: Muestra las ganancias, las rectas lineales de cada ventana local,
    los cambios de tendencia y las anomalías.
    """
    if anomalias is None and resultado_global is not None:
        anomalias = detectar_anomalias(datos, resultado_global)
    elif anomalias is None:
        anomalias = []

    if cambios is None:
        cambios = detectar_cambios_tendencia(resultados_locales, datos, ventana=ventana)

    saltos = detectar_saltos_tiempo(datos)

    x = np.asarray(datos["x"], dtype=float)
    y = np.asarray(datos["y"], dtype=float)

    orden = np.argsort(x)
    x = x[orden]
    y = y[orden]

    nombre_x = datos.get("nombre_x", "Período")
    nombre_y = datos.get("nombre_y", "Ganancia ($)")

    plt.figure(figsize=(9, 5))

    plt.plot(x, y, marker="o", linestyle="-", color="#1f77b4", label="Ganancias registradas")

    for idx, res in enumerate(resultados_locales):
        if "datos analizados" in res:
            x_seg = np.asarray(res["datos analizados"]["x"], dtype=float)
        else:
            inicio = idx
            fin = min(idx + ventana - 1, len(x) - 1)
            x_seg = x[inicio : fin + 1]

        if len(x_seg) >= 2:
            y_seg = res["pendiente"] * x_seg + res["intercepcion"]
            plt.plot(
                x_seg,
                y_seg,
                linestyle="--",
                linewidth=2,
                alpha=0.85,
                label=f"Ventana {idx + 1} ({res.get('tendencia', '')})",
            )

    if cambios:
        x_camb = [c["x_referencia"] for c in cambios]
        y_camb = [y[c["indice_fin"]] for c in cambios]
        plt.scatter(
            x_camb,
            y_camb,
            marker="^",
            color="#9467bd",
            s=130,
            zorder=5,
            label="Cambio de tendencia",
        )

    if anomalias:
        x_anom = [a["x"] for a in anomalias]
        y_anom = [a["y"] for a in anomalias]
        plt.scatter(
            x_anom,
            y_anom,
            color="#d62728",
            s=120,
            zorder=6,
            label="Anomalías detectadas",
        )

    aviso_salto = " (con saltos de tiempo)" if saltos else ""
    plt.title(f"Análisis Local de Tendencias por Ventanas{aviso_salto}")
    plt.xlabel(nombre_x)
    plt.ylabel(nombre_y)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.show()
