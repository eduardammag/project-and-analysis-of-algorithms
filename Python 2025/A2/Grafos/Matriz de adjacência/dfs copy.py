import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, t

# --- Configurações básicas ---
c = 1.63
x = np.linspace(-4, 4, 1000)
pdf_norm = norm.pdf(x)
pdf_t5 = t.pdf(x, df=5)

# --- Áreas centrais ---
A_norm = norm.cdf(c) - norm.cdf(-c)
A_t5 = t.cdf(c, df=5) - t.cdf(-c, df=5)
Delta = A_norm - A_t5

# --- Máscaras ---
mask_center = (x >= -c) & (x <= c)
mask_left = (x < -c)
mask_right = (x > c)

# --- Gráfico único ---
plt.figure(figsize=(12,7))
plt.title(
    f"Comparação das distribuições Normal(0,1) e t(5)\n"
    f"Área entre -{c} e {c}: Normal = {A_norm:.4f},  t(5) = {A_t5:.4f},  Diferença Δ = {Delta:.4f}",
    fontsize=13, pad=15
)

# Curvas de densidade
plt.plot(x, pdf_norm, color='blue', label='Normal(0,1)', linewidth=2)
plt.plot(x, pdf_t5, color='orange', linestyle='--', label='t(5)', linewidth=2)

# --- Áreas sombreadas ---
# 1️⃣ Centro: Normal tem densidade maior
plt.fill_between(x[mask_center], pdf_norm[mask_center], pdf_t5[mask_center],
                 where=(pdf_norm[mask_center] >= pdf_t5[mask_center]),
                 color='blue', alpha=0.3, label='Centro: Normal > t(5)')

# 2️⃣ Caudas: t(5) tem densidade maior
plt.fill_between(x[mask_left], pdf_t5[mask_left], pdf_norm[mask_left],
                 where=(pdf_t5[mask_left] >= pdf_norm[mask_left]),
                 color='orange', alpha=0.3, label='Caudas: t(5) > Normal')
plt.fill_between(x[mask_right], pdf_t5[mask_right], pdf_norm[mask_right],
                 where=(pdf_t5[mask_right] >= pdf_norm[mask_right]),
                 color='orange', alpha=0.3)

# Linhas de referência
plt.axvline(-c, color='gray', linestyle=':')
plt.axvline(c, color='gray', linestyle=':')
plt.axhline(0, color='black', linewidth=0.8)

# Eixos e legenda
plt.xlabel("x", fontsize=12)
plt.ylabel("Densidade", fontsize=12)
plt.legend(fontsize=11, loc='upper center', ncol=2, frameon=True)
plt.grid(alpha=0.3)

# Texto explicativo no gráfico
plt.text(0, 0.35, "Normal domina no centro", color='blue', fontsize=11, ha='center')
plt.text(2.7, 0.1, "t(5) domina nas caudas", color='orange', fontsize=11, ha='center')

plt.show()
