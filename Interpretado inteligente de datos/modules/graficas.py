import matplotlib.pyplot as plt
import numpy as np


def graficar_global(datos, resultado_global, anomalias, evaluacion=None):
    """
    Gráfica 1: Muestra las ganancias registradas, la recta lineal global
    y las posibles anomalías detectadas.
    """
    x = np.asarray(datos["x"], dtype=float)
    y = np.asarray(datos["y"], dtype=float)
    nombre_x = datos.get("nombre_x", "Período")
    nombre_y = datos.get("nombre_y", "Ganancia ($)")

    pendiente = resultado_global["pendiente"]
    intercepto = resultado_global["intercepción con eje y"]
    y_recta = pendiente * x + intercepto

    plt.figure(figsize=(9, 5))

    plt.plot(x, y, marker="o", linestyle="-", color="#1f77b4", label="Ganancias registradas")
    plt.plot(
        x,
        y_recta,
        linestyle="--",
        linewidth=2,
        color="#2ca02c",
        label=f"Tendencia global ({resultado_global['funcion']})",
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

    r2_mostrar = evaluacion["r2"] if evaluacion else resultado_global.get("r2", 0.0)
    tendencia = resultado_global.get("tendencia", "")

    plt.title(f"Balance Global de Ganancias — {tendencia} (R² = {r2_mostrar:.2f})")
    plt.xlabel(nombre_x)
    plt.ylabel(nombre_y)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.show()


def graficar_local(datos, resultados_locales, anomalias, cambios, ventana=4):
    """
    Gráfica 2: Muestra las ganancias, las rectas lineales de cada ventana local,
    los cambios de tendencia y las anomalías.
    """
    x = np.asarray(datos["x"], dtype=float)
    y = np.asarray(datos["y"], dtype=float)
    nombre_x = datos.get("nombre_x", "Período")
    nombre_y = datos.get("nombre_y", "Ganancia ($)")

    plt.figure(figsize=(9, 5))

    plt.plot(x, y, marker="o", linestyle="-", color="#1f77b4", label="Ganancias registradas")

    for idx, res in enumerate(resultados_locales):
        inicio = res.get("inicio", idx)
        fin = min(res.get("fin", idx + ventana - 1), len(x) - 1)

        if fin > inicio:
            x_seg = x[inicio : fin + 1]
            y_seg = res["pendiente"] * x_seg + res["intercepción con eje y"]
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

    plt.title("Análisis Local de Tendencias por Ventanas")
    plt.xlabel(nombre_x)
    plt.ylabel(nombre_y)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.show()