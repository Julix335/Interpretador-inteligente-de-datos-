def modelo_lineal(x, y):

    n = len(x)
    
    suma_x = sum(x)
    suma_y = sum(y)

    suma_xy = 0 
    suma_x2 = 0 

    for i in range(len(x)):
        suma_xy += x[i] * y[i]
        suma_x2 += x[i] ** 2

    pendiente = (n * suma_xy - suma_x * suma_y) / (n * suma_x2 - (suma_x**2))

    intercepcion = (suma_y - pendiente * suma_x) / n 

    y_estimados = []
    for valor_x in x:
        estimado = (pendiente * valor_x) + intercepcion 
        y_estimados.append(estimado)

    resultado ={
        "modelo" : "Lineal",
        "pendiente" : pendiente,
        "intercepcion" : intercepcion,
        "coeficientes" : [pendiente, intercepcion],
        "r2" : None,
        "tendencia" : None,
        "irregularidades_x" : None
    }
    return resultado, y_estimados

def calcular_r2(y, y_estimados):

    media_y = sum(y) / len(y)
    ss_tot = 0 
    ss_res = 0 

    for i in range(len(y)):
        ss_tot += (y[i] - media_y)**2
        ss_res += (y[i] - y_estimados[i])**2

    if ss_tot == 0:
        return 1

    r2 = 1 - (ss_res/ss_tot)

    return r2

def clacificar_tendencia(m, y, r2):
        
    rango_y = (max(y) - min(y))
    tolerancia = rango_y * 0.05

    if r2 < 0.5:
        return "Sin tendencia clara"

    if m > tolerancia:
        return "Crecimiento"

    elif m < -tolerancia:
        return "Decrecimiento"

    else:
        return "Estabilidad"

def deteccion_irregularidades_x(x):

    dx = []

    for i in range(len(x) - 1):
        dx.append(x[i+1] - x[i])

    if len(dx) == 0:
        return []

    promedio_dx = sum(dx) / len(dx)

    irregularidades = []

    for indice, intervalo in enumerate(dx):
        if intervalo > promedio_dx * 2:
            irregularidad = {
                "inicio_irregularidad" : x[indice],
                "final_irregularidad" : x[indice + 1],
                "brecha" : intervalo
            }
            irregularidades.append(irregularidad)

    return irregularidades 

def analisis_global(datos):

    x = datos["x"]
    y = datos["y"]

    resultados, y_estimados = modelo_lineal(x, y)

    r2 = calcular_r2(y, y_estimados)

    tendencia = clacificar_tendencia(resultados["pendiente"], y, r2)

    irregularidades = deteccion_irregularidades_x(x)

    resultados["r2"] = r2
    resultados["tendencia"] = tendencia
    resultados["irregularidades_x"] = irregularidades

    return resultados

def analisis_local(datos, ventana = 4):

    x = datos["x"]
    y = datos["y"]

    if len(x) < ventana:
        raise ValueError(
            "No hay suficientes datos para realizar el analisis local"
        )

    resultados = []

    for i in range(len(x) - ventana + 1):
        datos_locales ={
            "x" : x[i:i + ventana],
            "y" : y[i:i + ventana]
        }

        resultado = {
            "ventana" : i + 1,
            "inicio" : x[i],
            "final" : x[i + ventana - 1],
            "datos analizados" : datos_locales
        }

        analisis = analisis_global(datos_locales)

        resultado.update(analisis)

        resultados.append(resultado)

    return resultados
