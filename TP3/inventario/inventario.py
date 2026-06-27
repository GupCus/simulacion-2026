import random
import math
import argparse
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec






def simular_inventario(
    inventario_inicial=80,
    s=20,
    S=80,
    demanda_min=1,
    demanda_max=4,
    lambda_arribo=2.5,
    lead_time_min=1,
    lead_time_max=3,
    costo_fijo_orden=50.0,
    costo_incremental_orden=3.0,
    costo_mantenimiento=1.0,
    costo_faltante=10.0,
    tiempo_simulacion=365,
    seed=None,
):
   
    if seed is not None:
        random.seed(seed)

    inventario = inventario_inicial
    orden_pendiente = 0          
    dia_llegada_orden = None     

    
    area_positiva = 0.0          
    area_negativa = 0.0          

    num_ordenes = 0
    unidades_ordenadas_total = 0  

  
    dias = []
    niveles = []

    for dia in range(1, tiempo_simulacion + 1):

        
        if dia_llegada_orden is not None and dia >= dia_llegada_orden:
            inventario += orden_pendiente
            orden_pendiente = 0
            dia_llegada_orden = None

  
        if inventario < s and orden_pendiente == 0:
            cantidad_orden = S - inventario
            lead_time = random.randint(lead_time_min, lead_time_max)
            dia_llegada_orden = dia + lead_time
            orden_pendiente = cantidad_orden
            num_ordenes += 1
            unidades_ordenadas_total += cantidad_orden

        
        demanda_dia = 0
        tiempo_rel = 0.0  
        while True:
            tiempo_rel += random.expovariate(lambda_arribo)
            if tiempo_rel >= 1.0:
                break
            demanda_dia += random.randint(demanda_min, demanda_max)
        inventario -= demanda_dia

        
        area_positiva += max(inventario, 0)
        area_negativa += max(-inventario, 0)

        dias.append(dia)
        niveles.append(inventario)

    
    costo_orden_fijo_total      = num_ordenes * costo_fijo_orden
    costo_orden_incr_total      = unidades_ordenadas_total * costo_incremental_orden
    costo_orden_total           = costo_orden_fijo_total + costo_orden_incr_total
    costo_mant_total            = costo_mantenimiento * area_positiva
    costo_faltante_total        = costo_faltante * area_negativa
    costo_total                 = costo_orden_total + costo_mant_total + costo_faltante_total

    T = tiempo_simulacion
    return {
        "costo_orden":              costo_orden_total,
        "costo_orden_fijo":         costo_orden_fijo_total,
        "costo_orden_incremental":  costo_orden_incr_total,
        "costo_mantenimiento":      costo_mant_total,
        "costo_faltante":           costo_faltante_total,
        "costo_total":              costo_total,
        "costo_orden_dia":              costo_orden_total / T,
        "costo_orden_fijo_dia":         costo_orden_fijo_total / T,
        "costo_orden_incremental_dia":  costo_orden_incr_total / T,
        "costo_mantenimiento_dia":      costo_mant_total / T,
        "costo_faltante_dia":           costo_faltante_total / T,
        "costo_total_dia":              costo_total / T,
        "num_ordenes":              num_ordenes,
        "unidades_ordenadas_total": unidades_ordenadas_total,
        "inventario_final":         inventario,
        "dias":                     dias,
        "niveles":                  niveles,
        "area_positiva":            area_positiva,
        "area_negativa":            area_negativa,
    }



def correr_replicas(n_corridas=10, **kwargs):
    """Ejecuta n_corridas réplicas y devuelve estadísticas."""
    resultados = []
    for i in range(n_corridas):
        r = simular_inventario(seed=i * 42 + 7, **kwargs)
        resultados.append(r)

    claves = ["costo_orden", "costo_orden_fijo", "costo_orden_incremental",
              "costo_mantenimiento", "costo_faltante", "costo_total",
              "costo_orden_dia", "costo_orden_fijo_dia", "costo_orden_incremental_dia",
              "costo_mantenimiento_dia", "costo_faltante_dia", "costo_total_dia",
              "num_ordenes", "unidades_ordenadas_total"]

    estadisticas = {}
    for k in claves:
        vals = [r[k] for r in resultados]
        estadisticas[k] = {
            "media":   np.mean(vals),
            "std":     np.std(vals, ddof=1),
            "min":     np.min(vals),
            "max":     np.max(vals),
            "valores": vals,
        }
    return resultados, estadisticas



def graficar_resultados(resultados, estadisticas, params):
    fig = plt.figure(figsize=(18, 14))
    fig.suptitle(
        f"Simulación Inventario (s={params['s']}, S={params['S']}) — "
        f"{len(resultados)} corridas × {params['tiempo_simulacion']} días",
        fontsize=14, fontweight="bold", y=0.98,
    )

    gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35)

    
    ax1 = fig.add_subplot(gs[0, :])
    dias   = resultados[0]["dias"]
    nivs   = resultados[0]["niveles"]
    ax1.plot(dias, nivs, color="#2563eb", linewidth=0.8, label="Inventario I(t)")
    ax1.axhline(params["s"], color="#dc2626", linestyle="--", linewidth=1.2, label=f"s = {params['s']}")
    ax1.axhline(params["S"], color="#16a34a", linestyle="--", linewidth=1.2, label=f"S = {params['S']}")
    ax1.axhline(0, color="black", linewidth=0.5)
    ax1.fill_between(dias, 0, [max(n, 0) for n in nivs], alpha=0.15, color="#16a34a", label="I⁺(t)")
    ax1.fill_between(dias, 0, [min(n, 0) for n in nivs], alpha=0.25, color="#dc2626", label="I⁻(t) faltante")
    ax1.set_xlabel("Día")
    ax1.set_ylabel("Unidades")
    ax1.set_title("Trayectoria del inventario — corrida 1")
    ax1.legend(fontsize=8, ncol=5)
    ax1.grid(True, alpha=0.3)

   
    ax2 = fig.add_subplot(gs[1, :2])
    n_r = len(resultados)
    x = np.arange(n_r)
    w = 0.25
    co = [r["costo_orden"] for r in resultados]
    cm = [r["costo_mantenimiento"] for r in resultados]
    cf = [r["costo_faltante"] for r in resultados]
    bars1 = ax2.bar(x - w, co, w, label="Orden", color="#f59e0b")
    bars2 = ax2.bar(x,     cm, w, label="Mantenimiento", color="#3b82f6")
    bars3 = ax2.bar(x + w, cf, w, label="Faltante", color="#ef4444")
    ax2.set_xlabel("Corrida")
    ax2.set_ylabel("Costo ($)")
    ax2.set_title("Costos por corrida")
    ax2.set_xticks(x)
    ax2.set_xticklabels([f"C{i+1}" for i in range(n_r)])
    ax2.legend(fontsize=8)
    ax2.grid(True, axis="y", alpha=0.3)

    
    ax3 = fig.add_subplot(gs[1, 2])
    ct = [r["costo_total"] for r in resultados]
    ax3.bar(range(1, n_r + 1), ct, color="#8b5cf6", alpha=0.8)
    ax3.axhline(np.mean(ct), color="red", linestyle="--", label=f"Media=${np.mean(ct):.0f}")
    ax3.set_title("Costo total por corrida")
    ax3.set_xlabel("Corrida")
    ax3.set_ylabel("Costo ($)")
    ax3.legend(fontsize=8)
    ax3.grid(True, axis="y", alpha=0.3)

    
    ax4 = fig.add_subplot(gs[2, :2])
    datos_box = [
        [r["costo_orden"] for r in resultados],
        [r["costo_mantenimiento"] for r in resultados],
        [r["costo_faltante"] for r in resultados],
        [r["costo_total"] for r in resultados],
    ]
    bp = ax4.boxplot(datos_box, patch_artist=True, widths=0.5,
                     medianprops=dict(color="black", linewidth=2))
    colores = ["#f59e0b", "#3b82f6", "#ef4444", "#8b5cf6"]
    for patch, color in zip(bp["boxes"], colores):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    ax4.set_xticklabels(["Orden", "Mantenimiento", "Faltante", "Total"])
    ax4.set_ylabel("Costo ($)")
    ax4.set_title("Distribución de costos (boxplot, 10 corridas)")
    ax4.grid(True, axis="y", alpha=0.3)

   
    ax5 = fig.add_subplot(gs[2, 2])
    medias = [
        estadisticas["costo_orden"]["media"],
        estadisticas["costo_mantenimiento"]["media"],
        estadisticas["costo_faltante"]["media"],
    ]
    etiquetas = ["Orden", "Mantenimiento", "Faltante"]
    colores_pie = ["#f59e0b", "#3b82f6", "#ef4444"]
    wedges, texts, autotexts = ax5.pie(
        medias, labels=etiquetas, colors=colores_pie,
        autopct="%1.1f%%", startangle=90,
        textprops={"fontsize": 8}
    )
    ax5.set_title("Composición costo promedio")

    plt.savefig(SCRIPT_DIR / "inventario_resultados.png", dpi=150, bbox_inches="tight")
    print("\n→ Gráfico guardado: inventario_resultados.png")
    plt.close()


def graficar_evolucion_temporal(resultados):
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle("Evolución temporal de costos acumulados (todas las corridas)", fontsize=13)

    nombres = ["costo_orden", "costo_mantenimiento", "costo_faltante", "costo_total"]
    titulos = ["Costo de Orden", "Costo Mantenimiento", "Costo Faltante", "Costo Total"]
    colores = ["#f59e0b", "#3b82f6", "#ef4444", "#8b5cf6"]

    for ax, nombre, titulo, color in zip(axes.flat, nombres, titulos, colores):
        for i, r in enumerate(resultados):
            dias = r["dias"]
            niveles = r["niveles"]
            
            acum = []
            acum_val = 0.0
            ord_count = 0
            prev_niv = r["niveles"][0] if r["niveles"] else 0

            
            total = r[nombre]
            T = len(dias)
            serie = [total * d / T for d in dias]
            ax.plot(dias, serie, color=color, alpha=0.4, linewidth=0.8)

  
        total_media = np.mean([r[nombre] for r in resultados])
        T = len(resultados[0]["dias"])
        dias_ref = resultados[0]["dias"]
        ax.plot(dias_ref, [total_media * d / T for d in dias_ref],
                color="black", linewidth=2, linestyle="--", label=f"Media=${total_media:.0f}")
        ax.set_title(titulo, fontsize=10)
        ax.set_xlabel("Día")
        ax.set_ylabel("$ acumulado")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(SCRIPT_DIR / "inventario_evolucion.png", dpi=150, bbox_inches="tight")
    print("→ Gráfico guardado: inventario_evolucion.png")
    plt.close()



def imprimir_reporte(resultados, estadisticas, params):
    sep = "─" * 68
    
    
    print("  PARÁMETROS DE SIMULACIÓN")
    print(sep)
    for k, v in params.items():
        print(f"  {k:<30} {v}")

    print(f"\n{sep}")
    print("  RESULTADOS POR CORRIDA")
    print(sep)
    header = f"{'Corrida':>7} {'C.Ord.Fijo':>11} {'C.Ord.Incr.':>12} {'C.Orden':>10} {'C.Mant.':>10} {'C.Falt.':>10} {'C.Total':>10} {'N.Órd.':>7} {'Uds.Ord.':>9}"
    print(header)
    print("─" * 88)
    for i, r in enumerate(resultados, 1):
        print(f"  {i:>5}   {r['costo_orden_fijo']:>11.2f} {r['costo_orden_incremental']:>12.2f} "
              f"{r['costo_orden']:>10.2f} {r['costo_mantenimiento']:>10.2f} "
              f"{r['costo_faltante']:>10.2f} {r['costo_total']:>10.2f} "
              f"{r['num_ordenes']:>7} {r['unidades_ordenadas_total']:>9}")

    print(f"\n{sep}")
    print("  ESTADÍSTICAS RESUMIDAS (10 corridas)")
    print(sep)
    claves_display = {
        "costo_orden_fijo":        "  Costo Fijo Orden ($)",
        "costo_orden_incremental": "  Costo Incremental Orden ($)",
        "costo_orden":             "Costo de Orden Total ($)",
        "costo_mantenimiento":     "Costo Mantenimiento ($)",
        "costo_faltante":          "Costo Faltante ($)",
        "costo_total":             "Costo Total ($)",
        "costo_orden_fijo_dia":        "  C.Fijo Orden/día ($)",
        "costo_orden_incremental_dia": "  C.Incr. Orden/día ($)",
        "costo_orden_dia":             "Costo Orden Total/día ($)",
        "costo_mantenimiento_dia":     "Costo Mant./día ($)",
        "costo_faltante_dia":          "Costo Faltante/día ($)",
        "costo_total_dia":             "Costo Total/día ($)",
        "num_ordenes":             "Número de Órdenes",
        "unidades_ordenadas_total":"Unidades Ordenadas Total",
    }
    print(f"  {'Métrica':<28} {'Media':>10} {'Std':>10} {'Min':>10} {'Max':>10}")
    print("─" * 68)
    for clave, nombre in claves_display.items():
        e = estadisticas[clave]
        print(f"  {nombre:<28} {e['media']:>10.2f} {e['std']:>10.2f} {e['min']:>10.2f} {e['max']:>10.2f}")

    print(f"\n{sep}")
    print("  INTERPRETACIÓN")
    print(sep)
    ct_media = estadisticas["costo_total"]["media"]
    ct_std   = estadisticas["costo_total"]["std"]
    n = len(resultados)
    ic_low  = ct_media - 1.96 * ct_std / math.sqrt(n)
    ic_high = ct_media + 1.96 * ct_std / math.sqrt(n)
    print(f"  Costo total medio estimado: ${ct_media:,.2f}")
    print(f"  IC 95% (normal): [${ic_low:,.2f} ; ${ic_high:,.2f}]")
    print(f"  Composición media:")
    print(f"    · Orden (fijo)       : ${estadisticas['costo_orden_fijo']['media']:>8.2f}  "
          f"({estadisticas['costo_orden_fijo']['media']/ct_media*100:.1f}%)")
    print(f"    · Orden (incremental): ${estadisticas['costo_orden_incremental']['media']:>8.2f}  "
          f"({estadisticas['costo_orden_incremental']['media']/ct_media*100:.1f}%)")
    print(f"    · Orden (total)      : ${estadisticas['costo_orden']['media']:>8.2f}  "
          f"({estadisticas['costo_orden']['media']/ct_media*100:.1f}%)")
    print(f"    · Mantenimiento      : ${estadisticas['costo_mantenimiento']['media']:>8.2f}  "
          f"({estadisticas['costo_mantenimiento']['media']/ct_media*100:.1f}%)")
    print(f"    · Faltante           : ${estadisticas['costo_faltante']['media']:>8.2f}  "
          f"({estadisticas['costo_faltante']['media']/ct_media*100:.1f}%)")
    print(sep)



def parse_args():
    parser = argparse.ArgumentParser(
        description="Simulación de inventario (s, S) — TP Simulación UTN FRRO",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--inventario-inicial", type=int, default=None,
                        help="Inventario inicial (default: igual a S)")
    parser.add_argument("--s",                  type=int, default=10,  help="Punto de reorden")
    parser.add_argument("--S",                  type=int, default=40,  help="Nivel máximo de inventario")
    parser.add_argument("--demanda-min",         type=int, default=1)
    parser.add_argument("--demanda-max",         type=int, default=4)
    parser.add_argument("--lambda-arribo",        type=float, default=2.5,   help="Tasa de arribos de demanda por día (λ)")
    parser.add_argument("--lead-time-min",       type=int, default=1)
    parser.add_argument("--lead-time-max",       type=int, default=3)
    parser.add_argument("--costo-fijo-orden",        type=float, default=50.0,  help="$ fijo por pedido (K)")
    parser.add_argument("--costo-incremental-orden",  type=float, default=3.0,   help="$ por unidad pedida (i)")
    parser.add_argument("--costo-mantenimiento", type=float, default=1.0,   help="$ por unidad·día")
    parser.add_argument("--costo-faltante",      type=float, default=10.0,  help="$ por unidad·día")
    parser.add_argument("--tiempo-simulacion",   type=int, default=365,    help="Días a simular")
    parser.add_argument("--corridas",            type=int, default=10)
    parser.add_argument("--sin-graficos",        action="store_true",       help="No generar gráficos")
    return parser.parse_args()



def main():
    args = parse_args()

    if args.inventario_inicial is None:
        args.inventario_inicial = args.S

    params = {
        "inventario_inicial":   args.inventario_inicial,
        "s":                    args.s,
        "S":                    args.S,
        "demanda_min":          args.demanda_min,
        "demanda_max":          args.demanda_max,
        "lambda_arribo":        args.lambda_arribo,
        "lead_time_min":        args.lead_time_min,
        "lead_time_max":        args.lead_time_max,
        "costo_fijo_orden":       args.costo_fijo_orden,
        "costo_incremental_orden": args.costo_incremental_orden,
        "costo_mantenimiento":  args.costo_mantenimiento,
        "costo_faltante":       args.costo_faltante,
        "tiempo_simulacion":    args.tiempo_simulacion,
    }

    print(f"\nEjecutando {args.corridas} corridas...")
    resultados, estadisticas = correr_replicas(n_corridas=args.corridas, **params)

    imprimir_reporte(resultados, estadisticas, {**params, "corridas": args.corridas})

    if not args.sin_graficos:
        graficar_resultados(resultados, estadisticas, params)
        graficar_evolucion_temporal(resultados)
        print("\nGráficos generados exitosamente.")


if __name__ == "__main__":
    main()