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
def simular_corrida(cant_tiradas, nro_apostado, estrategia,tipo_capital) -> tuple:
    caja=1000000
    capital_inicial=caja
    cantidad_apostada_inicial=100
    cant_a_apostar=cantidad_apostada_inicial
    valores_caja=[]
    valores_frecuencia_acumulada=[]
    gane=0

    for j in range(cant_tiradas):
        if tipo_capital=='f' and cant_a_apostar>caja:
            break

        valor = random.randint(0, 36)

        if estrategia=="m":
            cant_a_apostar,caja=martingala(nro_apostado,valor,caja,cant_a_apostar,cantidad_apostada_inicial)
        elif estrategia=="d":
           cant_a_apostar,caja=dalembert()
        elif estrategia=="f":
           cant_a_apostar,caja=fibonacci()
        elif estrategia=="o":
            cant_a_apostar,caja=goBigOrGoHome()
        
        if valor==nro_apostado:
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

def martingala(nro_apostado, valor, caja,cant_a_apostar,cant_apostada_inicial) ->tuple:
    if valor == nro_apostado:
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
def goBigOrGoHome():
    pass


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────
def main():
    try:
        cant_corridas = int(sys.argv[2])
        cant_tiradas  = int(sys.argv[4])
        nro_apostado  = int(sys.argv[6])
        estrategia_utilizada=sys.argv[8]
        tipo_capital=sys.argv[10]
        if cant_tiradas >= 1 and cant_corridas >= 1 and 0 <= nro_apostado <= 36 and estrategia_utilizada in ['m','d','f','o'] and tipo_capital in['i','f']:
            ruleta_casino(cant_corridas, cant_tiradas, nro_apostado,estrategia_utilizada,tipo_capital)
        else:
            print("Argumentos inválidos. Rangos: corridas>=1, tiradas>=1, número entre 0 y 36, estrategia tiene que estar entre ['m','d','f','o'] y tipo de capital tiene que estar entre ['i','f'] .")

    except (ValueError, IndexError):
        print("Uso correcto: python main.py -c <corridas> -n <tiradas> -e <número> -s <estrategia> -a <capital>")
        print("Ejemplo:      python main.py -c 5 -n 1000 -e 17 -s f -a f")


if __name__ == "__main__":
    main()