import networkx as nx
import pandas as pd
import sys

"""
Métricas necessárias
- Grau médio
- Densidade
- Distância média
- Diâmetro
- Clusterização global
"""

try:
    fh = open("./exercicio_metricas/networks/www.edgelist.txt", "rb")
    www_network = nx.read_edgelist(fh)
    fh.close()
except FileNotFoundError:
    print("Erro: Arquivo 'www.edgelist.txt' não encontrado.")
    sys.exit()

metricas = {}

metricas['Nós'] = www_network.number_of_nodes()
metricas['Arestas'] = www_network.number_of_edges()
metricas['Grau Médio'] = (2 * metricas['Arestas']) / metricas['Nós'] if metricas['Nós'] > 0 else 0
metricas['Densidade'] = nx.density(www_network)
metricas['Clusterização Global (Transitivity)'] = nx.transitivity(www_network)
metricas['Clusterização Média (Average)'] = nx.average_clustering(www_network)


# Aqui é o cálculo das distâncias. Não tive muito tempo de testar porque demora bastante para ser calculado
"""if nx.is_connected(www_network):
    print("A rede é conectada. Calculando métricas de distância na rede inteira...")
    G_para_distancia = www_network
    metricas['Componentes Conectados'] = 1
else:
    print("A rede é desconectada. Usando o maior componente conectado para métricas de distância.")
    metricas['Componentes Conectados'] = nx.number_connected_components(www_network)
    componentes = nx.connected_components(www_network)
    maior_componente = max(componentes, key=len)
    G_para_distancia = www_network.subgraph(maior_componente)
    print(f"Maior componente tem {G_para_distancia.number_of_nodes()} nós.")

try:
    metricas['Distância Média'] = nx.average_shortest_path_length(G_para_distancia)
    metricas['Diâmetro'] = nx.diameter(G_para_distancia)
except nx.NetworkXError as e:
    print(f"Não foi possível calcular métricas de distância: {e}")
    metricas['Distância Média'] = "N/A"
    metricas['Diâmetro'] = "N/A"
"""

df_metricas = pd.DataFrame.from_dict(metricas, orient='index', columns=['Valor'])

df_metricas.index.name = 'Métrica'

df_metricas['Valor'] = df_metricas['Valor'].apply(lambda x: round(x, 4) if isinstance(x, float) else x)

# Imprime a tabela
print("\n" + "="*40)
print("      Tabela de Métricas da Rede WWW")
print("="*40)
print(df_metricas.to_string())
print("="*40)