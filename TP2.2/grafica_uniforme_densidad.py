import numpy as np
import matplotlib.pyplot as plt

a = float(input("Límite inferior (a): "))
b = float(input("Límite superior (b): "))

def f(x, a, b):
    if a <= x <= b:
        return 1 / (b - a)
    return 0

margen = (b - a) * 0.3
x = np.linspace(a - margen, b + margen, 500)
y = [f(xi, a, b) for xi in x]

media = (a + b) / 2
altura = 1 / (b - a)

plt.figure(figsize=(8, 4))
plt.plot(x, y, color='steelblue', linewidth=2, label='f(x)')
plt.axvline(a, color='green', linestyle='--', label=f'a = {a}')
plt.axvline(b, color='green', linestyle='--', label=f'b = {b}')
plt.axvline(media, color='red', linestyle='--', label=f'μ = {media:.2f}')
plt.axhline(altura, color='orange', linestyle=':', alpha=0.5, label=f'1/(b-a) = {altura:.4f}')
plt.fill_between(x, y, alpha=0.1, color='steelblue')
plt.title(f'Función de densidad Uniforme(a={a}, b={b})')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.tight_layout()
plt.savefig('uniforme_densidad.png', dpi=150, bbox_inches='tight')
plt.show()
