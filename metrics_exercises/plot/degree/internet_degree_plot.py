import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

fh = open("./exercicio_metricas/networks/internet.edgelist.txt", "rb")
internet_network = nx.read_edgelist(fh)

degree_sequence = sorted((d for n, d in internet_network.degree()), reverse=True)
dmax = max(degree_sequence)

fig = plt.figure("Degree of Internet Network", figsize=(8, 8))
axgrid = fig.add_gridspec(5, 4)

ax1 = fig.add_subplot(axgrid[3:, :2])
ax1.plot(degree_sequence, "b-", marker="o")
ax1.set_title("Degree Rank Plot")
ax1.set_ylabel("Degree")
ax1.set_xlabel("Rank")

fig.tight_layout()
plt.show()