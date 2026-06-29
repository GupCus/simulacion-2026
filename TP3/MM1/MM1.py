# mm1.py - Simulación M/M/1 y M/M/1/K por eventos discretos
# TP3 - Simulación - UTN FRRO
#
# Uso:
#   python mm1.py                              (usa defaults: μ=20, 10 corridas, T=10000)
#   python mm1.py --mu 20 --corridas 10 --tiempo 10000 --output-dir resultados

import os
import json
import random
import argparse
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict


# ── Fórmulas teóricas M/M/1 ───────────────────────────────────────────────────

def teorico_mm1(lam, mu):
    """Métricas teóricas del M/M/1. Devuelve inf si ρ ≥ 1 (sistema inestable)."""
    rho = lam / mu
    if rho >= 1.0:
        return {"rho": rho, "L": float("inf"), "Lq": float("inf"),
                "W": float("inf"), "Wq": float("inf")}
    L  = rho / (1 - rho)
    Lq = rho**2 / (1 - rho)
    W  = 1 / (mu - lam)
    Wq = lam / (mu * (mu - lam))
    return {"rho": rho, "L": L, "Lq": Lq, "W": W, "Wq": Wq}


def teorico_pn_mm1(rho, n):
    """P(n clientes en el sistema) para M/M/1 en estado estacionario."""
    if rho >= 1.0:
        return float("nan")
    return (1 - rho) * rho**n


def teorico_mm1k(lam, mu, K):
    """
    Métricas teóricas M/M/1/K.
    K = capacidad de la COLA. Sistema admite K+1 clientes en total.
    """
    rho = lam / mu
    S   = K + 1     # capacidad total del sistema
    if abs(rho - 1.0) < 1e-9:
        p0 = 1.0 / (S + 1)
        pn = [p0] * (S + 1)
    else:
        p0 = (1 - rho) / (1 - rho**(S + 1))
        pn = [p0 * rho**n for n in range(S + 1)]
    Pb    = pn[S]                        # P(bloqueo) = P(sistema lleno)
    lam_e = lam * (1 - Pb)              # tasa efectiva de ingreso
    L     = sum(n * pn[n] for n in range(S + 1))
    Lq    = sum(max(n - 1, 0) * pn[n] for n in range(S + 1))
    W     = L  / lam_e if lam_e > 0 else float("inf")
    Wq    = Lq / lam_e if lam_e > 0 else float("inf")
    return {"rho": rho, "L": L, "Lq": Lq, "W": W, "Wq": Wq, "Pb": Pb}


# ── P(n en cola), a partir de P(n en sistema) ─────────────────────────────────

def pn_sistema_a_cola(pn_sistema, n_max):
    """
    Convierte P(n en sistema) a P(n en cola).
    P(0 en cola) = P(0 en sistema) + P(1 en sistema)  (servidor libre u ocupado sin nadie esperando)
    P(n en cola) = P(n+1 en sistema) para n >= 1
    `pn_sistema` puede ser dict {n: prob} o lista indexada por n.
    """
    def get(k):
        if isinstance(pn_sistema, dict):
            return pn_sistema.get(k, 0.0)
        return pn_sistema[k] if k < len(pn_sistema) else 0.0

    cola = [get(0) + get(1)]
    for n in range(1, n_max + 1):
        cola.append(get(n + 1))
    return cola


# ── Simulación por eventos discretos: M/M/1 ───────────────────────────────────

def simular_mm1(lam, mu, T, semilla=None, registrar_evolucion=False):
    """
    Una corrida de M/M/1 por eventos discretos.

    Idea: en lugar de avanzar segundo a segundo, saltamos de evento a evento
    (llegada o salida). En cada salto acumulamos el área bajo n(t) para
    calcular los promedios temporales L y Lq.

    Si registrar_evolucion=True, además guarda la evolución de los promedios
    acumulados L(t)=area_n(t)/t y Lq(t)=area_nq(t)/t en cada evento, útil para
    ver cómo el sistema converge al estado estacionario.

    Retorna dict con: L, Lq, W, Wq, rho, pn [, evolucion]
    """
    if semilla is not None:
        random.seed(semilla)

    t      = 0.0           # tiempo actual
    n      = 0             # clientes en el sistema ahora mismo
    t_ult  = 0.0           # tiempo del último evento (para calcular área)
    area_n = 0.0           # ∫ n(t) dt  → al final: L = area_n / T
    area_nq = 0.0          # ∫ nq(t) dt → al final: Lq = area_nq / T
    t_busy = 0.0           # tiempo con servidor ocupado → ρ = t_busy / T
    hist_n = defaultdict(float)   # tiempo acumulado en cada estado n (para P(n))
    evol_t, evol_L, evol_Lq = [], [], []   # evolución temporal (opcional)

    # programar primer arribo y primera salida
    t_arr = random.expovariate(lam)
    t_dep = float("inf")          # sin clientes → sin salida

    while True:
        t_next  = min(t_arr, t_dep)
        t_corte = min(t_next, T)    # no acumular más allá del horizonte

        # acumular área entre t_ult y t_corte
        dt = t_corte - t_ult
        area_n  += n * dt
        area_nq += max(n - 1, 0) * dt
        if n > 0:
            t_busy += dt
        hist_n[n] += dt
        t_ult = t_corte

        if registrar_evolucion and t_corte > 0:
            evol_t.append(t_corte)
            evol_L.append(area_n / t_corte)
            evol_Lq.append(area_nq / t_corte)

        if t_next > T:
            break   # próximo evento fuera del horizonte → fin

        t = t_next

        if t_arr <= t_dep:
            # ── Evento: llegada ──────────────────────────────────────────────
            n += 1
            t_arr = t + random.expovariate(lam)
            if n == 1:                     # servidor estaba libre → arranca servicio
                t_dep = t + random.expovariate(mu)

        else:
            # ── Evento: salida ───────────────────────────────────────────────
            n -= 1
            t_dep = t + random.expovariate(mu) if n > 0 else float("inf")

    L   = area_n  / T
    Lq  = area_nq / T
    rho = t_busy  / T
    W   = L  / lam      # Ley de Little: W = L / λ
    Wq  = Lq / lam      # Ley de Little: Wq = Lq / λ
    pn  = {k: v / T for k, v in hist_n.items()}

    resultado = {"L": L, "Lq": Lq, "W": W, "Wq": Wq, "rho": rho, "pn": pn}
    if registrar_evolucion:
        resultado["evolucion"] = {"t": evol_t, "L": evol_L, "Lq": evol_Lq}
    return resultado


# ── Simulación por eventos discretos: M/M/1/K ─────────────────────────────────

def simular_mm1k(lam, mu, K, T, semilla=None):
    """
    Una corrida de M/M/1/K (cola finita de tamaño K).
    Cuando el sistema tiene K+1 clientes (cola llena + servidor ocupado),
    los nuevos arrivals son rechazados → denegación de servicio.
    """
    if semilla is not None:
        random.seed(semilla)

    t, n, t_ult = 0.0, 0, 0.0
    area_n = area_nq = t_busy = 0.0
    rechazados = llegadas = 0
    S = K + 1     # capacidad total (cola + servidor)

    t_arr = random.expovariate(lam)
    t_dep = float("inf")

    while True:
        t_next  = min(t_arr, t_dep)
        t_corte = min(t_next, T)
        dt = t_corte - t_ult
        area_n  += n * dt
        area_nq += max(n - 1, 0) * dt
        if n > 0:
            t_busy += dt
        t_ult = t_corte

        if t_next > T:
            break

        t = t_next

        if t_arr <= t_dep:
            llegadas += 1
            if n < S:                           # hay lugar en el sistema
                n += 1
                if n == 1:
                    t_dep = t + random.expovariate(mu)
            else:                               # sistema lleno → rechazo
                rechazados += 1
            t_arr = t + random.expovariate(lam)

        else:
            n -= 1
            t_dep = t + random.expovariate(mu) if n > 0 else float("inf")

    Pb    = rechazados / llegadas if llegadas > 0 else 0.0
    lam_e = lam * (1 - Pb)    # tasa efectiva (solo los que entran)
    L     = area_n  / T
    Lq    = area_nq / T
    rho   = t_busy  / T
    W     = L  / lam_e if lam_e > 0 else float("inf")
    Wq    = Lq / lam_e if lam_e > 0 else float("inf")

    return {"L": L, "Lq": Lq, "W": W, "Wq": Wq, "rho": rho, "Pb": Pb}


# ── N corridas y promedio ──────────────────────────────────────────────────────

def experimento(lam, mu, T, n_corridas):
    """Corre n_corridas del M/M/1 y devuelve el promedio de cada métrica."""
    resultados = [simular_mm1(lam, mu, T) for _ in range(n_corridas)]
    metricas   = ["L", "Lq", "W", "Wq", "rho"]
    prom = {m: sum(r[m] for r in resultados) / n_corridas for m in metricas}
    # promediar también P(n)
    todos_n  = set(k for r in resultados for k in r["pn"])
    prom["pn"] = {k: sum(r["pn"].get(k, 0.0) for r in resultados) / n_corridas
                  for k in todos_n}
    return prom


def experimento_k(lam, mu, K, T, n_corridas):
    """Corre n_corridas del M/M/1/K y devuelve el promedio de cada métrica."""
    resultados = [simular_mm1k(lam, mu, K, T) for _ in range(n_corridas)]
    metricas   = ["L", "Lq", "W", "Wq", "rho", "Pb"]
    return {m: sum(r[m] for r in resultados) / n_corridas for m in metricas}


# ── Gráficas ──────────────────────────────────────────────────────────────────

METRICAS_INFO = [
    ("L",   "Clientes en sistema (L)"),
    ("Lq",  "Clientes en cola (Lq)"),
    ("W",   "Tiempo en sistema (W)"),
    ("Wq",  "Tiempo en cola (Wq)"),
    ("rho", "Utilización del servidor (ρ)"),
]


def _grid_metricas(rhos, series, titulo, archivo):
    """series: lista de (valores_dict, color, estilo, etiqueta) a graficar juntas."""
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    axes = axes.flatten()
    for i, (m, subtitulo) in enumerate(METRICAS_INFO):
        ax = axes[i]
        for valores, color, estilo, etiqueta in series:
            ax.plot(rhos, valores[m], estilo, color=color, label=etiqueta)
        ax.set_xlabel("ρ = λ/μ")
        ax.set_ylabel(subtitulo)
        ax.set_title(subtitulo)
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
    axes[5].set_visible(False)
    plt.suptitle(titulo, fontsize=12)
    plt.tight_layout()
    plt.savefig(archivo, dpi=150)
    plt.close()
    print(f"Guardado: {archivo}")


def graficar_metricas(mu, rhos, sim_metricas, teo_metricas, n_corridas, T, output_dir):
    """Genera teorico_metricas.png, python_metricas.png y comparacion_metricas.png."""
    sim = {m: [sim_metricas[i][m] for i in range(len(rhos))] for m, _ in METRICAS_INFO}
    teo = {m: [float("nan") if teo_metricas[i][m] == float("inf") else teo_metricas[i][m]
               for i in range(len(rhos))] for m, _ in METRICAS_INFO}

    titulo = f"M/M/1 — μ={mu}, corridas={n_corridas}, T={T}"
    _grid_metricas(rhos, [(teo, "tomato", "s--", "Teórico")],
                   titulo, os.path.join(output_dir, "teorico_metricas.png"))
    _grid_metricas(rhos, [(sim, "steelblue", "o-", "Simulado (Python)")],
                   titulo, os.path.join(output_dir, "python_metricas.png"))
    _grid_metricas(rhos, [(sim, "steelblue", "o-", "Simulado (Python)"),
                          (teo, "tomato", "s--", "Teórico")],
                   titulo, os.path.join(output_dir, "comparacion_metricas.png"))


def _grafico_pn(ns, series, titulo, archivo):
    """series: lista de (valores, color, etiqueta) a graficar como barras."""
    x = np.arange(len(ns))
    w = 0.35 if len(series) > 1 else 0.6
    fig, ax = plt.subplots(figsize=(10, 5))
    offsets = np.linspace(-w/2, w/2, len(series)) if len(series) > 1 else [0]
    for (valores, color, etiqueta), off in zip(series, offsets):
        ax.bar(x + off, valores, w if len(series) == 1 else w, label=etiqueta, color=color, alpha=0.8)
    ax.set_xticks(x)
    ax.set_xticklabels(ns)
    ax.set_xlabel("n (clientes en cola)")
    ax.set_ylabel("P(n en cola)")
    ax.set_title(titulo)
    ax.legend()
    ax.grid(True, alpha=0.3, axis="y")
    plt.tight_layout()
    plt.savefig(archivo, dpi=150)
    plt.close()
    print(f"Guardado: {archivo}")


def graficar_pn(lam, mu, pn_sim_sistema, output_dir, n_max=15):
    """P(n en cola), no P(n en sistema): teorico_pn.png, python_pn.png, comparacion_pn.png."""
    rho = lam / mu
    ns  = list(range(n_max + 1))

    pn_teo_sistema = {n: teorico_pn_mm1(rho, n) for n in range(n_max + 2)}
    teo_cola = pn_sistema_a_cola(pn_teo_sistema, n_max)
    sim_cola = pn_sistema_a_cola(pn_sim_sistema, n_max)

    titulo = f"P(n en cola) — M/M/1 con ρ={rho:.2f} (λ={lam}, μ={mu})"
    _grafico_pn(ns, [(teo_cola, "tomato", "Teórico")],
                titulo, os.path.join(output_dir, "teorico_pn.png"))
    _grafico_pn(ns, [(sim_cola, "steelblue", "Simulado (Python)")],
                titulo, os.path.join(output_dir, "python_pn.png"))
    _grafico_pn(ns, [(sim_cola, "steelblue", "Simulado (Python)"), (teo_cola, "tomato", "Teórico")],
                titulo, os.path.join(output_dir, "comparacion_pn.png"))

    return teo_cola, sim_cola


def graficar_denegacion(capacidades, sim_pb, teo_pb, rho_base, output_dir):
    """P(bloqueo) por K: teorico_denegacion.png, python_denegacion.png, comparacion_denegacion.png."""
    x = np.arange(len(capacidades))
    etiquetas = [f"K={k}" for k in capacidades]
    titulo = f"Probabilidad de denegación — M/M/1/K, ρ={rho_base:.2f}"

    def plot(series, archivo):
        w = 0.35 if len(series) > 1 else 0.6
        offsets = np.linspace(-w/2, w/2, len(series)) if len(series) > 1 else [0]
        fig, ax = plt.subplots(figsize=(8, 5))
        for (valores, color, etiqueta), off in zip(series, offsets):
            ax.bar(x + off, valores, w, label=etiqueta, color=color, alpha=0.8)
        ax.set_xticks(x)
        ax.set_xticklabels(etiquetas)
        ax.set_xlabel("Capacidad de cola K")
        ax.set_ylabel("P(bloqueo)")
        ax.set_title(titulo)
        ax.legend()
        ax.grid(True, alpha=0.3, axis="y")
        plt.tight_layout()
        plt.savefig(archivo, dpi=150)
        plt.close()
        print(f"Guardado: {archivo}")

    plot([(teo_pb, "tomato", "Teórico")], os.path.join(output_dir, "teorico_denegacion.png"))
    plot([(sim_pb, "steelblue", "Simulado (Python)")], os.path.join(output_dir, "python_denegacion.png"))
    plot([(sim_pb, "steelblue", "Simulado (Python)"), (teo_pb, "tomato", "Teórico")],
         os.path.join(output_dir, "comparacion_denegacion.png"))


def graficar_evolucion(lam, mu, T, output_dir, max_puntos=3000):
    """python_evolucion.png: L(t) y Lq(t) acumulados, para ver convergencia al estado estacionario."""
    res = simular_mm1(lam, mu, T, registrar_evolucion=True)
    evol = res["evolucion"]
    t, L, Lq = evol["t"], evol["L"], evol["Lq"]

    # downsamplear si hay demasiados eventos, para que el gráfico no sea pesado
    paso = max(1, len(t) // max_puntos)
    t, L, Lq = t[::paso], L[::paso], Lq[::paso]

    rho = lam / mu
    teo = teorico_mm1(lam, mu)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(t, L,  color="steelblue", label="L(t) simulado")
    ax.plot(t, Lq, color="darkorange", label="Lq(t) simulado")
    if teo["L"] != float("inf"):
        ax.axhline(teo["L"],  color="steelblue",  linestyle="--", alpha=0.6, label="L teórico")
        ax.axhline(teo["Lq"], color="darkorange", linestyle="--", alpha=0.6, label="Lq teórico")
    ax.set_xlabel("Tiempo de simulación")
    ax.set_ylabel("Promedio acumulado de clientes")
    ax.set_title(f"Evolución temporal — M/M/1 con ρ={rho:.2f} (λ={lam}, μ={mu})")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    archivo = os.path.join(output_dir, "python_evolucion.png")
    plt.savefig(archivo, dpi=150)
    plt.close()
    print(f"Guardado: {archivo}")


# ── Tablas en consola, separadas por fuente ───────────────────────────────────

def _fmt(v):
    return f"{v:.4f}" if v != float("inf") else "     ∞"


def imprimir_tabla(titulo, rhos, lista_metricas):
    sep = "─" * 60
    print(f"\n{titulo:^60}")
    print(sep)
    print(f"{'ρ':>5} │ {'L':>9} {'Lq':>9} {'W':>9} {'Wq':>9} {'ρ_obs':>9}")
    print(sep)
    for rho, m in zip(rhos, lista_metricas):
        print(f"{rho:>5.2f} │ {_fmt(m['L']):>9} {_fmt(m['Lq']):>9} "
              f"{_fmt(m['W']):>9} {_fmt(m['Wq']):>9} {_fmt(m['rho']):>9}")


def imprimir_denegacion(titulo, capacidades, pb_lista):
    sep = "─" * 35
    print(f"\n{titulo:^35}")
    print(sep)
    print(f"{'K':>5} │ {'Pb':>12}")
    print(sep)
    for K, pb in zip(capacidades, pb_lista):
        print(f"{K:>5} │ {pb:>12.6f}")


# ── JSON ───────────────────────────────────────────────────────────────────────

def _safe(v):
    """Convierte inf/nan a None para que el JSON sea estándar."""
    if isinstance(v, float) and (v == float("inf") or v != v):
        return None
    return v


def guardar_json(path, rhos, mu, metricas_lista, capacidades, pb_lista):
    experimentos = [
        {
            "rho": rho,
            "lam": rho * mu,
            "L":  _safe(m["L"]),
            "Lq": _safe(m["Lq"]),
            "W":  _safe(m["W"]),
            "Wq": _safe(m["Wq"]),
            "rho_sim": _safe(m["rho"]),
        }
        for rho, m in zip(rhos, metricas_lista)
    ]
    denegacion = [{"K": K, "Pb": _safe(pb)} for K, pb in zip(capacidades, pb_lista)]

    data = {"experimentos": experimentos, "denegacion": denegacion}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Guardado: {path}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Simulación M/M/1 — TP3 UTN FRRO")
    ap.add_argument("--mu",       type=float, default=20.0,
                    help="Tasa de servicio μ (def: 20, igual que AnyLogic)")
    ap.add_argument("--corridas", type=int,   default=10,
                    help="Corridas por experimento (def: 10)")
    ap.add_argument("--tiempo",   type=float, default=10000.0,
                    help="Tiempo de simulación T (def: 10000, igual que AnyLogic)")
    ap.add_argument("--output-dir", type=str, default=".",
                    help="Directorio donde guardar gráficas y JSON (def: directorio actual)")
    args = ap.parse_args()

    mu         = args.mu
    n_corridas = args.corridas
    T          = args.tiempo
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)

    # ρ = λ/μ: 25%, 50%, 75%, 100%, 125% de la tasa de servicio
    rhos        = [0.25, 0.50, 0.75, 1.00, 1.25]
    # tamaños de cola finita para análisis de denegación
    capacidades = [0, 2, 5, 10, 50]
    rho_base    = 0.75   # corrida representativa para P(n), denegación y evolución

    print(f"\nParámetros: μ={mu}, corridas={n_corridas}, T={T}")
    print(f"λ por experimento: {[round(r*mu,2) for r in rhos]}")

    # ── Calcular métricas de los dos experimentos por ρ ──────────────────────
    teo_metricas = [teorico_mm1(rho * mu, mu) for rho in rhos]
    sim_metricas = [experimento(rho * mu, mu, T, n_corridas) for rho in rhos]

    imprimir_tabla(f"M/M/1 TEÓRICO — μ={mu}", rhos, teo_metricas)
    imprimir_tabla(f"M/M/1 SIMULACIÓN PYTHON — μ={mu}, corridas={n_corridas}, T={T}",
                    rhos, sim_metricas)

    # ── Denegación de servicio, M/M/1/K con ρ=0.75 ────────────────────────────
    lam_base = rho_base * mu
    sim_pb = [experimento_k(lam_base, mu, K, T, n_corridas)["Pb"] for K in capacidades]
    teo_pb = [teorico_mm1k(lam_base, mu, K)["Pb"] for K in capacidades]

    imprimir_denegacion(f"M/M/1/K TEÓRICO (ρ={rho_base})", capacidades, teo_pb)
    imprimir_denegacion(f"M/M/1/K SIMULACIÓN PYTHON (ρ={rho_base})", capacidades, sim_pb)

    # ── Gráficas ───────────────────────────────────────────────────────────────
    print("\nGenerando gráficas...")
    graficar_metricas(mu, rhos, sim_metricas, teo_metricas, n_corridas, T, output_dir)

    idx_base = rhos.index(rho_base)
    graficar_pn(lam_base, mu, sim_metricas[idx_base]["pn"], output_dir)

    graficar_denegacion(capacidades, sim_pb, teo_pb, rho_base, output_dir)
    graficar_evolucion(lam_base, mu, T, output_dir)

    # ── JSON ────────────────────────────────────────────────────────────────────
    guardar_json(os.path.join(output_dir, "resultados_teorico.json"),
                 rhos, mu, teo_metricas, capacidades, teo_pb)
    guardar_json(os.path.join(output_dir, "resultados_python.json"),
                 rhos, mu, sim_metricas, capacidades, sim_pb)

    print("\nListo.")


if __name__ == "__main__":
    main()
