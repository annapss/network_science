import pandas as pd
from thefuzz import fuzz  # Biblioteca para similaridade de string
import itertools
import networkx as nx
import matplotlib.pyplot as plt
import sys

    # --- AQUI COMEÇA A MUDANÇA ---
ano_inicio = 2019
ano_fim = 2021

arestas_file = 'trabalho_final/edge_list/arestas_com_genero_e_peso_' + str(ano_inicio) + '-' + str(ano_fim) + '.csv'

df_arestas = pd.read_csv(arestas_file)

print("Criando o grafo com NetworkX...")
rede_csbc = nx.Graph()
    
df_arestas_ponderadas_nx = pd.read_csv(arestas_file) # Recarregar para garantir
for _, row in df_arestas_ponderadas_nx.iterrows():
    rede_csbc.add_edge(row['Autor1'], row['Autor2'], weight=row['Peso'])
    rede_csbc.nodes[row['Autor1']].update({'Gênero': row['Gênero_Autor1']})
    rede_csbc.nodes[row['Autor2']].update({'Gênero': row['Gênero_Autor2']})

# 1. Crie um mapa de cores
print("Criando mapa de cores para o plot...")

# Dicionário de cores
mapa_cores_genero = {
    'Homem': '#1f77b4',  # Azul
    'Mulher': '#ff7f0e', # Laranja
    'Desconhecido': '#7f7f7f' # Cinza (Default)
}

color_map = []
# rede_csbc.nodes(data=True) permite acessar o nó e seus dados (incluindo Gênero)
for node, data in rede_csbc.nodes(data=True):
    genero = data.get('Gênero', 'Desconhecido') # Usar .get() é mais seguro
    cor = mapa_cores_genero.get(genero, '#7f7f7f') # Pega a cor ou usa cinza
    color_map.append(cor)

# 2. Desenhe o grafo usando o mapa de cores
if not rede_csbc.nodes():
    print("Grafo está vazio. Não há nada para desenhar.")
else:
    print(f"Desenhando o grafo com {rede_csbc.number_of_nodes()} nós... (Isso pode ser MUITO lento)")
    
    # O layout Spring é computacionalmente caro. 
    # Para grafos grandes, considere o 'random_layout' ou 'circular_layout'
    # pos = nx.random_layout(rede_csbc) 
    
    nx.draw(rede_csbc, 
            node_color=color_map,  # <-- Aqui você passa a lista de cores
            with_labels=False,     # 'True' vai travar seu PC
            node_size=10,          # Nós bem pequenos
            width=0.1,             # Arestas bem finas
            # pos=pos              # Descomente se usar um layout pré-calculado
            )
        
    # Adicionar uma legenda (opcional, mas recomendado)
    # Criamos 'patches' falsos para a legenda
    import matplotlib.patches as mpatches
    legend_patches = [
        mpatches.Patch(color=mapa_cores_genero['Homem'], label='Homem'),
        mpatches.Patch(color=mapa_cores_genero['Mulher'], label='Mulher'),
        mpatches.Patch(color=mapa_cores_genero['Desconhecido'], label='Desconhecido/N/A')
    ]
    plt.legend(handles=legend_patches)

    plt.show() # Mostra o plot

print("\n--- Processamento Concluído. Lista de arestas por evento salva! ---")