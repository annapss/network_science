import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

ANO_INICIO = 2019 
ANO_FIM = 2023    
PERIODO_PASTA = f'{ANO_INICIO}-{ANO_FIM}'

INPUT_FILE = os.path.join(
    'trabalho_final', 'metricas', 'comunidades', PERIODO_PASTA, 
    f'contagem_genero_comunidade_total.csv'
)
OUTPUT_HEATMAP_DIR = os.path.join('trabalho_final', 'visualizacao', PERIODO_PASTA)
OUTPUT_HEATMAP_FILE = os.path.join(OUTPUT_HEATMAP_DIR, f'heatmap_comunidade_vs_genero_{PERIODO_PASTA}.png')

def gerar_heatmap_genero():
    try:
        if not os.path.exists(INPUT_FILE):
             print(f"ERRO: Arquivo de contagem de gênero/comunidade não encontrado: {INPUT_FILE}")
             print("Certifique-se de que 'analise_eventos.py' foi executado e gerou o arquivo de contagem para a rede TOTAL no período.")
             return

        df_contagem = pd.read_csv(INPUT_FILE, index_col='Comunidade_ID')
        
        generos = ['Homem', 'Mulher'] 
        df_heatmap_data = df_contagem[generos].copy()
        
        df_proporcao = df_heatmap_data.div(df_contagem['Total_Comunidade'], axis=0).fillna(0)
           
        print(f"Dados prontos para o Heatmap. {len(df_proporcao)} comunidades encontradas.")

        plt.figure(figsize=(10, 15))
        sns.heatmap(
            df_proporcao,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            linewidths=.5,
            linecolor='gray',
            cbar_kws={'label': 'Proporção de Membros por Gênero (0 a 1)'}
        )
        
        plt.title(f'Composição de Gênero das Comunidades ({PERIODO_PASTA})', fontsize=16)
        plt.ylabel('ID da Comunidade', fontsize=14)
        plt.xlabel('Gênero', fontsize=14)
        
        os.makedirs(OUTPUT_HEATMAP_DIR, exist_ok=True)
        plt.savefig(OUTPUT_HEATMAP_FILE, dpi=300, bbox_inches='tight')
        print(f"\nHeatmap Gênero/Comunidade salvo em: {OUTPUT_HEATMAP_FILE}")

    except Exception as e:
        print(f"Ocorreu um erro durante a geração do Heatmap de Gênero: {e}")
        
if __name__ == '__main__':
    gerar_heatmap_genero()