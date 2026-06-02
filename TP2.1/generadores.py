### generadores pseudoaleatorios
import math
import json
import sys

def gcl(m, a, c, x0, n):
    """
    Genera n números pseudoaleatorios en [0, 1).
    Fórmula: X(n+1) = (a * X(n) + c) mod m   →   U = X / m
    Retorna None si los parámetros son inválidos.
    """

    # ── Validación ────────────────────────────────────────────────────────────

    if m < 2:
        print("Error: m debe ser >= 2"); return None
    if not (1 <= a <= m - 1):
        print(f"Error: a debe estar en [1, {m-1}]"); return None
    if not (0 <= c <= m - 1):
        print(f"Error: c debe estar en [0, {m-1}]"); return None
    if not (0 <= x0 <= m - 1):
        print(f"Error: x0 debe estar en [0, {m-1}]"); return None

    # Hull-Dobell 1: c y m deben ser coprimos
    if math.gcd(c, m) != 1:
        print(f"Hull-Dobell 1 fallida: mcd(c={c}, m={m}) = {math.gcd(c,m)} ≠ 1"); return None

    # Hull-Dobell 2: cada primo que divide a m debe dividir a (a-1)
    n_temp = m
    d = 2
    while d * d <= n_temp:
        if n_temp % d == 0:
            if (a - 1) % d != 0:
                print(f"Hull-Dobell 2 fallida: (a-1)={a-1} no es divisible por {d}"); return None
            while n_temp % d == 0:
                n_temp //= d
        d += 1
    if n_temp > 1 and (a - 1) % n_temp != 0:
        print(f"Hull-Dobell 2 fallida: (a-1)={a-1} no es divisible por {n_temp}"); return None

    # Hull-Dobell 3: si 4 | m, entonces 4 | (a-1)
    if m % 4 == 0 and (a - 1) % 4 != 0:
        print(f"Hull-Dobell 3 fallida: 4 | m={m} pero 4 no divide a (a-1)={a-1}"); return None

    # ── Generación ────────────────────────────────────────────────────────────

    secuencia = []
    x = x0
    for _ in range(n):
        x = (a * x + c) % m
        secuencia.append(x / m)
    return secuencia


# ── Tests de calidad ──────────────────────────────────────────────────────────
# Todas las funciones reciben una secuencia de números en [0, 1)


def test_uniformidad(secuencia, intervalos=10):
    """
    Test de uniformidad Chi-cuadrado.
    Divide [0,1) en k intervalos y compara la frecuencia observada vs esperada.
    """
    n = len(secuencia)
    esperado = n / intervalos
    observado = [0] * intervalos

    for u in secuencia:
        indice = min(int(u * intervalos), intervalos - 1)
        observado[indice] += 1

    chi2 = sum((o - esperado) ** 2 / esperado for o in observado)

    print(f"=== Test de Uniformidad (Chi-cuadrado) ===")
    print(f"  Intervalos:        {intervalos}")
    print(f"  Frecuencia esperada por intervalo: {esperado:.2f}")
    print(f"  Frecuencia observada: {observado}")
    print(f"  Chi-cuadrado:      {chi2:.4f}")
    print(f"  Grados de libertad: {intervalos - 1}")
    return chi2


def test_frecuencia(secuencia, intervalos=10):
    """
    Test de frecuencia.
    Verifica que cada subintervalo de [0,1) sea visitado una cantidad similar de veces.
    """
    n = len(secuencia)
    esperado = n / intervalos
    conteo = [0] * intervalos

    for u in secuencia:
        indice = min(int(u * intervalos), intervalos - 1)
        conteo[indice] += 1

    desviaciones = [abs(c - esperado) for c in conteo]
    desviacion_max = max(desviaciones)
    desviacion_prom = sum(desviaciones) / intervalos

    print(f"=== Test de Frecuencia ===")
    print(f"  Intervalos:           {intervalos}")
    print(f"  Esperado por intervalo: {esperado:.2f}")
    for i, c in enumerate(conteo):
        print(f"  [{i/intervalos:.1f}, {(i+1)/intervalos:.1f}): {c} (desvío: {abs(c - esperado):.2f})")
    print(f"  Desvío máximo:        {desviacion_max:.4f}")
    print(f"  Desvío promedio:      {desviacion_prom:.4f}")
    return desviacion_max, desviacion_prom


def test_series(secuencia, intervalos=5):
    """
    Test de series.
    Analiza pares consecutivos (U_i, U_{i+1}) y verifica que se distribuyan
    uniformemente en la grilla intervalos x intervalos de [0,1)^2.
    """
    n = len(secuencia)
    esperado = (n - 1) / (intervalos ** 2)
    conteo = [[0] * intervalos for _ in range(intervalos)]

    for i in range(n - 1):
        fila = min(int(secuencia[i]     * intervalos), intervalos - 1)
        col  = min(int(secuencia[i + 1] * intervalos), intervalos - 1)
        conteo[fila][col] += 1

    chi2 = sum(
        (conteo[f][c] - esperado) ** 2 / esperado
        for f in range(intervalos)
        for c in range(intervalos)
    )

    print(f"=== Test de Series ===")
    print(f"  Grilla:             {intervalos}x{intervalos}")
    print(f"  Pares analizados:   {n - 1}")
    print(f"  Esperado por celda: {esperado:.2f}")
    print(f"  Chi-cuadrado:       {chi2:.4f}")
    print(f"  Grados de libertad: {intervalos ** 2 - 1}")
    return chi2


def test_corridas(secuencia):
    """
    Test de corridas.
    Una corrida es una subsecuencia consecutiva de valores todos crecientes o todos decrecientes.
    Compara la cantidad de corridas observadas vs la esperada para una secuencia aleatoria.
    """
    n = len(secuencia)

    # Contar corridas
    corridas = 1
    for i in range(1, n):
        if secuencia[i] != secuencia[i - 1]:
            if (secuencia[i] > secuencia[i - 1]) != (secuencia[i - 1] > secuencia[i - 2] if i > 1 else True):
                corridas += 1

    # Media y varianza esperadas para secuencia aleatoria
    media_esperada  = (2 * n - 1) / 3
    varianza_esperada = (16 * n - 29) / 90

    z = (corridas - media_esperada) / math.sqrt(varianza_esperada)

    print(f"=== Test de Corridas ===")
    print(f"  N:                  {n}")
    print(f"  Corridas observadas: {corridas}")
    print(f"  Media esperada:     {media_esperada:.4f}")
    print(f"  Varianza esperada:  {varianza_esperada:.4f}")
    print(f"  Z:                  {z:.4f}  (si |Z| < 1.96 → no se rechaza aleatoriedad al 95%)")
    return z


def python_random(n):
    import random
    return [random.random() for _ in range(n)]


GENERADORES = {
    "gcl": lambda n: gcl(m=2**32, a=1664525, c=1013904223, x0=42, n=n),
    "python_random": python_random,
}


def guardar_resultados(nombre, resultados_dict):
    with open(f"resultados_{nombre}.json", "w") as f:
        json.dump(resultados_dict, f, indent=2)


def generar_graficas(secuencia, nombre):
    import matplotlib.pyplot as plt

    n = len(secuencia)
    intervalos = 10
    esperado = n / intervalos

    # Histograma
    fig, ax = plt.subplots()
    ax.hist(secuencia, bins=intervalos, range=(0, 1), edgecolor="black")
    ax.axhline(y=esperado, color="red", linestyle="--", label=f"esperado ({esperado:.1f})")
    ax.set_xlabel("Valor")
    ax.set_ylabel("Frecuencia")
    ax.set_title(f"Histograma — {nombre}")
    ax.legend()
    fig.savefig(f"{nombre}_histograma.png")
    plt.close(fig)

    # Scatter de pares consecutivos
    fig, ax = plt.subplots()
    ax.scatter(secuencia[:-1], secuencia[1:], s=2, alpha=0.5)
    ax.set_xlabel("U_i")
    ax.set_ylabel("U_{i+1}")
    ax.set_title(f"Scatter pares consecutivos — {nombre}")
    fig.savefig(f"{nombre}_scatter.png")
    plt.close(fig)


def ejecutar(nombre, n=1000):
    if nombre not in GENERADORES:
        print(f"Generador '{nombre}' no encontrado. Disponibles: {list(GENERADORES.keys())}")
        return

    secuencia = GENERADORES[nombre](n)

    chi2_unif          = test_uniformidad(secuencia, intervalos=10)
    desvio_max, desvio_prom = test_frecuencia(secuencia, intervalos=10)
    chi2_series        = test_series(secuencia, intervalos=5)
    z_corridas         = test_corridas(secuencia)

    guardar_resultados(nombre, {
        "generador": nombre,
        "n": n,
        "uniformidad_chi2": chi2_unif,
        "frecuencia_desviacion_max": desvio_max,
        "frecuencia_desviacion_prom": desvio_prom,
        "series_chi2": chi2_series,
        "corridas_z": z_corridas,
    })

    generar_graficas(secuencia, nombre)

    print(f"Archivos guardados: resultados_{nombre}.json, {nombre}_histograma.png, {nombre}_scatter.png")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) > 1:
        nombre = sys.argv[1]
    else:
        print(f"Generadores disponibles: {list(GENERADORES.keys())}")
        nombre = input("Escribí el nombre del generador: ").strip()

    ejecutar(nombre, n=1000)

# python_random(n): genera n floats en [0, 1) usando random.random() (Mersenne Twister) de la stdlib de Python.














