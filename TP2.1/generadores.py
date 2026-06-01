### generadores pseudoaleatorios 




import math
import time


# ─── Helpers ─────────────────────────────────────────────────────────────────

def factores_primos(n):
    """Retorna los factores primos únicos de n (para verificar Hull-Dobell 2)."""
    factores = set()
    while n % 2 == 0:
        factores.add(2)
        n //= 2
    d = 3
    while d * d <= n:
        while n % d == 0:
            factores.add(d)
            n //= d
        d += 2
    if n > 1:
        factores.add(n)
    return sorted(factores)


# ─── Validación ──────────────────────────────────────────────────────────────

def validar_gcl(m, a, c, x0):
    """
    Verifica restricciones básicas y condiciones de Hull-Dobell.
    Retorna True si todo es válido, False (con mensaje) si hay error.
    """
    # Restricciones mínimas
    if m < 2:
        print("Error: m debe ser >= 2"); return False
    if not (1 <= a <= m - 1):
        print(f"Error: a debe estar en [1, {m-1}]"); return False
    if not (0 <= c <= m - 1):
        print(f"Error: c debe estar en [0, {m-1}]"); return False
    if not (0 <= x0 <= m - 1):
        print(f"Error: x0 debe estar en [0, {m-1}]"); return False

    # Hull-Dobell 1: c y m deben ser coprimos
    if math.gcd(c, m) != 1:
        print(f"Hull-Dobell 1 fallida: mcd(c={c}, m={m}) = {math.gcd(c,m)} ≠ 1")
        return False

    # Hull-Dobell 2: cada primo que divide a m debe dividir a (a-1)
    for p in factores_primos(m):
        if (a - 1) % p != 0:
            print(f"Hull-Dobell 2 fallida: (a-1)={a-1} no es divisible por {p}")
            return False

    # Hull-Dobell 3: si 4 | m, entonces 4 | (a-1)
    if m % 4 == 0 and (a - 1) % 4 != 0:
        print(f"Hull-Dobell 3 fallida: 4 | m={m} pero 4 no divide a (a-1)={a-1}")
        return False

    return True


# ─── Generador ───────────────────────────────────────────────────────────────

def gcl(m, a, c, x0, n):
    """
    Genera n números pseudoaleatorios en [0, 1).
    Fórmula: X(n+1) = (a * X(n) + c) mod m   →   U = X / m
    Retorna None si los parámetros son inválidos.
    """
    if not validar_gcl(m, a, c, x0):
        return None

    secuencia = []
    x = x0
    for _ in range(n):
        x = (a * x + c) % m
        secuencia.append(x / m)
    return secuencia


def detectar_periodo(m, a, c, x0, max_iter=1_000_000):
    """
    Detecta el período real del generador contando pasos hasta volver a x0.
    Usar solo con m pequeño; para m grande el período puede ser enorme.
    Retorna -1 si no se detecta en max_iter pasos.
    """
    x = x0
    for i in range(1, max_iter + 1):
        x = (a * x + c) % m
        if x == x0:
            return i
    return -1


# ─── Demo ─────────────────────────────────────────────────────────────────────

if _name_ == "_main_":

    # Parámetros de Numerical Recipes — cumple Hull-Dobell con m = 2^32
    M, A, C = 2**32, 1664525, 1013904223
    X0 = 42

    print("=== GCL — Numerical Recipes (m=2^32) ===")
    secuencia = gcl(M, A, C, X0, n=10)
    for i, u in enumerate(secuencia, 1):
        print(f"  U({i}) = {u:.8f}")

    # Comparación período completo vs incompleto con m=16
    print("\n=== Período completo vs incompleto (m=16) ===")

    # Cumple Hull-Dobell: a=5, c=1 → período = 16
    p_completo = detectar_periodo(16, 5, 1, x0=0)
    print(f"m=16, a=5,  c=1 → período = {p_completo}  ({'OK' if p_completo == 16 else 'INCOMPLETO'})")

    # Falla Hull-Dobell condición 3: a=3, c=1 → período = 8
    p_incompleto = detectar_periodo(16, 3, 1, x0=0)
    print(f"m=16, a=3,  c=1 → período = {p_incompleto}  ({'OK' if p_incompleto == 16 else 'INCOMPLETO'})")

    # RANDU: c=0 falla la condición 1 desde el inicio
    print("\n=== RANDU (parámetros defectuosos, c=0) ===")
    gcl(2**31, 65539, 0, 1, n=5)  # imprime el error de Hull-Dobell 1




























