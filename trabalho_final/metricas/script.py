import pandas as pd
from thefuzz import fuzz  # Biblioteca para similaridade de string
import itertools
import networkx as nx
import sys
import matplotlib.pyplot as plt

ano_inicio = 2019
ano_fim = 2021

arquivo_edgelist = 'trabalho_final/edge_list/arestas_por_evento_filtrada_'  + str(ano_inicio) + '-' + str(ano_fim) + '.csv'
df_arestas = pd.read_csv(arquivo_edgelist)

rede_csbc = nx.from_pandas_edgelist(
        df_arestas, 
        source='Autor1',         # Coluna para o nó de origem
        target='Autor2',         # Coluna para o nó de destino
        edge_attr='Evento',      # Coluna para usar como atributo de aresta
        create_using=nx.MultiGraph()  # <-- A MÁGICA ACONTECE AQUI
    )

"""
Métricas necessárias
- Grau médio
- Densidade
- Distância média
- Diâmetro
- Clusterização global
"""

# --- 1. Coleta de Métricas ---

print("Iniciando o cálculo das métricas...")

# Dicionário para armazenar os resultados
metricas = {}

# Métricas que funcionam em qualquer grafo (conectado ou não)
metricas['Nós'] = rede_csbc.number_of_nodes()
metricas['Arestas'] = rede_csbc.number_of_edges()
metricas['Grau Médio'] = (2 * metricas['Arestas']) / metricas['Nós'] if metricas['Nós'] > 0 else 0
metricas['Densidade'] = nx.density(rede_csbc)

# O Networkx utiliza o calculo de clusterização de forma diferente da que aprendemos no caso de um multigraph. Então, vou avaliar se realmente o Multigraph é necessário

# Transitivity é a definição formal de clusterização global
#metricas['Clusterização Global (Transitivity)'] = nx.transitivity(rede_csbc)
# Average clustering é a média dos coeficientes de clusterização locais
#metricas['Clusterização Média (Average)'] = nx.average_clustering(rede_csbc)


# Métricas que dependem de caminhos (distância)
if nx.is_connected(rede_csbc):
    print("A rede é conectada. Calculando métricas de distância na rede inteira...")
    # Se a rede é conectada, usamos o grafo inteiro
    G_para_distancia = rede_csbc
    metricas['Componentes Conectados'] = 1
else:
    print("A rede é desconectada. Usando o maior componente conectado para métricas de distância.")
    # Pega o número de componentes
    metricas['Componentes Conectados'] = nx.number_connected_components(rede_csbc)
    # Encontra o maior componente conectado
    componentes = nx.connected_components(rede_csbc)
    maior_componente = max(componentes, key=len)
    # Cria um subgrafo contendo apenas o maior componente
    G_para_distancia = rede_csbc.subgraph(maior_componente)
    print(f"Maior componente tem {G_para_distancia.number_of_nodes()} nós.")


# ATENÇÃO: Os cálculos de distância podem ser LENTOS para redes grandes
try:
    metricas['Distância Média'] = nx.average_shortest_path_length(G_para_distancia)
    metricas['Diâmetro'] = nx.diameter(G_para_distancia)
except nx.NetworkXError as e:
    print(f"Não foi possível calcular métricas de distância: {e}")
    metricas['Distância Média'] = "N/A"
    metricas['Diâmetro'] = "N/A"

print("Cálculo finalizado.")

# --- 2. Criação da Tabela com Pandas ---

# Criamos um DataFrame do Pandas a partir do dicionário.
# O orient='index' transforma as chaves do dicionário em linhas.
df_metricas = pd.DataFrame.from_dict(metricas, orient='index', columns=['Valor'])

# Ajustamos o nome da coluna do índice
df_metricas.index.name = 'Métrica'

# Arredondando os valores para melhor visualização
df_metricas['Valor'] = df_metricas['Valor'].apply(lambda x: round(x, 4) if isinstance(x, float) else x)


# --- 3. Exibição da Tabela ---
print("\n" + "="*40)
print("      Tabela de Métricas da Rede")
print("="*40)
print(df_metricas.to_string()) # .to_string() garante que a tabela inteira seja impressa
print("="*40)