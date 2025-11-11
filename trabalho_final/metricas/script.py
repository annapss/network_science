import pandas as pd
import networkx as nx
import sys
import matplotlib.pyplot as plt

# As importações do fuzz e itertools não são usadas neste script
# import pandas as pd
# from thefuzz import fuzz  # Biblioteca para similaridade de string
# import itertools

ano_inicio = 2019
ano_fim = 2021

arestas_file = 'trabalho_final/edge_list/arestas_com_genero_e_peso_' + str(ano_inicio) + '-' + str(ano_fim) + '.csv'

try:
    df_arestas = pd.read_csv(arestas_file)

    print("Criando o grafo com NetworkX...")
    rede_csbc = nx.Graph()
        
    for _, row in df_arestas.iterrows():
        rede_csbc.add_edge(row['Autor1'], row['Autor2'], weight=row['Peso'])
        
        # --- CORREÇÃO IMPORTANTE ---
        # O nome do atributo deve ser 'Gênero', e não 'attribute'
        rede_csbc.nodes[row['Autor1']].update({'Gênero': row['Gênero_Autor1']})
        rede_csbc.nodes[row['Autor2']].update({'Gênero': row['Gênero_Autor2']})

    print(f"Grafo criado. Número de nós: {rede_csbc.number_of_nodes()}, Número de arestas: {rede_csbc.number_of_edges()}")

    # --- 1. Coleta de Métricas GLOBAIS ---

    print("Iniciando o cálculo das métricas GLOBAIS...")
    metricas = {}

    metricas['Nós'] = rede_csbc.number_of_nodes()
    metricas['Arestas'] = rede_csbc.number_of_edges()
    metricas['Grau Médio'] = (2 * metricas['Arestas']) / metricas['Nós'] if metricas['Nós'] > 0 else 0
    metricas['Densidade'] = nx.density(rede_csbc)
    
    # Removida a centralidade de 'metricas'
    
    metricas['Clusterização Global (Transitivity)'] = nx.transitivity(rede_csbc)
    metricas['Clusterização Média (Average)'] = nx.average_clustering(rede_csbc)

    if nx.is_connected(rede_csbc):
        print("A rede é conectada. Calculando métricas de distância na rede inteira...")
        G_para_distancia = rede_csbc
        metricas['Componentes Conectados'] = 1
    else:
        print("A rede é desconectada. Usando o maior componente conectado para métricas de distância.")
        metricas['Componentes Conectados'] = nx.number_connected_components(rede_csbc)
        componentes = nx.connected_components(rede_csbc)
        maior_componente = max(componentes, key=len)
        G_para_distancia = rede_csbc.subgraph(maior_componente)
        print(f"Maior componente tem {G_para_distancia.number_of_nodes()} nós.")

    try:
        metricas['Distância Média'] = nx.average_shortest_path_length(G_para_distancia)
        metricas['Diâmetro'] = nx.diameter(G_para_distancia)
    except nx.NetworkXError as e:
        print(f"Não foi possível calcular métricas de distância: {e}")
        metricas['Distância Média'] = "N/A"
        metricas['Diâmetro'] = "N/A"

    print("Cálculo de métricas globais finalizado.")

    # --- 2. Exibição da Tabela de Métricas GLOBAIS ---
    df_metricas = pd.DataFrame.from_dict(metricas, orient='index', columns=['Valor'])
    df_metricas.index.name = 'Métrica'
    df_metricas['Valor'] = df_metricas['Valor'].apply(lambda x: round(x, 4) if isinstance(x, float) else x)

    print("\n" + "="*40)
    print("      Tabela de Métricas Globais da Rede")
    print("="*40)
    print(df_metricas.to_string())
    print("="*40)


    # --- 3. CÁLCULO E EXIBIÇÃO DAS CENTRALIDADES (NOVA SEÇÃO) ---
    
    print("\nIniciando o cálculo das CENTRALIDADES (Top 10)...")
    
    # Calcular as centralidades (usando peso quando apropriado)
    centralidade_grau = nx.degree_centrality(rede_csbc)
    centralidade_grau_ponderado = dict(rede_csbc.degree(weight='weight')) # Grau ponderado (soma dos pesos)
    
    # Eigenvector pode não convergir em redes desconectadas, rodar no maior componente
    try:
        centralidade_autovetor = nx.eigenvector_centrality(G_para_distancia, weight='weight')
    except Exception as e:
        print(f"Não foi possível calcular Eigenvector: {e}. Usando 'None'.")
        centralidade_autovetor = {node: None for node in rede_csbc.nodes()}
        
    # Coletar Gêneros
    generos = nx.get_node_attributes(rede_csbc, 'Gênero')

    # Criar um DataFrame com os resultados
    df_centralidade = pd.DataFrame({
        'Gênero': pd.Series(generos),
        'Grau (Centralidade)': pd.Series(centralidade_grau),
        'Grau Ponderado (Força)': pd.Series(centralidade_grau_ponderado)
    })

    # Substituir valores ausentes (de componentes menores) por 0 ou N/A
    df_centralidade.fillna(0, inplace=True) # ou use .fillna('N/A')
    
    # Definir o nome do índice
    df_centralidade.index.name = 'Autor'

    # Arredondar para 4 casas decimais
    df_centralidade = df_centralidade.round(4)
    
    # --- 4. Exibição Legível das Centralidades ---
    

    # Imprimir os 10 mais centrais por Grau Ponderado (Força)
    print("\n" + "="*70)
    print("        Top 10 Autores por Força (Grau Ponderado)")
    print("="*70)
    print(df_centralidade.sort_values(by='Grau Ponderado (Força)', ascending=False).head(10).to_string())
    print("="*70)

    # Salvar o DataFrame de centralidade COMPLETO em um CSV
    centralidade_file = 'trabalho_final/metricas/centralidades/centralidades_autores_' + str(ano_inicio) + '-' + str(ano_fim) + '.csv'
    df_centralidade.to_csv(centralidade_file)
    print(f"\nDataFrame completo de centralidades salvo em: {centralidade_file}")
    
    print("\n--- Processamento Concluído. ---")

except FileNotFoundError:
    print(f"Erro: Arquivo '{arestas_file}' não encontrado.")
    print("Por favor, verifique se o caminho está correto.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")