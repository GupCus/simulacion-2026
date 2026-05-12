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

#DUDAS: clase aparte para la ruleta? Ruleta.py, algo así, en caso de que se complique
import random
import matplotlib.pyplot as plt
import sys


def calcular_frecuencias(valores, cant_tiradas):
    frecuencia_absoluta = [valores.count(numero) for numero in range(37)]
    frecuencia_relativa = [frecuencia_absoluta[numero] / cant_tiradas for numero in range(37)]
    return frecuencia_absoluta, frecuencia_relativa

def ruleta_casino(cant_tiradas, cant_corridas, nro_apostado):
    for i in range(cant_corridas):
        random_values = [random.randint(0, 36) for _ in range(cant_tiradas)]

        frecuencia_absoluta, frecuencia_relativa = calcular_frecuencias(random_values, cant_tiradas)

        valor_teorico_esperado = cant_tiradas / 37  

        fig, axs = plt.subplots(1, 3, figsize=(18, 6))

        axs[0].bar(range(37), frecuencia_absoluta, color='blue')
        axs[0].set_title(f'Corrida {i+1}: Frecuencia Absoluta')
        axs[0].set_xlabel('Número')
        axs[0].set_ylabel('Frecuencia')

        axs[1].bar(range(37), frecuencia_relativa, color='red')
        axs[1].set_title(f'Corrida {i+1}: Frecuencia Relativa')
        axs[1].set_xlabel('Número')
        axs[1].set_ylabel('Frecuencia')

        axs[2].plot(random_values, color='blue', label='Valores aleatorios')
        axs[2].axhline(y=nro_apostado, color='red', linestyle='--', label=f'Apostado ({nro_apostado})')
        axs[2].set_title(f'Corrida {i+1}: Valores por tirada')
        axs[2].set_xlabel('Tirada')
        axs[2].set_ylabel('Valor')
        axs[2].legend()

        plt.tight_layout()
        plt.savefig(f'corrida_{i+1}.png')
        plt.show()

def main():
    try:
        cant_corridas = int(sys.argv[2])
        cant_tiradas = int(sys.argv[4])
        nro_apostado = int(sys.argv[6])

        if cant_tiradas >= 1 and cant_corridas >= 1 and 0 <= nro_apostado <= 36:
            ruleta_casino(cant_tiradas, cant_corridas, nro_apostado)
        else:
            print("Argumentos inválidos")
            return

    except (ValueError,IndexError):
        print("No se puede ejecutar el programa. Uso correcto: python main.py -c XXX -n YYY -e ZZ")
        return



# Esta es una buena práctica en Python 3 para indicar que main() solo debe ejecutarse si ejecutamos ESTE archivo directamente.
if __name__ == "__main__":
    main()


















