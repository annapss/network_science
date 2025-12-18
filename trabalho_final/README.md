# Trabalho Final

Aqui explico como foram calculadas as métricas que foram apresentados no trabalho final da disciplina de Ciência de Redes.

## Organização do Repositório

- ./dados: tem o dataset completo em que cada linha apresenta nome do artigo, conferência publicada, sigla da conferência, ano de publicação, categoria, autor do artigo
- ./edge_list: arquivos criados após a limpeza dos dados
- ./metricas: arquivos csv com os resultados de calculos que fiz. Dentro de métricas, tem arquivos com as metricas gerais de cada janela separada por evento e tem da rede sem considerar um evento específico também.
- ./metricas/centralidades: calculei a centralidade do top 10% de cada janela e evento. Os resultados ficam nessa pasta.
- ./metricas/comunidades: resultado da detecção de comunidades da rede como um todo e de cada evento por janela de tempo. Para o trabalho, achei que as comunidades detectadas na rede como um todo ficaram mais interessantes.
- ./metricas/scripts: scripts utilizados para calcular metricas gerais de cada rede, detecção de comunidades e centralidades
- ./metricas/versao_antiga_scripts: aqui foram as primeiras versões dos scripts que montei. Deixei aqui só para caso eu precisasse fazer algo parecido novamente.
- ./metricas/inicio-fim: as pastas com os anos de inicio e fim das janelas deslizantes apresentam os resultados dos cálculos das metricas. Podem ver que nas pastas de centralidades e comunidades esse padrão se repete.
- ./similaridade_autores: aqui são os autores que apresentam nomes parecidos e podem ser considerados como sendo o mesmo nó.
- ./visualizacao: aqui são gráficos e imagens que foram criados

## Ordem de execução dos scripts
- Em cada script há a possibilidade de colocar um ano de início e um ano de fim. Para cada janela deslizante, foram executados os scripts na seguinte ordem:
    - ./gera_csv_rede_total.py
    - ./gera_csv_subgrafo_evento.py
    - ./gera_csv_coatoria.py
    - ./metricas/scripts/analise_eventos.py
    - ./metricas/scripts/heatmap_eventos.py
    - ./metricas/scripts/heatmap_genero_comunidade.py
    - ./metricas/scripts/grafico_linhas_assortatividade_v2.py

Após executar os scripts, pode encontrar os gráficos gerados em ./visualizacao para a janela deslizante escolhida