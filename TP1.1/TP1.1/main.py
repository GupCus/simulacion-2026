# Consignas del TP:
# El trabajo de investigación consiste en construir un programa en lenguaje Python 3.x que simule el funcionamiento del
# plato de una ruleta. Para esto se debe tener en cuenta los siguientes temas:
# • Generación de valores aleatorios enteros.
# • Uso de listas para el almacenamiento de datos.
# • Uso de la estructura de control FOR para iterar las listas.
# • Empleo de funciones estadísticas.
# • Gráficos de los resultados mediante el paquete Matplotlib.
# • Ingreso por consola de parámetros para la simulación (cantidad de tiradas, corridas y número elegido)
#   ejemplo: python main.py -c XXX -n YYY -e ZZ.

import random
import matplotlib.pyplot as plt
import sys


# ─────────────────────────────────────────────
# Simulación de una corrida
# ─────────────────────────────────────────────
def simular_corrida(cant_tiradas, nro_apostado):
    """
    Simula una corrida de cant_tiradas tiradas y devuelve las listas
    de estadísticos acumulados tirada a tirada.
    """
    frn = []   # frecuencia relativa acumulada del número apostado
    vpn = []   # valor promedio acumulado
    vvn = []   # varianza muestral acumulada
    vdn = []   # desvío estándar acumulado

    conteo_apostado = 0
    suma = 0
    suma_cuadrados = 0

    for j in range(cant_tiradas):
        valor = random.randint(0, 36)
        n = j + 1

        if valor == nro_apostado:
            conteo_apostado += 1
        suma += valor
        suma_cuadrados += valor ** 2

        promedio = suma / n
        frn.append(conteo_apostado / n)
        vpn.append(promedio)

        if n > 1:
            varianza = (suma_cuadrados - n * promedio ** 2) / (n - 1)
            vvn.append(varianza)
            vdn.append(varianza ** 0.5)
        else:
            vvn.append(0)
            vdn.append(0)

    return frn, vpn, vvn, vdn


# ─────────────────────────────────────────────
# Graficación
# ─────────────────────────────────────────────
def graficar(titulo, eje_x, historiales, etiquetas, valores_esperados, labels_esperados):
    """
    Genera una figura 2x2 con los 4 estadísticos.
    historiales  : [hist_frecuencias, hist_promedios, hist_varianzas, hist_desvios]
    etiquetas    : títulos de cada subplot
    valores_esp  : línea roja de referencia para cada subplot
    labels_esp   : etiqueta de la línea roja
    """
    fig, axs = plt.subplots(2, 2, figsize=(14, 8))
    fig.suptitle(titulo, fontsize=14, fontweight='bold')

    posiciones = [(0, 0), (0, 1), (1, 0), (1, 1)]
    ylabels = ['Frecuencia Relativa', 'Promedio', 'Varianza', 'Desvío Estándar']

    for idx, (fila, col) in enumerate(posiciones):
        ax = axs[fila][col]
        for corrida in historiales[idx]:
            ax.plot(eje_x, corrida, linewidth=0.8, alpha=0.6)
        ax.axhline(
            y=valores_esperados[idx],
            color='red',
            linestyle='--',
            linewidth=1.5,
            label=labels_esperados[idx]
        )
        ax.set_title(etiquetas[idx])
        ax.set_xlabel('Número de tiradas (n)')
        ax.set_ylabel(ylabels[idx])
        ax.legend(fontsize=8)

    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────
# Función principal de simulación
# ─────────────────────────────────────────────
def ruleta_casino(cant_corridas, cant_tiradas, nro_apostado):
    # Valores teóricos esperados (distribución uniforme discreta sobre {0,...,36})
    fresperada      = 1 / 37                          # ≈ 0.02703
    promesperado    = 36 / 2                          # = 18
    varianzaesperada = ((36 - 0 + 1) ** 2 - 1) / 12  # = 114
    desvioesperado  = varianzaesperada ** 0.5         # ≈ 10.677

    etiquetas = [
        f'Frecuencia Relativa del número {nro_apostado}',
        'Valor Promedio de las tiradas',
        'Varianza de las tiradas',
        'Desvío Estándar de las tiradas'
    ]
    valores_esp = [fresperada, promesperado, varianzaesperada, desvioesperado]
    labels_esp  = [
        f'Frec. esperada = {fresperada:.5f}',
        f'Promedio esperado = {promesperado}',
        f'Varianza esperada = {varianzaesperada}',
        f'Desvío esperado = {desvioesperado:.4f}'
    ]

    eje_x = list(range(1, cant_tiradas + 1))

    # ── FIGURA 1: una sola corrida ─────────────────────────────────────────
    # Muestra cómo convergen los estadísticos en un único experimento
    frn1, vpn1, vvn1, vdn1 = simular_corrida(cant_tiradas, nro_apostado)

    graficar(
        titulo=f'Figura 1 — Una corrida ({cant_tiradas} tiradas, número apostado: {nro_apostado})',
        eje_x=eje_x,
        historiales=[[frn1], [vpn1], [vvn1], [vdn1]],
        etiquetas=etiquetas,
        valores_esperados=valores_esp,
        labels_esperados=labels_esp
    )

    # ── FIGURA 2: múltiples corridas simultáneas ───────────────────────────
    # Muestra la variabilidad entre corridas y la convergencia al TCL
    hist_frecuencias = []
    hist_promedios   = []
    hist_varianzas   = []
    hist_desvios     = []

    for _ in range(cant_corridas):
        frn, vpn, vvn, vdn = simular_corrida(cant_tiradas, nro_apostado)
        hist_frecuencias.append(frn)
        hist_promedios.append(vpn)
        hist_varianzas.append(vvn)
        hist_desvios.append(vdn)

    graficar(
        titulo=f'Figura 2 — {cant_corridas} corridas simultáneas ({cant_tiradas} tiradas, número apostado: {nro_apostado})',
        eje_x=eje_x,
        historiales=[hist_frecuencias, hist_promedios, hist_varianzas, hist_desvios],
        etiquetas=etiquetas,
        valores_esperados=valores_esp,
        labels_esperados=labels_esp
    )


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────
def main():
    try:
        cant_corridas = int(sys.argv[2])
        cant_tiradas  = int(sys.argv[4])
        nro_apostado  = int(sys.argv[6])

        if cant_tiradas >= 1 and cant_corridas >= 1 and 0 <= nro_apostado <= 36:
            ruleta_casino(cant_corridas, cant_tiradas, nro_apostado)
        else:
            print("Argumentos inválidos. Rangos: corridas>=1, tiradas>=1, número entre 0 y 36.")

    except (ValueError, IndexError):
        print("Uso correcto: python main.py -c <corridas> -n <tiradas> -e <número>")
        print("Ejemplo:      python main.py -c 5 -n 1000 -e 17")


if __name__ == "__main__":
    main()