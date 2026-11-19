datos = {
    "x" : [1, 2, 3, 4, 5, 6, 7, 8],
    "y" : [100, 120, 140, 160, 90, 70, 75, 80]
}

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
        "intercepción con eje y" : intercepcion,
        "coeficientes" : [pendiente, intercepcion],
        "funcion" : f"y = {pendiente:.2f}x + {intercepcion:.2f}",
        "r2" : None,
        "tendencia" : None
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

    elif m < tolerancia:
        return "Decrecimiento"

    else:
        return "Estabilidad"

def analisis_global(datos):

    x = datos["x"]
    y = datos["y"]

    resultados, y_estimados = modelo_lineal(x, y)

    r2 = calcular_r2(y, y_estimados)

    tendencia = clacificar_tendencia(resultados["pendiente"], y, r2)

    resultados["r2"] = r2
    resultados["tendencia"] = tendencia

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
        x_local = x[i:i + ventana]
        y_local = y[i:i + ventana]

        resultado, y_estimado = modelo_lineal(x_local, y_local)

        r2 = calcular_r2(y_local, y_estimado)

        tendencia = clacificar_tendencia(resultado["pendiente"], y_local, r2)

        resultado["r2"] = r2
        resultado["tendencia"] = tendencia
        resultados.append(resultado)

    return resultados

b = analisis_local(datos)
print(b)