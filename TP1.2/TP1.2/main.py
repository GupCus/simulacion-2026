# Consignas del TP:
# • Beneficios de las apuestas según la selección (color, fila, número único, etc).
# • Distintos tipos de estrategias de apuestas en la ruleta.
# • Gráficas de los resultados mediante el paquete Matplotlib (u otro similar).
# Se pide que se detalle la estrategias empleadas y las fuentes donde las obtuvieron (si no son de elaboración propia).
# Se proponen analizar 3 estrategia: la martingala, D’Alembert y Fibonacci,
# Por lo tanto la ejecución junto con el TP 1.1: python programa.py -c XXX -n YYY -e ZZ -s -a
# Nota: El parámetro -e es solo en caso de usar un solo número para la estrategia seleccionada, sino no es necesario.

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

# ─────────────────────────────────────────────
# Simulación de una corrida
# ─────────────────────────────────────────────
def simular_corrida(cant_tiradas, apuesta, estrategia,tipo_capital) -> tuple:
    caja=100000
    capital_inicial=caja
    cantidad_apostada_inicial=1000
    cant_a_apostar=cantidad_apostada_inicial
    valores_caja=[]
    valores_frecuencia_acumulada=[]
    gane=0
    cortar = False
    bancarrota = False

    for j in range(cant_tiradas):
        if tipo_capital=='f' and cant_a_apostar>caja:
            bancarrota = True
            break

        valor = random.randint(0, 36)

        if estrategia=="m":
            cant_a_apostar,caja=martingala(apuesta,valor,caja,cant_a_apostar,cantidad_apostada_inicial)
        elif estrategia=="d":
           cant_a_apostar, caja = dalembert(apuesta, valor, caja, cant_a_apostar, cantidad_apostada_inicial)
        elif estrategia=="f":
           cant_a_apostar,caja=fibonacci()
        elif estrategia=="o":
            cant_a_apostar,caja,cortar=goBigOrGoHome(apuesta, valor, caja, cant_a_apostar, capital_inicial, cantidad_apostada_inicial)
            if cortar:
                break
        
        if  (apuesta == "rojo" and valor in rojo) or \
            (apuesta == "negro" and valor in negro) or \
            (apuesta == "par" and valor != 0 and valor % 2 == 0) or \
            (apuesta == "impar" and valor != 0 and valor % 2 != 0) or \
            (apuesta == "c1" and valor in primera_columna) or \
            (apuesta == "c2" and valor in segunda_columna) or \
            (apuesta == "c3" and valor in tercera_columna) or \
            (valor == apuesta):
            gane = gane + 1
        
        valores_caja.append(caja)
        valores_frecuencia_acumulada.append(gane/(j+1))  #j+1 porque j empieza en 0
    #esto se printeaba para debuguear
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
# Graficación
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
    #esto seria para una sola corrida (las dos primeras graficas)
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

def martingala(apuesta, valor, caja,cant_a_apostar,cant_apostada_inicial) ->tuple:
   
    if apuesta == "rojo" and valor in rojo:
        caja=caja+cant_a_apostar*2-cant_a_apostar
        cant_a_apostar=cant_apostada_inicial
    elif apuesta == "negro" and valor in negro:
        caja=caja+cant_a_apostar*2-cant_a_apostar
        cant_a_apostar=cant_apostada_inicial
    elif apuesta == "par" and valor % 2 == 0 and valor != 0:
        caja=caja+cant_a_apostar*2-cant_a_apostar
        cant_a_apostar=cant_apostada_inicial
    elif apuesta == "impar" and valor % 2 != 0 and valor != 0:
        caja=caja+cant_a_apostar*2-cant_a_apostar
        cant_a_apostar=cant_apostada_inicial
    elif apuesta == "c1" and valor in primera_columna: 
        caja=caja+cant_a_apostar*3-cant_a_apostar
        cant_a_apostar=cant_apostada_inicial
    elif apuesta == "c2" and valor in segunda_columna: 
        caja=caja+cant_a_apostar*3-cant_a_apostar
        cant_a_apostar=cant_apostada_inicial
    elif apuesta == "c3" and valor in tercera_columna: 
        caja=caja+cant_a_apostar*3-cant_a_apostar
        cant_a_apostar=cant_apostada_inicial
    elif valor == apuesta: 
        caja=caja+cant_a_apostar*36-cant_a_apostar
        cant_a_apostar=cant_apostada_inicial
    else:
        caja=caja-cant_a_apostar
        cant_a_apostar=cant_a_apostar*2
        
    return cant_a_apostar,caja

def dalembert(apuesta, valor, caja, cant_a_apostar, cant_apostada_inicial) -> tuple:
    gano = False
    multiplicador_ganancia = 0

    if apuesta == "rojo" and valor in rojo:
        gano = True
        multiplicador_ganancia = 1
    elif apuesta == "negro" and valor in negro:
        gano = True
        multiplicador_ganancia = 1
    elif apuesta == "par" and valor % 2 == 0 and valor != 0:
        gano = True
        multiplicador_ganancia = 1
    elif apuesta == "impar" and valor % 2 != 0 and valor != 0:
        gano = True
        multiplicador_ganancia = 1
    elif apuesta == "c1" and valor in primera_columna:
        gano = True
        multiplicador_ganancia = 2
    elif apuesta == "c2" and valor in segunda_columna:
        gano = True
        multiplicador_ganancia = 2
    elif apuesta == "c3" and valor in tercera_columna:
        gano = True
        multiplicador_ganancia = 2
    elif valor == apuesta:
        gano = True
        multiplicador_ganancia = 35

    if gano:
        caja = caja + cant_a_apostar * multiplicador_ganancia
        # Bajar 1 unidad, pero nunca por debajo de la unidad base
        cant_a_apostar = max(cant_apostada_inicial, cant_a_apostar - cant_apostada_inicial)
    else:
        caja = caja - cant_a_apostar
        cant_a_apostar = cant_a_apostar + cant_apostada_inicial

    return cant_a_apostar, caja

def fibonacci():
    pass

def goBigOrGoHome(apuesta, valor, caja, cant_a_apostar, capital_inicial, cantidad_apostada_inicial):
    if valor == apuesta:
        caja = caja + cant_a_apostar * 35
        if caja >= capital_inicial * 2:
            return cant_a_apostar, caja, True
        cant_a_apostar = cantidad_apostada_inicial
        return cant_a_apostar, caja, False
    else:
        caja = caja - cant_a_apostar
        cant_a_apostar = cant_a_apostar * 1.2
        return cant_a_apostar, caja, False

# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────
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