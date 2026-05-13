# Consignas del TP:
# El trabajo de investigación consiste en construir un programa en lenguaje Python 3.x que simule el funcionamiento del
# plato de una ruleta. Para esto se debe tener en cuenta los siguientes temas:
# • Generación de valores aleatorios enteros.
# • Uso de listas para el almacenamiento de datos.
# • Uso de la estructura de control FOR para iterar las listas.
# • Empleo de funciones estadísticas.
# • Gráficos de los resultados mediante el paquete Matplotlib.
# • Ingreso por consola de parámetros para la simulación (cantidad de tiradas, corridas y número elegido)
#   ejemplo: python programa.py -c XXX -n YYY -e ZZ.

import random
import statistics
import matplotlib.pyplot as plt
import sys



def calcular_frecuencias(valores, cant_tiradas):
    frecuencia_absoluta = [valores.count(numero) for numero in range(37)]
    frecuencia_relativa = [frecuencia_absoluta[numero] / cant_tiradas for numero in range(37)]
    return frecuencia_absoluta, frecuencia_relativa

def ruleta_casino(cant_corridas, cant_tiradas, nro_apostado):
    #Valores esperados:
    fresperada = 1/37 #0,02702 o 2,7%
    promesperado = 36/2 #18
    varianzaesperada = (((36-0+1)**2) - 1 ) / 12 # 114 | Varianza de una distrib. uniforme discreta (max-min + 1) elevado a 2 sobre 12
    desvioesperado = varianzaesperada ** 0.5 # ~10,667 | raíz cuadrada de la varianza

    # Acumulador de resultados:
    historial_frecuencias = []
    historial_promedios = []
    historial_varianzas = []
    historial_desvios = []

    for i in range(cant_corridas):
        valores_tiradas = [random.randint(0, 36) for _ in range(cant_tiradas)]

        frn = []
        vpn = []
        vvn = []
        vdn = []

        conteo_apostado = 0
        suma = 0
        suma_cuadrados = 0

        for j in range(cant_tiradas):
            valor = valores_tiradas[j]
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

        historial_frecuencias.append(frn)
        historial_promedios.append(vpn)
        historial_varianzas.append(vvn)
        historial_desvios.append(vdn)

    eje_x = list(range(1, cant_tiradas + 1))

    #Gráficas de convergencia por número de tiradas
    fig, axs = plt.subplots(2, 2, figsize=(18, 6))

    for frn in historial_frecuencias:
        axs[0][0].plot(eje_x, frn, linewidth=0.8, alpha=0.7)
    axs[0][0].axhline(y=fresperada, color='red', linestyle='--', label=f'Frecuencia esperada ({fresperada})')
    axs[0][0].set_title('Frecuencia Relativa')
    axs[0][0].set_xlabel('Número de tiradas')
    axs[0][0].set_ylabel('Frecuencia Relativa')
    axs[0][0].legend()

    for vpn in historial_promedios:
        axs[0][1].plot(eje_x, vpn, linewidth=0.8, alpha=0.7)
    axs[0][1].axhline(y=promesperado, color='red', linestyle='--', label=f'Promedio esperado ({promesperado})')
    axs[0][1].set_title('Promedio')
    axs[0][1].set_xlabel('Número de tiradas')
    axs[0][1].set_ylabel('Promedio')
    axs[0][1].legend()

    for vvn in historial_varianzas:
        axs[1][0].plot(eje_x, vvn, linewidth=0.8, alpha=0.7)
    axs[1][0].axhline(y=varianzaesperada, color='red', linestyle='--', label=f'Varianza esperada ({varianzaesperada})')
    axs[1][0].set_title('Varianza')
    axs[1][0].set_xlabel('Número de tiradas')
    axs[1][0].set_ylabel('Varianza')
    axs[1][0].legend()

    for vdn in historial_desvios:
        axs[1][1].plot(eje_x, vdn, linewidth=0.8, alpha=0.7)
    axs[1][1].axhline(y=desvioesperado, color='red', linestyle='--', label=f'Varianza esperada ({desvioesperado})')
    axs[1][1].set_title('Desvío')
    axs[1][1].set_xlabel('Número de tiradas')
    axs[1][1].set_ylabel('Desvío')
    axs[1][1].legend()

    plt.tight_layout()
    plt.show()


def main():
    try:
        cant_corridas = int(sys.argv[2])
        cant_tiradas = int(sys.argv[4])
        nro_apostado = int(sys.argv[6])

        if cant_tiradas >= 1 and cant_corridas >= 1 and 0 <= nro_apostado <= 36:
            ruleta_casino(cant_corridas,cant_tiradas, nro_apostado)
        else:
            print("Argumentos inválidos")
            return

    except (ValueError,IndexError):
        print("No se puede ejecutar el programa. Uso correcto: python main.py -c XXX -n YYY -e ZZ")
        return



# Esta es una buena práctica en Python 3 para indicar que main() solo debe ejecutarse si ejecutamos ESTE archivo directamente.
if __name__ == "__main__":
    main()


















