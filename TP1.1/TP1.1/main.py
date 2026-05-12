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

        #Acá calcula según la cant_tiradas
        valores_tiradas = [random.randint(0, 36) for _ in range(cant_tiradas)]
        frecuencia_absoluta, frecuencia_relativa = calcular_frecuencias(valores_tiradas, cant_tiradas)
        promedio = sum(valores_tiradas) / len(valores_tiradas)
        varianza = statistics.variance(valores_tiradas)
        desvio_estandar = varianza ** 0.5

        #Sumo a los historiales los resultados
        historial_frecuencias.append(frecuencia_relativa[nro_apostado])
        historial_promedios.append(promedio)
        historial_varianzas.append(varianza)
        historial_desvios.append(desvio_estandar)

        '''
        #Acá grafica cant_corridas de veces, por eso ejecuta las ventanas por cada corrida, queda comentado ver si podemos hacer algo interesante
        #Gráficos generales, distribución de los números.
        fig, axs = plt.subplots(1, 3, figsize=(18, 6))
        axs[0].bar(range(37), frecuencia_absoluta, color='blue')
        axs[0].set_title(f'Corrida {i+1}: Frecuencia Absoluta')
        axs[0].set_xlabel('Número')
        axs[0].set_ylabel('Frecuencia')

        axs[1].bar(range(37), frecuencia_relativa, color='red')
        axs[1].set_title(f'Corrida {i+1}: Frecuencia Relativa')
        axs[1].set_xlabel('Número')
        axs[1].set_ylabel('Frecuencia')

        axs[2].plot(valores_tiradas, color='blue', label='Valores aleatorios')
        axs[2].axhline(y=promedio, color='red', linestyle='--', label=f'Promedio de las tiradas ({promedio})')
        axs[2].set_title(f'Corrida {i+1}: Valores por tirada')
        axs[2].set_xlabel('Tirada')
        axs[2].set_ylabel('Valor')
        axs[2].legend()


        plt.tight_layout()
        #plt.savefig(f'corrida_{i+1}.png') #Desmarcar esto provoca que se guarden las corridas como imágenes.
        plt.show()
        '''
    #Gráficas de los históricos por corrida
    fig, axs = plt.subplots(2, 2, figsize=(18, 6))
    axs[0][0].plot(historial_frecuencias, color='blue', label='Frecuencia Relativa')
    axs[0][0].axhline(y=fresperada, color='red', linestyle='--', label=f'Frecuencia esperada ({fresperada})')
    axs[0][0].set_title('Frecuencia Relativa')
    axs[0][0].set_xlabel('Corrida')
    axs[0][0].set_ylabel('Frecuencia Relativa')
    axs[0][0].legend()
    axs[0][1].plot(historial_promedios, color='blue', label='Promedio')
    axs[0][1].axhline(y=promesperado, color='red', linestyle='--', label=f'Promedio esperado ({promesperado})')
    axs[0][1].set_title('Promedio')
    axs[0][1].set_xlabel('Corrida')
    axs[0][1].set_ylabel('Promedio')
    axs[0][1].legend()
    axs[1][0].plot(historial_varianzas, color='blue', label='Varianza')
    axs[1][0].axhline(y=varianzaesperada, color='red', linestyle='--', label=f'Varianza esperada ({varianzaesperada})')
    axs[1][0].set_title('Varianza')
    axs[1][0].set_xlabel('Corrida')
    axs[1][0].set_ylabel('Varianza')
    axs[1][0].legend()
    axs[1][1].plot(historial_desvios,color = 'blue', label = 'Desvío')
    axs[1][1].axhline(y=desvioesperado, color='red', linestyle='--', label=f'Varianza esperada ({desvioesperado})')
    axs[1][1].set_title('Desvío')
    axs[1][1].set_xlabel('Corrida')
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


















