from analise_subgrafo import analisar_subgrafo
import sys
import os

# Defina a janela deslizante aqui!
ANO_INICIO = 2019
ANO_FIM = 2023

EVENTOS_CSBC = [
    'CTD', 'CTIC', 'SEMISH', 'WEI', 'WIT', 'ETC', 
    'ENCompIF', 'WASHES', 'WPerformance', 'SBCUP'
]

def criar_diretorios():
    try:
        os.makedirs('trabalho_final/metricas', exist_ok=True)
        os.makedirs('trabalho_final/metricas/comunidades', exist_ok=True)
        os.makedirs('trabalho_final/metricas/centralidades', exist_ok=True)
        os.makedirs('trabalho_final/visualizacao', exist_ok=True)
        os.makedirs('trabalho_final/edge_list/por_evento', exist_ok=True)
    except Exception as e:
        print(f"Erro ao criar diretórios: {e}")
        sys.exit(1)
        
criar_diretorios()

print("------ INICIANDO ANÁLISE DA REDE TOTAL ------")
analisar_subgrafo(ANO_INICIO, ANO_FIM) 
print("------ ANÁLISE DA REDE TOTAL CONCLUÍDA ------\n")

print("------ INICIANDO ANÁLISE DOS EVENTOS INDIVIDUAIS ------")
for evento in EVENTOS_CSBC:
    analisar_subgrafo(ANO_INICIO, ANO_FIM, sigla_evento=evento)

print("\n--- Processamento de TODOS os eventos e da REDE TOTAL concluído. ---")