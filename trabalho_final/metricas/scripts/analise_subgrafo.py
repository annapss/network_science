import pandas as pd
import networkx as nx
import sys
import matplotlib.pyplot as plt
import community as community_louvain 
import numpy as np
import os

def analisar_subgrafo(ano_inicio, ano_fim, sigla_evento=None):
    
    periodo_pasta = f'{ano_inicio}-{ano_fim}'
    
    if sigla_evento:
        file_name = f'arestas_com_genero_e_peso_{sigla_evento}_{ano_inicio}-{ano_fim}.csv'
        arestas_file = os.path.join('trabalho_final', 'edge_list', 'por_evento', file_name)
        prefixo_saida = sigla_evento
        print(f"\n{'='*70}\nINICIANDO ANÁLISE DO EVENTO: {sigla_evento}\n{'='*70}")
    else:
        file_name = f'arestas_com_genero_e_peso_{ano_inicio}-{ano_fim}.csv'
        arestas_file = os.path.join('trabalho_final', 'edge_list', file_name)
        prefixo_saida = 'total'
        print(f"\n{'='*70}\nINICIANDO ANÁLISE DA REDE TOTAL\n{'='*70}")

    try:
        df_arestas = pd.read_csv(arestas_file)
    except FileNotFoundError:
        print(f"AVISO: Arquivo '{arestas_file}' não encontrado. Pulando análise.")
        return
    except pd.errors.EmptyDataError:
        print(f"AVISO: Arquivo '{arestas_file}' vazio. Pulando análise.")
        return

    print("Criando o grafo com NetworkX...")
    rede_csbc = nx.Graph()
    if df_arestas.empty:
        print("Grafo vazio.")
        return
        
    for _, row in df_arestas.iterrows():
        rede_csbc.add_edge(row['Autor1'], row['Autor2'], weight=row['Peso'])
        rede_csbc.nodes[row['Autor1']].update({'Gênero': row['Gênero_Autor1']})
        rede_csbc.nodes[row['Autor2']].update({'Gênero': row['Gênero_Autor2']})

    print(f"Grafo criado. Nós: {rede_csbc.number_of_nodes()}, Arestas: {rede_csbc.number_of_edges()}")

    print("Iniciando o cálculo das métricas GLOBAIS...")
    metricas = {}

    metricas['Nós'] = rede_csbc.number_of_nodes()
    
    generos_nodes = nx.get_node_attributes(rede_csbc, 'Gênero')
    if generos_nodes:
        contagem_genero = pd.Series(generos_nodes).value_counts()
        metricas['Nós (Homens)'] = contagem_genero.get('Homem', 0)
        metricas['Nós (Mulheres)'] = contagem_genero.get('Mulher', 0)
        print(f"Contagem de Gênero: H={metricas['Nós (Homens)']}, M={metricas['Nós (Mulheres)']}")
    else:
        metricas['Nós (Homens)'] = 0
        metricas['Nós (Mulheres)'] = 0

    metricas['Arestas'] = rede_csbc.number_of_edges()
    metricas['Grau Médio'] = (2 * metricas['Arestas']) / metricas['Nós'] if metricas['Nós'] > 0 else 0
    metricas['Densidade'] = nx.density(rede_csbc)    
    metricas['Clusterização Global (Transitivity)'] = nx.transitivity(rede_csbc)
    metricas['Clusterização Média (Average)'] = nx.average_clustering(rede_csbc)
    
    try:
        assortatividade = nx.attribute_assortativity_coefficient(rede_csbc, "Gênero")
        metricas['Assortatividade (Gênero)'] = assortatividade
        print(f"Assortatividade de Gênero calculada: {assortatividade:.4f}")
    except Exception as e:
        metricas['Assortatividade (Gênero)'] = "N/A"
        print(f"AVISO: Não foi possível calcular Assortatividade: {e}")
    
    if nx.is_connected(rede_csbc):
        G_para_distancia = rede_csbc
        metricas['Componentes Conectados'] = 1
        metricas['Nós (LCC)'] = rede_csbc.number_of_nodes()
    else:
        metricas['Componentes Conectados'] = nx.number_connected_components(rede_csbc)
        componentes = nx.connected_components(rede_csbc)
        maior_componente = max(componentes, key=len)
        G_para_distancia = rede_csbc.subgraph(maior_componente)
        metricas['Nós (LCC)'] = G_para_distancia.number_of_nodes()
        
    if metricas['Nós (LCC)'] > 1:
        try:
            metricas['Distância Média'] = nx.average_shortest_path_length(G_para_distancia)
            metricas['Diâmetro'] = nx.diameter(G_para_distancia)
        except nx.NetworkXError:
            metricas['Distância Média'] = "N/A"
            metricas['Diâmetro'] = "N/A"
    else:
        metricas['Distância Média'] = "N/A"
        metricas['Diâmetro'] = "N/A"

    if metricas['Nós (LCC)'] > 1:
        partition = community_louvain.best_partition(G_para_distancia, weight='weight')
        modularity = community_louvain.modularity(partition, G_para_distancia, weight='weight')
        metricas['Modularity'] = modularity
        metricas['Comunidades (Louvain)'] = len(set(partition.values()))

        community_map = {node: -1 for node in rede_csbc.nodes()}
        community_map.update(partition) 
        nx.set_node_attributes(rede_csbc, community_map, 'Comunidade')
    else:
        partition = {}
        metricas['Modularity'] = "N/A"
        metricas['Comunidades (Louvain)'] = 0

    base_metricas_dir = os.path.join('trabalho_final', 'metricas', periodo_pasta)
    os.makedirs(base_metricas_dir, exist_ok=True)
    
    comunidades_output_dir = os.path.join('trabalho_final', 'metricas', 'comunidades', periodo_pasta)
    os.makedirs(comunidades_output_dir, exist_ok=True)
    
    centralidades_output_dir = os.path.join('trabalho_final', 'metricas', 'centralidades', periodo_pasta)
    os.makedirs(centralidades_output_dir, exist_ok=True)
    
    df_metricas = pd.DataFrame.from_dict(metricas, orient='index', columns=['Valor'])
    df_metricas.index.name = 'Métrica'
    df_metricas['Valor'] = df_metricas['Valor'].apply(lambda x: round(x, 4) if isinstance(x, float) else x)
    
    metricas_file = os.path.join(base_metricas_dir, f'metricas_globais_{prefixo_saida}.csv')
    
    df_metricas.to_csv(metricas_file, header=True)
    print(f"Métricas Globais salvas em: {metricas_file}")
    
    if partition:
        df_comunidades = pd.DataFrame(list(partition.items()), columns=['Autor', 'Comunidade_ID'])
        generos = nx.get_node_attributes(rede_csbc, 'Gênero')
        df_comunidades['Gênero'] = df_comunidades['Autor'].map(generos)
        
        if not sigla_evento:
            raw_members_file = os.path.join(comunidades_output_dir, f'membros_comunidade_bruta_{prefixo_saida}.csv')
            df_comunidades.to_csv(raw_members_file, index=False)
            print(f"Lista de membros da comunidade bruta salva em: {raw_members_file}")

        df_genero_comunidade = df_comunidades.pivot_table(index='Comunidade_ID', columns='Gênero', aggfunc='size', fill_value=0)
        df_genero_comunidade['Total_Comunidade'] = df_genero_comunidade.sum(axis=1)
            
        if 'Desconhecido' in df_genero_comunidade.columns:
            df_genero_comunidade.drop(columns=['Desconhecido'], inplace=True)
            df_genero_comunidade['Total_Comunidade'] = df_genero_comunidade.sum(axis=1)
            
        genero_comunidade_file = os.path.join(comunidades_output_dir, f'contagem_genero_comunidade_{prefixo_saida}.csv')
        
        df_genero_comunidade.to_csv(genero_comunidade_file)
        print(f"Tabela Gênero/Comunidade salva em: {genero_comunidade_file}")

    if rede_csbc.number_of_nodes() > 0:
        centralidade_grau = nx.degree_centrality(rede_csbc)
        df_centralidade = pd.DataFrame({'Grau (Centralidade)': pd.Series(centralidade_grau)})
        df_centralidade.index.name = 'Autor'
        
        num_nos_total = rede_csbc.number_of_nodes()
        num_top_10_percent = max(1, int(num_nos_total * 0.10)) 

        df_top_centralidade = df_centralidade.sort_values(
            by='Grau (Centralidade)', 
            ascending=False
        ).head(num_top_10_percent)
        
        generos_nodes = nx.get_node_attributes(rede_csbc, 'Gênero')
        df_top_centralidade['Gênero'] = df_top_centralidade.index.map(generos_nodes)
        
        df_top_centralidade = df_top_centralidade.round(4)
        
        centralidade_file = os.path.join(centralidades_output_dir, f'centralidades_autores_{prefixo_saida}.csv')
        
        df_top_centralidade.to_csv(centralidade_file)
        print(f"Tabela de Centralidades (Top {num_top_10_percent} autores) salva em: {centralidade_file}")

    print(f"\n--- Análise do Subgrafo {prefixo_saida} Concluída. ---")

def criar_diretorios():
    try:
        os.makedirs('trabalho_final/metricas', exist_ok=True)
        os.makedirs('trabalho_final/metricas/comunidades', exist_ok=True)
        os.makedirs('trabalho_final/metricas/centralidades', exist_ok=True)
        os.makedirs('trabalho_final/visualizacao', exist_ok=True)
        os.makedirs('trabalho_final/edge_list/por_evento', exist_ok=True)
    except Exception as e:
        print(f"ERRO DE DIRETÓRIO: Não foi possível criar os diretórios de saída: {e}")
        sys.exit(1)