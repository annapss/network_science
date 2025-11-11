import pandas as pd
from thefuzz import fuzz  # Biblioteca para similaridade de string
import itertools
import sys
# Removidas as importações de networkx e matplotlib

# --- 1. DEFINIÇÃO DOS FILTROS ---
# (Baseado no seu arquivo script_v2.py)
ano_inicio = 2019
ano_fim = 2021
siglas_desejadas = [
    'CTD', 'CTIC', 'SEMISH', 'WEI', 'WIT', 'BraSNAm', 'ETC', 
    'ENCompIF', 'WASHES', 'WPerformance', 'SBCUP'
]
limite_similaridade = 90 # Similaridade de 90%

# --- Início do Script ---
print("Iniciando processamento da rede de coautoria COM FILTROS...")
print(f"Filtros: Anos == {ano_inicio} a {ano_fim}, Siglas == {siglas_desejadas}")

# Carregar o arquivo CSV
# ATENÇÃO: O caminho do arquivo é o do seu script. Verifique se está correto!
file_path = 'trabalho_final/dados/autoresSBC_en.csv' 
try:
    df = pd.read_csv(file_path, delimiter='|')

    # --- 2. Filtrar dados ---
    print(f"Tamanho original do DataFrame: {len(df)}")
    
    # Filtros básicos
    df_filtrado = df[df['Gênero'] != 'Desconhecido'].copy()
    df_filtrado.dropna(subset=['Autores', 'Titulo'], inplace=True)
    print(f"Tamanho após filtros básicos (Gênero, Nulos): {len(df_filtrado)}")
    
    # === NOVOS FILTROS ===
    # Filtrar pelo Ano 
    df_filtrado = df_filtrado[(df_filtrado['Ano'] >= ano_inicio) & (df_filtrado['Ano'] <= ano_fim)]
    print(f"Tamanho após filtrar 'Ano entre {ano_inicio} e {ano_fim}': {len(df_filtrado)}")

    # Filtrar pela lista de Siglas
    df_filtrado = df_filtrado[df_filtrado['Sigla'].isin(siglas_desejadas)]
    print(f"Tamanho após filtrar pela lista de Siglas: {len(df_filtrado)}")
    # === FIM DOS NOVOS FILTROS ===

    # --- 3. Preparar para Desambiguação ---
    autores_unicos = df_filtrado['Autores'].unique()
    autores_unicos.sort()
    print(f"Número de nomes de autores únicos (antes da desambiguação): {len(autores_unicos)}")

    # --- 4. Desambiguação (Agrupamento) de Autores ---
    print("Iniciando processo de desambiguação de nomes...")
    
    mapeamento_nomes = {}
    nomes_canonicos = []

    total_autores = len(autores_unicos)
    for i, nome in enumerate(autores_unicos):
        if i % 1000 == 0 and i > 0:
            print(f"Processando autor {i} de {total_autores}...")
            
        if nome in mapeamento_nomes:
            continue

        match_encontrado = False
        for canonico in nomes_canonicos:
            similaridade = fuzz.ratio(nome, canonico) 
            
            if similaridade > limite_similaridade:
                mapeamento_nomes[nome] = canonico
                match_encontrado = True
                break
        
        if not match_encontrado:
            nomes_canonicos.append(nome)
            mapeamento_nomes[nome] = nome

    print("Desambiguação concluída.")
    print(f"Número de autores únicos (nós) após desambiguação: {len(nomes_canonicos)}")

    # Salvar o mapeamento em um CSV para auditoria
    mapeamento_file = 'trabalho_final/similaridade_nome_autores/mapeamento_autores_filtrado_' + str(ano_inicio) + '-' + str(ano_fim) + '.csv'
    df_mapeamento = pd.DataFrame(list(mapeamento_nomes.items()), columns=['Nome_Original', 'Nome_Canonico'])
    df_mapeamento_alterados = df_mapeamento[df_mapeamento['Nome_Original'] != df_mapeamento['Nome_Canonico']].copy()
    df_mapeamento_alterados.sort_values(by=['Nome_Canonico', 'Nome_Original'], inplace=True)
    df_mapeamento_alterados.to_csv(mapeamento_file, index=False)
    print(f"Mapeamento de nomes salvo em: {mapeamento_file}")

    # --- 5. Aplicar Mapeamento ---
    print("Aplicando mapeamento de nomes ao DataFrame...")
    df_filtrado['Autor_Canonico'] = df_filtrado['Autores'].map(mapeamento_nomes)
    
    # --- 6. Criar Mapa de Gênero ---
    # Cria um dicionário (Series) mapeando cada autor canônico ao seu gênero
    print("Criando mapa de Gênero por autor canônico...")
    genero_map = df_filtrado.drop_duplicates('Autor_Canonico').set_index('Autor_Canonico')['Gênero']

    # --- 7. Construir e Salvar a Lista de Arestas por Evento ---
    print("Construindo lista de arestas por evento...")
    
    artigos_agrupados = df_filtrado.groupby(['Titulo', 'Ano', 'Sigla'])
    
    print(f"Número de artigos únicos (após filtros): {len(artigos_agrupados)}")
    
    arestas = [] # Lista para salvar (Autor1, Autor2, Evento)
    
    for (titulo, ano, sigla_evento), group in artigos_agrupados:
        autores_do_artigo = list(group['Autor_Canonico'])
        autores_unicos_artigo = sorted(list(set(autores_do_artigo)))
        
        if len(autores_unicos_artigo) > 1:
            combinacoes = itertools.combinations(autores_unicos_artigo, 2)
            for coautoria in combinacoes:
                arestas.append((coautoria[0], coautoria[1], sigla_evento))

    print(f"Número total de arestas de coautoria (ocorrências) encontradas: {len(arestas)}")

    # --- 8. Criar e Salvar DataFrame de Arestas (com Gênero) ---
    arestas_file = 'trabalho_final/edge_list/arestas_por_evento_com_genero_' + str(ano_inicio) + '-' + str(ano_fim) + '.csv'
    
    if not arestas:
         print("Nenhuma aresta encontrada. O arquivo CSV de arestas estará vazio.")
         # Salva um CSV vazio com os novos cabeçalhos
         pd.DataFrame(columns=['Autor1', 'Gênero_Autor1', 'Autor2', 'Gênero_Autor2', 'Evento']).to_csv(arestas_file, index=False)
    else:
        print("Adicionando dados de gênero ao arquivo de arestas...")
        # Criar o DataFrame com as colunas básicas
        df_arestas = pd.DataFrame(arestas, columns=['Autor1', 'Autor2', 'Evento'])
        
        # Usar o mapa de gênero para adicionar as novas colunas
        df_arestas['Gênero_Autor1'] = df_arestas['Autor1'].map(genero_map)
        df_arestas['Gênero_Autor2'] = df_arestas['Autor2'].map(genero_map)
        
        # Reordenar colunas para melhor leitura
        df_arestas = df_arestas[['Autor1', 'Gênero_Autor1', 'Autor2', 'Gênero_Autor2', 'Evento']]
        
        # Salvar o DataFrame final
        df_arestas.to_csv(arestas_file, index=False)
        print(f"Lista de arestas com gênero salva em: {arestas_file}")
    
    # --- Fim do Script (removida parte de NetworkX/Plot) ---

    print("\n--- Processamento Concluído. Lista de arestas por evento (com gênero) salva! ---")

except FileNotFoundError:
    print(f"Erro: Arquivo '{file_path}' não encontrado.")
    print("Por favor, verifique se o caminho 'trabalho_final/dados/autoresSBC_en.csv' está correto.")
except ImportError:
    print("\nERRO: Biblioteca 'thefuzz' não encontrada.")
    print("Por favor, instale-a usando: pip install python-thefuzz")
except Exception as e:
    print(f"Ocorreu um erro durante o processamento: {e}")