import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import os

n_C = 10000
n_B = 1000
n_A = 100
m = 4

rede_A = nx.barabasi_albert_graph(n_A, m, seed=42) # Usar seed para reprodutibilidade
rede_B = nx.barabasi_albert_graph(n_B, m, seed=42)
rede_C = nx.barabasi_albert_graph(n_C, m, seed=42)

top_20_A = sorted(rede_A.degree(), key=lambda item: item[1], reverse=True)[:20]
top_20_B = sorted(rede_B.degree(), key=lambda item: item[1], reverse=True)[:20]
top_20_C = sorted(rede_C.degree(), key=lambda item: item[1], reverse=True)[:20]

df_A = pd.DataFrame(top_20_A, columns=[f'Nó (N={n_A})   ', f'Grau (N={n_A})   '])
df_B = pd.DataFrame(top_20_B, columns=[f'Nó (N={n_B})   ', f'Grau (N={n_B})   '])
df_C = pd.DataFrame(top_20_C, columns=[f'Nó (N={n_C})   ', f'Grau (N={n_C})   '])

df_comparacao = pd.concat([df_A, df_B, df_C], axis=1)

print("--- Comparação dos 20 Vértices com Maior Grau ---")
print(df_comparacao.to_string())

max_grau_A = top_20_A[0][1]
max_grau_B = top_20_B[0][1]
max_grau_C = top_20_C[0][1]

razoes_A = [max_grau_A / grau for no, grau in top_20_A[1:]]
razoes_B = [max_grau_B / grau for no, grau in top_20_B[1:]]
razoes_C = [max_grau_C / grau for no, grau in top_20_C[1:]]

ranks = range(2, 21)

plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(12, 8))

ax.plot(ranks, razoes_A, 'o-', label=f'N={n_A}')
ax.plot(ranks, razoes_B, 's-', label=f'N={n_B}')
ax.plot(ranks, razoes_C, '^-', label=f'N={n_C}')

ax.set_title('Razão entre o Maior Grau (Rank 1) e os Seguintes', fontsize=16)
ax.set_xlabel('Rank do Vértice (2 a 20)', fontsize=12)
ax.set_ylabel('Razão (Grau_Máximo / Grau_do_Rank)', fontsize=12)
ax.set_xticks(ranks)
ax.legend()

fig.tight_layout()

output_dir = './barabasi_albert_model'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
plt.savefig(os.path.join(output_dir, '20_vertices.png'), dpi=300)
plt.show()