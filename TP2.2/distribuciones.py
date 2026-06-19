# =============================================================================
# TP 2.2 - Generadores de Números Pseudoaleatorios
# Distribuciones de Probabilidad
# =============================================================================

import random
from math import exp, factorial, floor, log, sqrt
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# DISTRIBUCIÓN UNIFORME (Continua)
# -----------------------------------------------------------------------------


def distribucion_uniforme(a, b):
    r = random.random()
    return a + (b - a) * r


# -----------------------------------------------------------------------------
# DISTRIBUCIÓN normal (Continua)
# -----------------------------------------------------------------------------


def distribucion_normal(a, b):
    r = random.random()
    return a + (b - a) * r


# -----------------------------------------------------------------------------
# DISTRIBUCIÓN EXPONENCIAL (Continua)
# -----------------------------------------------------------------------------


def distribucion_exponencial(EX):
    r = random.random()
    return -EX * log(r)


# -----------------------------------------------------------------------------
# DISTRIBUCIÓN GAMMA (Continua)
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# DISTRIBUCIÓN NORMAL (Continua)
# -----------------------------------------------------------------------------

def distribucion_normal_limite_central(EX, VX):
    
    STDX = sqrt(VX)
    suma = sum(random.random() for _ in range(12))
    return STDX * (suma - 6) + EX


def distribucion_normal_von_neumann(EX, VX):
    
    STDX = sqrt(VX)
    aceptado = False
    while not aceptado:
        r1 = random.random()
        r2 = random.random()
        y = -log(r1)
        aceptado = r2 <= exp(-(y - 1)**2 / 2)
    r3 = random.random()
    if r3<=0.5:
        z=y
    else:
        z=-y
    return STDX * z + EX

# -----------------------------------------------------------------------------
# DISTRIBUCIÓN PASCAL (Discreta)
# -----------------------------------------------------------------------------


def distribucion_pascal(k, p):
    q = 1 - p
    logq = log(q)
    prod = 1.0
    for i in range(k):
        r = distribucion_uniforme(0, 1)
        prod *= r
    resultado = floor(log(prod) / logq)
    return resultado


# -----------------------------------------------------------------------------
# DISTRIBUCIÓN POISSON (Discreta)
# -----------------------------------------------------------------------------


def distribucion_poisson(lam):
    B = exp(-lam)
    TR = 1
    x = 0
    while True:
        r = random.random()
        TR *= r
        if TR >= B:
            x += 1
        else:
            return x


# -----------------------------------------------------------------------------
# DISTRIBUCIÓN EMPÍRICA DISCRETA (Discreta)
# -----------------------------------------------------------------------------


def distribucion_empirica_discreta(bs, ps):
    r = random.random()
    acumulada = 0
    for b, p in zip(bs, ps):
        acumulada += p
        if r <= acumulada:
            return b


# =============================================================================
# FUNCIONES AUXILIARES DE TEST
# =============================================================================


def _nombre_archivo(nombre):
    """Convierte el nombre de la distribución en un nombre de archivo válido."""
    return (
        nombre.lower()
        .replace("(", "")
        .replace(")", "")
        .replace("=", "")
        .replace(",", "")
        .replace(" ", "_")
        .replace("λ", "lambda")
    )


def _imprimir_resultados(nombre, media_teorica, varianza_teorica,
                          media_muestral, varianza_muestral):
    if media_teorica != 0:
        error_media = abs(media_muestral - media_teorica) / media_teorica * 100
    else:
        error_media = abs(media_muestral - media_teorica)

    if varianza_teorica != 0:
        error_varianza = abs(varianza_muestral - varianza_teorica) / varianza_teorica * 100
    else:
        error_varianza = abs(varianza_muestral - varianza_teorica)
    
    print("=" * 50)
    print(f"  TEST - Distribución {nombre}")
    print("=" * 50)
    print(f"  Media teórica     : {media_teorica:.4f}")
    print(f"  Media muestral    : {media_muestral:.4f}  (error: {error_media:.2f}%)")
    print(f"  Varianza teórica  : {varianza_teorica:.4f}")
    print(
        f"  Varianza muestral : {varianza_muestral:.4f}  (error: {error_varianza:.2f}%)"
    )
    resultado = "OK" if error_media < 10 and error_varianza < 15 else "REVISAR"
    print(f"\n  RESULTADO: {resultado}")
    print("=" * 50)


# =============================================================================
# TEST PARA DISTRIBUCIONES CONTINUAS
# =============================================================================


def testear_distribucion(valores, nombre, media_teorica, varianza_teorica):
    """
    Testea una distribución continua verificando:
      - Media muestral vs media teórica
      - Varianza muestral vs varianza teórica
      - Histograma con líneas de media muestral y teórica
    Guarda el gráfico como PNG para incluir en el informe.
    """
    n = len(valores)
    media_muestral = sum(valores) / n
    varianza_muestral = sum((x - media_muestral) ** 2 for x in valores) / n

    _imprimir_resultados(
        nombre, media_teorica, varianza_teorica, media_muestral, varianza_muestral
    )

    plt.figure(figsize=(8, 4))
    plt.hist(valores, bins=30, edgecolor="black", color="steelblue", alpha=0.7)
    plt.axvline(
        media_muestral,
        color="red",
        linestyle="--",
        label=f"Media muestral ({media_muestral:.2f})",
    )
    plt.axvline(
        media_teorica,
        color="green",
        linestyle="--",
        label=f"Media teórica ({media_teorica:.2f})",
    )
    plt.title(f"Histograma - Distribución {nombre}")
    plt.xlabel("Valores generados")
    plt.ylabel("Frecuencia")
    plt.legend()
    plt.tight_layout()
    archivo = _nombre_archivo(nombre) + ".png"
    plt.savefig(archivo, dpi=150, bbox_inches="tight")
    print(f"  Gráfico guardado: {archivo}")
    plt.show()


# =============================================================================
# TEST PARA DISTRIBUCIONES DISCRETAS
# =============================================================================


def testear_discreta(valores, nombre, media_teorica, varianza_teorica, probs_teoricas):
    """
    Testea una distribución discreta verificando:
      - Media muestral vs media teórica
      - Varianza muestral vs varianza teórica
      - Gráfico de barras: frecuencia relativa observada vs probabilidad teórica
    Guarda el gráfico como PNG para incluir en el informe.

    Parámetros:
        valores         : lista de valores generados
        nombre          : nombre de la distribución (para título y nombre de archivo)
        media_teorica   : EX teórico
        varianza_teorica: VX teórico
        probs_teoricas  : dict {valor: probabilidad_teorica}
    """
    n = len(valores)
    media_muestral = sum(valores) / n
    varianza_muestral = sum((x - media_muestral) ** 2 for x in valores) / n

    _imprimir_resultados(
        nombre, media_teorica, varianza_teorica, media_muestral, varianza_muestral
    )

    # Frecuencias relativas observadas por valor
    valores_unicos = sorted(probs_teoricas.keys())
    conteo = {v: 0 for v in valores_unicos}
    for v in valores:
        if v in conteo:
            conteo[v] += 1

    obs = [conteo[v] / n for v in valores_unicos]
    esp = [probs_teoricas[v] for v in valores_unicos]
    etiquetas = [str(v) for v in valores_unicos]
    x = range(len(valores_unicos))
    ancho = 0.35

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(
        [i - ancho / 2 for i in x],
        obs,
        ancho,
        label="Frecuencia relativa observada",
        color="steelblue",
        alpha=0.8,
        edgecolor="black",
    )
    ax.bar(
        [i + ancho / 2 for i in x],
        esp,
        ancho,
        label="Probabilidad teórica",
        color="green",
        alpha=0.8,
        edgecolor="black",
    )
    ax.set_xticks(list(x))
    ax.set_xticklabels(etiquetas)
    ax.set_title(f"Frecuencias observadas vs teóricas - Distribución {nombre}")
    ax.set_xlabel("Valor")
    ax.set_ylabel("Probabilidad / Frecuencia relativa")
    ax.legend()
    plt.tight_layout()
    archivo = _nombre_archivo(nombre) + ".png"
    plt.savefig(archivo, dpi=150, bbox_inches="tight")
    print(f"  Gráfico guardado: {archivo}")
    plt.show()


# =============================================================================
# MAIN
# =============================================================================


def main():
    opciones = "uniforme  / exponencial / gamma / normal / pascal / binomial / hipergeometrica / poisson / empirica"
    distribucion = input(f"Distribución ({opciones}): ").strip().lower()

    match distribucion:
        case "uniforme":
            a = float(input("a: "))
            b = float(input("b: "))
            valores = [distribucion_uniforme(a, b) for _ in range(1000)]
            testear_distribucion(
                valores,
                f"Uniforme(a={a}, b={b})",
                media_teorica=(a + b) / 2,
                varianza_teorica=(b - a) ** 2 / 12,
            )

        

        case "exponencial":
            EX = float(input("EX (media): "))
            valores = [distribucion_exponencial(EX) for _ in range(1000)]
            testear_distribucion(
                valores,
                f"Exponencial(EX={EX})",
                media_teorica=EX,
                varianza_teorica=EX**2,
            )

        case "pascal":
            k = int(input("k (número de éxitos buscados): "))
            p = float(input("p (probabilidad de éxito): "))
            valores = [distribucion_pascal(k, p) for _ in range(1000)]
            testear_distribucion(
                valores,
                f"Pascalk={k}p={p}",
                media_teorica=((k * (1 - p)) / p),
                varianza_teorica=(k * (1 - p) / p**2),
            )
        case "poisson":
            lam = float(input("λ (media): "))
            valores = [distribucion_poisson(lam) for _ in range(1000)]

            # Probabilidades teóricas para k = 0, 1, ..., max observado
            max_k = max(valores) + 1
            probs = {k: exp(-lam) * lam**k / factorial(k) for k in range(max_k)}

            testear_discreta(
                valores,
                f"Poisson(lambda={lam})",
                media_teorica=lam,
                varianza_teorica=lam,
                probs_teoricas=probs,
            )

        case "empirica":
            # Distribución de ejemplo — Naylor (1982), pág. 135
            bs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            ps = [0.273, 0.037, 0.195, 0.009, 0.124, 0.058, 0.062, 0.151, 0.047, 0.044]

            ex = sum(b * p for b, p in zip(bs, ps))
            vx = sum(b**2 * p for b, p in zip(bs, ps)) - ex**2
            probs = dict(zip(bs, ps))

            valores = [distribucion_empirica_discreta(bs, ps) for _ in range(1000)]
            testear_discreta(
                valores,
                "Empirica_Discreta",
                media_teorica=ex,
                varianza_teorica=vx,
                probs_teoricas=probs,
            )
        case "normal":
            EX = float(input("EX (media): "))
            VX = float(input("VX (varianza): "))
            
            # Límite central
            valores_lc = [distribucion_normal_limite_central(EX, VX) for _ in range(1000)]
            testear_distribucion(valores_lc, f"Normal_limite_central(EX={EX}, VX={VX})",
                                media_teorica=EX,
                                varianza_teorica=VX)
            
            # Von Neumann
            valores_vn = [distribucion_normal_von_neumann(EX, VX) for _ in range(1000)]
            testear_distribucion(valores_vn, f"Normal_von_neumann(EX={EX}, VX={VX})",
                                media_teorica=EX,
                                varianza_teorica=VX)
        case _:
            print("Distribución no reconocida.")


if __name__ == "__main__":
    main()
