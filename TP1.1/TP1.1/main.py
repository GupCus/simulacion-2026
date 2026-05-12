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


def ruleta_casino(cant_tiradas, cant_corridas, nro_apostado):
    for i in range(cant_corridas):
        random_values = [random.randint(0, 36) for _ in range(cant_tiradas)]

        print("Apostaste al: ", nro_apostado)
        print(random_values)
        plt.figure(figsize=(10, 6))
        plt.plot(random_values, label='Valores Aleatorios', color='blue')
        plt.xlabel('Número de tirada')
        plt.ylabel('Valor obtenido')
        plt.title('Gráfico de Valores Aleatorios con Valor Constante Intermitente')
        plt.legend()
        plt.grid(True)
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

    except ValueError,IndexError:
        print("No se puede ejecutar el programa. Uso correcto: python main.py -c XXX -n YYY -e ZZ")
        return



# Esta es una buena práctica en Python 3 para indicar que main() solo debe ejecutarse si ejecutamos ESTE archivo directamente.
if __name__ == "__main__":
    main()