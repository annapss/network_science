import networkx as nx
import matplotlib.pyplot as plt

fh = open("./exercicio_metricas/networks/www.edgelist.txt", "rb")
www_network = nx.read_edgelist(fh)

degrees = dict(www_network.degree())

clustering_coeffs = nx.clustering(www_network)

nodes = www_network.nodes()
degree_values = [degrees[node] for node in nodes]
clustering_values = [clustering_coeffs[node] for node in nodes]


plt.style.use('default')
plt.figure(figsize=(10, 7))

plt.scatter(degree_values, clustering_values, c='purple', s=25, alpha=0.7)

plt.xscale('log')
plt.yscale('log')

plt.title('Coeficiente de Clusterização vs. Grau do Nó', fontsize=16)
plt.xlabel('Grau (k)', fontsize=14)
plt.ylabel('Coeficiente de Clusterização C(k)', fontsize=14)

plt.grid(True, which="both", ls="--", linewidth=0.5)

plt.show()