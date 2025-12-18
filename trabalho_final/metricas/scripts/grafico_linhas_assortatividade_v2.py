import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

periodos = ['2016-2020', '2017-2021', '2018-2022', '2019-2023']
eventos_lista = ['CTD', 'CTIC', 'SEMISH', 'WEI', 'WIT', 'ETC', 
                 'ENCompIF', 'WASHES', 'WPerformance', 'SBCUP']

grupo1 = eventos_lista[:5]
grupo2 = eventos_lista[5:]

grupos = [
    {'nome': 'Grupo 1', 'eventos': grupo1, 'arquivo': 'evolucao_assortatividade_grupo1.png'},
    {'nome': 'Grupo 2', 'eventos': grupo2, 'arquivo': 'evolucao_assortatividade_grupo2.png'}
]

dados_lista = []
eventos_para_processar = ['total'] + eventos_lista

for p in periodos:
    for e in eventos_para_processar:
        caminho = os.path.join('trabalho_final', 'metricas', p, f'metricas_globais_{e}.csv')
        if os.path.exists(caminho):
            try:
                df = pd.read_csv(caminho, index_col=0)
                valor = df.loc['Assortatividade (Gênero)', 'Valor']
                valor_numeric = pd.to_numeric(valor, errors='coerce')
                if not pd.isna(valor_numeric):
                    dados_lista.append({'Período': p, 'Evento': e, 'Assortatividade': valor_numeric})
            except Exception as err:
                print(f"Erro ao processar {caminho}: {err}")

df_plot = pd.DataFrame(dados_lista)

sns.set_style("whitegrid")
output_dir = 'trabalho_final/visualizacao'
os.makedirs(output_dir, exist_ok=True)

for g in grupos:
    plt.figure(figsize=(12, 7))
    
    eventos_no_grafico = ['total'] + g['eventos']
    df_grupo = df_plot[df_plot['Evento'].isin(eventos_no_grafico)]
    
    df_apenas_eventos = df_grupo[df_grupo['Evento'] != 'total']
    sns.lineplot(
        data=df_apenas_eventos, 
        x='Período', 
        y='Assortatividade', 
        hue='Evento', 
        marker='o',
        linewidth=1.5,
        alpha=0.5
    )
    
    df_total = df_grupo[df_grupo['Evento'] == 'total']
    if not df_total.empty:
        plt.plot(
            df_total['Período'], 
            df_total['Assortatividade'], 
            color='black', 
            marker='s',
            linewidth=4,
            label='TOTAL (Rede)',
            zorder=10
        )
    
    plt.axhline(0, color='red', linestyle='--', alpha=0.5, label='Neutro (0)')
    plt.title(f'Evolução da Assortatividade: {g["nome"]} vs Total', fontsize=16)
    plt.ylabel('Coeficiente de Assortatividade (r)', fontsize=12)
    plt.xlabel('Janelas de Tempo', fontsize=12)
    plt.ylim(-0.25, 0.75)
    
    plt.legend(title='Eventos', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    save_path = os.path.join(output_dir, g['arquivo'])
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Gráfico do {g['nome']} salvo em: {save_path}")

print("\n--- Processamento concluído: Dois gráficos gerados. ---")