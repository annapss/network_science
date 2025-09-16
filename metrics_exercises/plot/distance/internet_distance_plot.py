import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Esse aqui não deu tempo de rodar, mas a complexidade dele é O(N * (N + M)). Dei uma pesquisada e talvez usar o graph tool poderia ajudar, já que no fundo ele tinha usa C/C++
fh = open("./exercicio_metricas/networks/internet.edgelist.txt", "rb")
internet_network = nx.read_edgelist(fh)

degrees = dict(internet_network.degree())

avg_path_lengths = {}
nodes = list(internet_network.nodes())

for node in nodes:
    path_lengths = nx.single_source_shortest_path_length(internet_network, node)

    reachable_nodes = len(path_lengths)
    
    if reachable_nodes > 1:
        total_path_length = sum(path_lengths.values())
        avg_path_lengths[node] = total_path_length / (reachable_nodes - 1)
    else:
        avg_path_lengths[node] = 0

degree_values = [degrees[node] for node in nodes]
avg_path_values = [avg_path_lengths[node] for node in nodes]

plt.style.use('default')
plt.figure(figsize=(10, 7))

plt.scatter(degree_values, avg_path_values, c='blue', s=25, alpha=0.7)

plt.xscale('log')

plt.title('Distância Média vs. Grau do Nó', fontsize=16)
plt.xlabel('Grau (k)', fontsize=14)
plt.ylabel('Distância Média', fontsize=14)

plt.grid(True, which="both", ls="--", linewidth=0.5)

plt.show()