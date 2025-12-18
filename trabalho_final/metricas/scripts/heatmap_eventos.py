import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

ANO_INICIO = 2019
ANO_FIM = 2023
PERIODO_PASTA = f'{ANO_INICIO}-{ANO_FIM}'

ARTIGOS_FILTRADOS_FILE = os.path.join(
    'trabalho_final', 'edge_list', f'artigos_eventos_por_autor_{PERIODO_PASTA}.csv'
)

COMUNIDADES_MEMBROS_FILE = os.path.join(
    'trabalho_final', 'metricas', 'comunidades', PERIODO_PASTA, 
    f'membros_comunidade_bruta_total.csv'
)
OUTPUT_HEATMAP_DIR = os.path.join('trabalho_final', 'visualizacao', PERIODO_PASTA)
OUTPUT_HEATMAP_FILE = os.path.join(OUTPUT_HEATMAP_DIR, f'heatmap_comunidade_vs_evento_{PERIODO_PASTA}.png')

def gerar_heatmap_cas():
    try:
        if not os.path.exists(COMUNIDADES_MEMBROS_FILE):
             print(f"ERRO: Arquivo de membros da comunidade não encontrado: {COMUNIDADES_MEMBROS_FILE}")
             print("Certifique-se de que 'analise_eventos.py' foi executado e que o 'analise_subgrafo.py' modificado salvou a lista bruta para a rede total.")
             return

        df_comunidades = pd.read_csv(COMUNIDADES_MEMBROS_FILE)
        print(f"Dados de comunidades carregados ({len(df_comunidades)} autores no LCC total).")

        if not os.path.exists(ARTIGOS_FILTRADOS_FILE):
             print(f"ERRO: Arquivo de artigos filtrados não encontrado: {ARTIGOS_FILTRADOS_FILE}")
             print("Execute o script 'gera_csv_genero_peso.py' com o período correto para gerar este arquivo.")
             return
             
        df_eventos = pd.read_csv(ARTIGOS_FILTRADOS_FILE)
        
        df_afiliacao_eventos = df_eventos.drop_duplicates(subset=['Autor_Canonico', 'Sigla'])
        df_afiliacao_eventos['Valor'] = 1
        
        df_afiliacao_eventos = df_afiliacao_eventos.pivot_table(
            index='Autor_Canonico', 
            columns='Sigla', 
            values='Valor', 
            fill_value=0
        )
        print("Matriz de afiliação Autor x Evento criada.")

        df_merge = df_comunidades.set_index('Autor').join(
            df_afiliacao_eventos.rename_axis('Autor')
        ).dropna(subset=['Comunidade_ID']).fillna(0)
        
        df_merge['Comunidade_ID'] = df_merge['Comunidade_ID'].astype(int)
        df_merge.drop(columns=['Gênero'], inplace=True)
        
        df_comunidade_evento = df_merge.groupby('Comunidade_ID').sum()
        
        total_membros_por_comunidade = df_comunidades['Comunidade_ID'].value_counts().sort_index()
        
        df_cas = df_comunidade_evento.div(total_membros_por_comunidade, axis=0)

        plt.figure(figsize=(14, 10))
        sns.heatmap(
            df_cas,
            annot=True,
            fmt=".2f",
            cmap="YlGnBu",
            linewidths=.5,
            linecolor='gray',
            cbar_kws={'label': 'Índice de Afiliação Comunitária (CAS)'}
        )
        
        plt.title(f'Afiliação Comunitária vs. Eventos CSBC ({PERIODO_PASTA})', fontsize=16)
        plt.ylabel('ID da Comunidade (Grafo Total)', fontsize=14)
        plt.xlabel('Sigla do Evento', fontsize=14)
        
        os.makedirs(OUTPUT_HEATMAP_DIR, exist_ok=True)
        plt.savefig(OUTPUT_HEATMAP_FILE, dpi=300, bbox_inches='tight')
        print(f"\nHeatmap CAS salvo em: {OUTPUT_HEATMAP_FILE}")

    except Exception as e:
        print(f"Ocorreu um erro durante a geração do Heatmap: {e}")
        
if __name__ == '__main__':
    gerar_heatmap_cas()