# Consignas del TP:
# El trabajo de investigación consiste en construir un programa en lenguaje Python 3.x que simule el funcionamiento del
# plato de una ruleta. Para esto se debe tener en cuenta los siguientes temas:
# • Generación de valores aleatorios enteros.
# • Uso de listas para el almacenamiento de datos.
# • Uso de la estructura de control FOR para iterar las listas.
# • Empleo de funciones estadísticas.
# • Gráficos de los resultados mediante el paquete Matplotlib.
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

    for j in range(cant_tiradas):
        if tipo_capital=='f' and cant_a_apostar>caja:
            break

        valor = random.randint(0, 36)

        if estrategia=="m":
            cant_a_apostar,caja=martingala(apuesta,valor,caja,cant_a_apostar,cantidad_apostada_inicial)
        elif estrategia=="d":
           cant_a_apostar,caja=dalembert()
        elif estrategia=="f":
           cant_a_apostar,caja=fibonacci()
        elif estrategia=="o":
            cant_a_apostar,caja,cortar=goBigOrGoHome(apuesta, valor, caja, cant_a_apostar, capital_inicial, cantidad_apostada_inicial)
            if cortar:
                break
        if valor==apuesta:
            gane=gane+1
        
        valores_caja.append(caja)
        valores_frecuencia_acumulada.append(gane/(j+1))  #j+1 porque j empieza en 0
    print(cant_a_apostar)
    print( valores_caja)
    print(valores_frecuencia_acumulada[:30])
    return valores_caja,valores_frecuencia_acumulada,capital_inicial


# ─────────────────────────────────────────────
# Graficación
# ─────────────────────────────────────────────
def graficar(valores_caja,valores_frecuencia_acumulada,capital_inicial):
  fig,(ax1,ax2)=plt.subplots(1,2,figsize=(12,5))
  eje_x=range(1,len(valores_frecuencia_acumulada)+1)
  ax1.bar(eje_x,valores_frecuencia_acumulada,color="red")
  ax1.set_xlabel('n (numero de tiradas)')
  ax1.set_ylabel('fr (frecuencia relativa)')
  ax1.set_title('Frecuencia relativa de obtener la apuesta favorable segun n')
  ax1.axhline(y=1/37, color='blue', linestyle='--', label='frec. esperada (1/37)')
  ax1.legend()
  ax2.plot(eje_x,valores_caja,color="red",label="fc (Flujo de caja)")
  ax2.axhline(y=capital_inicial,color="blue",linestyle="--",label="fci (flujo de caja inicial)")
  ax2.set_xlabel("n (numero de tiradas)")
  ax2.set_ylabel("cc (cantidad de capital)")
  ax2.set_title("Flujo de caja")
  ax2.legend()
  plt.tight_layout()
  plt.show()
# ─────────────────────────────────────────────
# Función principal de simulación
# ─────────────────────────────────────────────
def ruleta_casino(cant_corridas, cant_tiradas, nro_apostado, estretegia, tipo_capital):
    
    #esto seria para una sola corrida (las dos primeras graficas)
    valores_caja,valores_frecuencia_acumulada,capital_inicial=simular_corrida(cant_tiradas,nro_apostado,estretegia,tipo_capital)
    graficar(valores_caja,valores_frecuencia_acumulada,capital_inicial)

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
    elif apuesta == "primera columna" and valor in primera_columna: 
        caja=caja+cant_a_apostar*3-cant_a_apostar
        cant_a_apostar=cant_apostada_inicial
    elif apuesta == "segunda columna" and valor in segunda_columna: 
        caja=caja+cant_a_apostar*3-cant_a_apostar
        cant_a_apostar=cant_apostada_inicial
    elif apuesta == "tercera columna" and valor in tercera_columna: 
        caja=caja+cant_a_apostar*3-cant_a_apostar
        cant_a_apostar=cant_apostada_inicial
    elif valor == apuesta: 
        caja=caja+cant_a_apostar*36-cant_a_apostar
        cant_a_apostar=cant_apostada_inicial
    else:
        caja=caja-cant_a_apostar
        cant_a_apostar=cant_a_apostar*2
        
    return cant_a_apostar,caja

def dalembert():
    pass

def fibonacci():
    pass

def goBigOrGoHome(apuesta, valor, caja, cant_a_apostar, capital_inicial, cantidad_apostada_inicial):
    if valor == apuesta:
        caja = caja + cant_a_apostar * 35  # ganancia neta = apuesta * 35
        if caja >= capital_inicial * 2:
            return cant_a_apostar, caja, True   # duplicó → retirarse
        cant_a_apostar = cantidad_apostada_inicial
        return cant_a_apostar, caja, False
    else:
        caja = caja - cant_a_apostar
        cant_a_apostar = cant_a_apostar * 1.2
        if caja <= 0 or cant_a_apostar > caja:  # bancarrota
            return cant_a_apostar, caja, True
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
        if cant_tiradas >= 1 and cant_corridas >= 1 and ((isinstance(apuesta, int) and 0 <= apuesta <= 36) or apuesta in ["rojo","negro","par","impar","primera columna","segunda columna","tercera columna"]) and estrategia_utilizada in ['m','d','f','o'] and tipo_capital in ['i','f']:
            ruleta_casino(cant_corridas, cant_tiradas, apuesta, estrategia_utilizada, tipo_capital)
        else:
            print("Argumentos inválidos. Rangos: corridas>=1, tiradas>=1, número entre 0 y 36, estrategia tiene que estar entre ['m','d','f','o'] y tipo de capital tiene que estar entre ['i','f'] .")

    except (ValueError, IndexError):
        print("Uso correcto: python main.py -c <corridas> -n <tiradas> -e <número> -s <estrategia> -a <capital>")
        print("Ejemplo:      python main.py -c 5 -n 1000 -e 17 -s f -a f")


if __name__ == "__main__":
    main()