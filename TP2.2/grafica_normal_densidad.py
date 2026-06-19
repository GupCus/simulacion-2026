import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, exp, pi

def f(x, mu, sigma):
    return (1 / (sigma * sqrt(2 * pi))) * exp(-0.5 * ((x - mu) / sigma) ** 2)

mu    = float(input("Media (mu): "))
sigma = float(input("Desvío estándar (sigma): "))

x = np.linspace(mu - 4*sigma, mu + 4*sigma, 500)
y = [f(xi, mu, sigma) for xi in x]

plt.figure(figsize=(8, 4))
plt.plot(x, y, color='steelblue', linewidth=2, label='f(x)')
plt.axvline(mu, color='red', linestyle='--', label=f'μ = {mu}')
plt.axvline(mu - sigma, color='green', linestyle=':', label=f'μ ± σ = {mu-sigma:.2f}, {mu+sigma:.2f}')
plt.axvline(mu + sigma, color='green', linestyle=':')
plt.axvline(mu - 2*sigma, color='orange', linestyle=':', label=f'μ ± 2σ = {mu-2*sigma:.2f}, {mu+2*sigma:.2f}')
plt.axvline(mu + 2*sigma, color='orange', linestyle=':')
plt.fill_between(x, y, alpha=0.1, color='steelblue')
plt.title(f'Función de densidad Normal(μ={mu}, σ={sigma})')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.tight_layout()
plt.savefig('normal_densidad.png', dpi=150, bbox_inches='tight')
plt.show()