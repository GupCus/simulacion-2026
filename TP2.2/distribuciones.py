# =============================================================================
# TP 2.2 - Generadores de Números Pseudoaleatorios
# Distribuciones de Probabilidad
# =============================================================================

### Elaborar un programa por cada distribución de probabilidad en lenguaje Python 3.x.
### Testear la generación de valores de la forma más conveniente para cada caso (queda a criterio del grupo el como testear).


import random
from math import log
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------------------------------------------------------
# DISTRIBUCIÓN UNIFORME (Continua)
# -----------------------------------------------------------------------------

def distribucion_uniforme(a, b):
    r = random.random()
    x = a + (b-a) * r
    return x


# -----------------------------------------------------------------------------
# DISTRIBUCIÓN EXPONENCIAL (Continua)
# -----------------------------------------------------------------------------

def distribucion_exponencial(EX):
    r = random.random()
    x = -EX * log(r)
    return x

# -----------------------------------------------------------------------------
# DISTRIBUCIÓN GAMMA (Continua)
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
# DISTRIBUCIÓN NORMAL (Continua)
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
# DISTRIBUCIÓN PASCAL (Discreta)
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
# DISTRIBUCIÓN BINOMIAL (Discreta)
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
# DISTRIBUCIÓN HIPERGEOMÉTRICA (Discreta)
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
# DISTRIBUCIÓN POISSON (Discreta)
# -----------------------------------------------------------------------------



# -----------------------------------------------------------------------------
# DISTRIBUCIÓN EMPÍRICA DISCRETA (Discreta)
# -----------------------------------------------------------------------------


# =============================================================================
# TEST GENERAL PARA DISTRIBUCIONES DE PROBABILIDAD
# =============================================================================
# Uso:
#   1. Generá una lista de valores con tu función de distribución
#   2. Llamá a testear_distribucion() con esa lista y los parámetros teóricos
#
    """
    Testea una distribución de probabilidad verificando:
      - Histograma (forma visual)
      - Media muestral vs media teórica
      - Varianza muestral vs varianza teórica
 
    Parámetros:
        valores        : lista de valores generados por la distribución
        nombre         : nombre de la distribución (para el título del gráfico)
        media_teorica  : EX teórico de la distribución
        varianza_teorica: VX teórico de la distribución
        n              : cantidad de valores generados (default 1000)
    """
# =============================================================================
 
def testear_distribucion(valores, nombre, media_teorica, varianza_teorica):
    n = len(valores)
    media_muestral    = sum(valores) / n
    varianza_muestral = sum((x - media_muestral) ** 2 for x in valores) / n
    error_media    = abs(media_muestral - media_teorica) / media_teorica * 100
    error_varianza = abs(varianza_muestral - varianza_teorica) / varianza_teorica * 100

    print("=" * 50)
    print(f"  TEST - Distribución {nombre}")
    print("=" * 50)
    print(f"  Media teórica     : {media_teorica:.4f}")
    print(f"  Media muestral    : {media_muestral:.4f}  (error: {error_media:.2f}%)")
    print(f"  Varianza teórica  : {varianza_teorica:.4f}")
    print(f"  Varianza muestral : {varianza_muestral:.4f}  (error: {error_varianza:.2f}%)")
    if error_media < 10 and error_varianza < 15:
        print(f"\n  RESULTADO: OK")
    else:
        print(f"\n  RESULTADO: REVISAR")
    print("=" * 50)

    plt.figure(figsize=(8, 4))
    plt.hist(valores, bins=30, edgecolor='black', color='steelblue', alpha=0.7)
    plt.axvline(media_muestral, color='red',   linestyle='--', label=f'Media muestral ({media_muestral:.2f})')
    plt.axvline(media_teorica,  color='green', linestyle='--', label=f'Media teórica ({media_teorica:.2f})')
    plt.title(f'Histograma - Distribución {nombre}')
    plt.xlabel('Valores generados')
    plt.ylabel('Frecuencia')
    plt.legend()
    plt.tight_layout()
    plt.show()

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":

    distribucion = input("Distribución (uniforme / exponencial): ").strip().lower()

    if distribucion == "uniforme":
        a = float(input("a: "))
        b = float(input("b: "))
        valores = [distribucion_uniforme(a, b) for _ in range(1000)]
        testear_distribucion(valores, f"Uniforme(a={a}, b={b})",
                             media_teorica=(a+b)/2,
                             varianza_teorica=(b-a)**2/12)

    elif distribucion == "exponencial":
        EX = float(input("EX (media): "))
        valores = [distribucion_exponencial(EX) for _ in range(1000)]
        testear_distribucion(valores, f"Exponencial(EX={EX})",
                             media_teorica=EX,
                             varianza_teorica=EX**2)

    else:
        print("Distribución no reconocida.")