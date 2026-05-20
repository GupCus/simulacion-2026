# Consignas del TP:
# • Beneficios de las apuestas según la selección (color, fila, número único, etc.).
# • Distintos tipos de estrategias de apuestas en la ruleta.
# • Gráficas de los resultados mediante el paquete Matplotlib (u otro similar).
# Se pide que se detalle las estrategias empleadas y las fuentes donde las obtuvieron (si no son de elaboración propia).
# Se proponen analizar 3 estrategias: la martingala, D’Alembert y Fibonacci,
# Por lo tanto, la ejecución junto con el TP 1.1: python programa.py -c XXX -n YYY -e ZZ -s -a
# Nota: El parámetro -e es solo en caso de usar un solo número para la estrategia seleccionada, si no no es necesario.

import random
import matplotlib.pyplot as plt
import sys


# ─────────────────────────────────────────────
# Tipos de apuesta (simplificado)
# ─────────────────────────────────────────────

rojo = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]

negro = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

primera_columna = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]

segunda_columna = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]

tercera_columna = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]

# ---------------------------------------------
# Crupier (indica si ganaste o no, actualiza la caja según la apuesta)
# ---------------------------------------------

def crupier(apuesta,valor,caja,cant_a_apostar):
    match apuesta:
        case "rojo" if valor in rojo:
            gane = True
            caja += cant_a_apostar
        case "negro" if valor in negro:
            gane = True
            caja += cant_a_apostar
        case "par" if valor % 2 == 0 and valor != 0:
            gane = True
            caja += cant_a_apostar
        case "impar" if valor % 2 != 0 and valor != 0:
            gane = True
            caja += cant_a_apostar
        case "c1" if valor in primera_columna:
            gane = True
            caja += cant_a_apostar * 2
        case "c2" if valor in segunda_columna:
            gane = True
            caja += cant_a_apostar * 2
        case "c3" if valor in tercera_columna:
            gane = True
            caja += cant_a_apostar * 2
        case _ if valor == apuesta:
            gane = True
            caja += cant_a_apostar * 35
        case _ :
            gane = False
            caja -= cant_a_apostar
    return gane, caja


# ─────────────────────────────────────────────
# Simulación de una corrida
# ─────────────────────────────────────────────
# noinspection PyTypeChecker
def simular_corrida(cant_tiradas, apuesta, estrategia,tipo_capital) -> tuple:
    caja=100000
    capital_inicial=caja
    cantidad_apostada_inicial=1000
    cant_a_apostar=cantidad_apostada_inicial
    valores_caja=[]
    valores_frecuencia_acumulada=[]
    gane=0
    bancarrota = False

    for j in range(cant_tiradas):
        # noinspection PyUnresolvedReferences
        if tipo_capital=='f' and (cant_a_apostar > caja):
            bancarrota = True
            break

        valor = random.randint(0, 36)

        resultado,caja=crupier(apuesta,valor,caja,cant_a_apostar)

        #LAS ESTRATEGIAS SOLO DEBERÍAN MODIFICAR LA PROXIMA APUESTA
        match estrategia:
            case "m":
                cant_a_apostar=martingala(cant_a_apostar,cantidad_apostada_inicial,resultado)
            case "d":
                cant_a_apostar= dalembert(cant_a_apostar, cantidad_apostada_inicial,resultado)
            case "f":
                cant_a_apostar=fibonacci(cant_a_apostar,cantidad_apostada_inicial,resultado)
            case "o":
                cant_a_apostar,cortar=goBigOrGoHome(caja, cant_a_apostar, capital_inicial, cantidad_apostada_inicial,resultado)
                if cortar: break
        
        if resultado: gane = gane + 1
        
        valores_caja.append(caja)
        valores_frecuencia_acumulada.append(gane/(j+1))  #j+1 porque j empieza en 0

    #esto se printable para debugger
    #print(cant_a_apostar)
    #print( valores_caja)
    #print(valores_frecuencia_acumulada[:30])
    return valores_caja,valores_frecuencia_acumulada,capital_inicial,bancarrota

def frecuencia_esperada(apuesta):
    if apuesta in ['rojo','negro','par','impar']:
        return 18/37
    elif apuesta in ['c1','c2','c3']:
        return 12/37
    else:
        return 1/37
# ─────────────────────────────────────────────
#   Graficación
# ─────────────────────────────────────────────
def graficar(valores_caja,valores_frecuencia_acumulada,capital_inicial,frecuencia):
  fig,(ax1,ax2)=plt.subplots(1,2,figsize=(12,5))
  eje_x=range(1,len(valores_frecuencia_acumulada)+1)
  ax1.bar(eje_x,valores_frecuencia_acumulada,color="red")
  ax1.set_xlabel('n (numero de tiradas)')
  ax1.set_ylabel('fr (frecuencia relativa)')
  ax1.set_title('Frecuencia relativa de obtener la apuesta favorable segun n')
  ax1.axhline(y=frecuencia, color='blue', linestyle='--', label=f'frec. esperada ({frecuencia:.4f})')
  ax1.legend()
  ax2.plot(eje_x,valores_caja,color="red",label="fc (Flujo de caja)")
  ax2.axhline(y=capital_inicial,color="blue",linestyle="--",label="fci (flujo de caja inicial)")
  ax2.set_xlabel("n (numero de tiradas)")
  ax2.set_ylabel("cc (cantidad de capital)")
  ax2.set_title("Flujo de caja")
  ax2.legend()
  plt.tight_layout()
  plt.show()

def graficar_multiples(valores_caja_corridas,  valores_frecuencia_acumulada_corridas, capital_inicial,frecuencia):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    for  valor_frecuencia_corrida in  valores_frecuencia_acumulada_corridas:
        eje_x = range(1, len(valor_frecuencia_corrida) + 1)
        ax1.plot(eje_x, valor_frecuencia_corrida, linewidth=0.8, alpha=0.6)

    ax1.axhline(y=frecuencia, color='blue', linestyle='--', label=f'frec. esperada ({frecuencia:.4f})')
    ax1.set_xlabel('n (numero de tiradas)')
    ax1.set_ylabel('fr (frecuencia relativa)')
    ax1.set_title('Frecuencia relativa - varias corridas')
    ax1.legend()

    for  valor_caja_corrida in valores_caja_corridas:
        eje_x = range(1, len(valor_caja_corrida) + 1)
        ax2.plot(eje_x, valor_caja_corrida, linewidth=0.8, alpha=0.6)

    ax2.axhline(y=capital_inicial, color='blue', linestyle='--', label='fci (capital inicial)')
    ax2.set_xlabel('n (numero de tiradas)')
    ax2.set_ylabel('cc (cantidad de capital)')
    ax2.set_title('Flujo de caja - varias corridas')
    ax2.legend()

    plt.tight_layout()
    plt.show()
# ─────────────────────────────────────────────
# Función principal de simulación
# ─────────────────────────────────────────────
def ruleta_casino(cant_corridas, cant_tiradas, nro_apostado, estrategia, tipo_capital):
    frecuencia=frecuencia_esperada(nro_apostado)
    #esto sería para una sola corrida (las dos primeras gráficas)
    valores_caja,valores_frecuencia_acumulada,capital_inicial,_=simular_corrida(cant_tiradas,nro_apostado,estrategia,tipo_capital)
    graficar(valores_caja,valores_frecuencia_acumulada,capital_inicial,frecuencia)

    valores_caja_corridas=[]
    valores_frecuencia_acumulada_corridas=[]
    bancarrotas = 0

    for i in range(cant_corridas):
        valor_caja_corrida,valor_freq_corrida,capital_inicial,hubo_bancarrota=simular_corrida(cant_tiradas,nro_apostado,estrategia,tipo_capital)
        if hubo_bancarrota:
            bancarrotas += 1
        valores_caja_corridas.append(valor_caja_corrida)
        valores_frecuencia_acumulada_corridas.append(valor_freq_corrida)
    graficar_multiples(valores_caja_corridas,  valores_frecuencia_acumulada_corridas, capital_inicial,frecuencia)

    if tipo_capital == 'f':
        print(f"\n--- Resumen de bancarrotas ---")
        print(f"Corridas simuladas: {cant_corridas}")
        print(f"Bancarrotas: {bancarrotas} ({bancarrotas/cant_corridas*100:.1f}%)")


    
# ─────────────────────────────────────────────
# Estrategias
# ─────────────────────────────────────────────

def martingala(cant_a_apostar,cant_apostada_inicial,resultado):

    if resultado:
       cant_a_apostar = cant_apostada_inicial
    else:
       cant_a_apostar = cant_a_apostar * 2
    return cant_a_apostar

def dalembert(cant_a_apostar, cant_apostada_inicial,resultado):

    if resultado:
        # Bajar 1 unidad, pero nunca por debajo de la unidad base
        cant_a_apostar = max(cant_apostada_inicial, cant_a_apostar - cant_apostada_inicial)
    else:
        cant_a_apostar = cant_a_apostar + cant_apostada_inicial

    return cant_a_apostar

def fibonacci(cant_a_apostar, cantidad_apostada_inicial,resultado):
    #No tengo forma de saber en qué posición de fibonacci estoy, tuve que descubrir el multiplicador de la apuesta incial así:
    multiplicador = cant_a_apostar / cantidad_apostada_inicial

    #Va a ir generando el valor de fibonacci hasta encontrar en el que estoy parado, no es lo más óptimo
    fibonacci_valores = [1, 1]
    while fibonacci_valores[-1] < multiplicador:
        siguiente_valor = fibonacci_valores[-1] + fibonacci_valores[-2]
        fibonacci_valores.append(siguiente_valor)

    #Si gano, retrocedo dos posiciones (-2) desde el valor que estoy parado (-1)
    #En caso de ganar la primera atajo con un 1
    #En caso de perder avanzo una posición en fibonacci
    if resultado:
        if len(fibonacci_valores) >= 3:
            multiplicadornvo = fibonacci_valores[-3]
        else:
            multiplicadornvo = 1
    else:
        multiplicadornvo = fibonacci_valores[-1] + fibonacci_valores[-2]

    #Finalmente, multiplico el valor de fibonacci por el valor inicial
    cant_a_apostar = cantidad_apostada_inicial * multiplicadornvo

    return cant_a_apostar

def goBigOrGoHome(caja, cant_a_apostar, capital_inicial, cantidad_apostada_inicial,resultado):
    if resultado:
        if caja >= capital_inicial * 2:
            return cant_a_apostar, True
        cant_a_apostar = cantidad_apostada_inicial
        return cant_a_apostar, False
    else:
        cant_a_apostar = cant_a_apostar * 1.2
        return cant_a_apostar, False

# ---------------------------------------------
# Main
# ---------------------------------------------
def main():
    try:
        cant_corridas = int(sys.argv[2])
        cant_tiradas  = int(sys.argv[4])
        try:
            apuesta = int(sys.argv[6])
        except ValueError:
            apuesta = sys.argv[6].lower()
        estrategia_utilizada = sys.argv[8]
        tipo_capital = sys.argv[10]
        if cant_tiradas >= 1 and cant_corridas >= 1 and ((isinstance(apuesta, int) and 0 <= apuesta <= 36) or apuesta in ["rojo","negro","par","impar","c1","c2","c3"]) and estrategia_utilizada in ['m','d','f','o'] and tipo_capital in ['i','f']:
            ruleta_casino(cant_corridas, cant_tiradas, apuesta, estrategia_utilizada, tipo_capital)
        else:
            print("Argumentos inválidos. Rangos: corridas>=1, tiradas>=1, número entre 0 y 36, estrategia tiene que estar entre ['m','d','f','o'] y tipo de capital tiene que estar entre ['i','f'] .")

    except (ValueError, IndexError):
        print("Uso correcto: python main.py -c <corridas> -n <tiradas> -e <número> -s <estrategia> -a <capital>")
        print("Ejemplo:      python main.py -c 5 -n 1000 -e 17 -s f -a f")


if __name__ == "__main__":
    main()