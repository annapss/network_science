import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import os
from collections import Counter

def calcular_ccdf(graus_rede):
    """Calcula a Distribuição Cumulativa Complementar de Grau (CCDF)."""
    contagem_graus = Counter(graus_rede)
    grau_min = min(contagem_graus.keys())
    grau_max = max(contagem_graus.keys())
    
    contagens = np.zeros(grau_max + 1)
    for grau, contagem in contagem_graus.items():
        contagens[grau] = contagem
        
    ccdf = np.cumsum(contagens[::-1])[::-1]
    total_vertices = len(graus_rede)
    ccdf_normalizada = ccdf / total_vertices
    
    graus_existentes = sorted(contagem_graus.keys())
    return graus_existentes, ccdf_normalizada[graus_existentes]


n_C = 10000
n_B = 1000
n_A = 100
m = 4

rede_A = nx.barabasi_albert_graph(n_A, m)
rede_B = nx.barabasi_albert_graph(n_B, m)
rede_C = nx.barabasi_albert_graph(n_C, m)

graus_A = [d for n, d in rede_A.degree()]
graus_B = [d for n, d in rede_B.degree()]
graus_C = [d for n, d in rede_C.degree()]


k_A, ccdf_A = calcular_ccdf(graus_A)
k_B, ccdf_B = calcular_ccdf(graus_B)
k_C, ccdf_C = calcular_ccdf(graus_C)

fig = plt.figure("CCDF das Redes BA", figsize=(10, 8))
ax = fig.add_subplot()

ax.loglog(k_A, ccdf_A, "bo", markersize=5, alpha=0.7, label=f"N={n_A} vértices")
ax.loglog(k_B, ccdf_B, "gs", markersize=5, alpha=0.7, label=f"N={n_B} vértices")
ax.loglog(k_C, ccdf_C, "r^", markersize=5, alpha=0.7, label=f"N={n_C} vértices")

ax.set_title("Distribuição Cumulativa Complementar de Grau (CCDF)")
ax.set_ylabel("Probabilidade P(Grau ≥ k)")
ax.set_xlabel("Grau (k)")
ax.legend()
ax.grid(True, which="both", linestyle='--', linewidth=0.5)

fig.tight_layout()
output_dir = './barabasi_albert_model'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
plt.savefig(os.path.join(output_dir, 'distribuicao_cumulativa_complementar_grau_barabasi_albert.png'), dpi=300)
plt.show()