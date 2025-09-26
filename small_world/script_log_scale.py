import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import os

def simulacao_watts_strogatz():
    n_vertices = 1000
    k_value = 10
    n_amostras = 20
    
    graus_medios_a_testar = np.logspace(-4, 0, 25) 
    
    valores_medios_cp = []
    valores_medios_lp = []
    total_steps = len(graus_medios_a_testar)

    modelo = nx.watts_strogatz_graph(n_vertices, k_value, 0)

    l0 = nx.average_shortest_path_length(modelo)
    c0 = nx.average_clustering(modelo)

    for i, p in enumerate(graus_medios_a_testar):
        lista_cp_temp = []
        lista_lp_temp = []

        for j in range(n_amostras):
            modelo = nx.watts_strogatz_graph(n_vertices, k_value, p)
            lp = nx.average_shortest_path_length(modelo)
            cp = nx.average_clustering(modelo)
            lista_cp_temp.append(cp)
            lista_lp_temp.append(lp)
        media_cp = np.mean(lista_cp_temp)
        media_lp = np.mean(lista_lp_temp)
        valores_medios_cp.append(media_cp)
        valores_medios_lp.append(media_lp)
        progresso = ((i + 1) / total_steps) * 100
        print(f"Progresso: {progresso:.1f}% completo (p = {p:.4f})")
    lp_normalizado = np.array(valores_medios_lp) / l0
    cp_normalizado = np.array(valores_medios_cp) / c0
    return graus_medios_a_testar, lp_normalizado, cp_normalizado

if __name__ == '__main__':
    probabilidades, L_norm, C_norm = simulacao_watts_strogatz()

    output_dir = './small_world'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.figure(figsize=(10, 6))
    
    plt.plot(probabilidades, L_norm, marker='o', linestyle='-', label='L(p) / L(0)')
    plt.plot(probabilidades, C_norm, marker='s', linestyle='-', label='C(p) / C(0)')
    
    plt.xscale('log')
    
    plt.title('Modelo Watts-Strogatz: L(p) e C(p) normalizados (n=1000, k=10)')
    plt.xlabel('Probabilidade de Religação (p) - Escala Log')
    plt.ylabel('Valores Normalizados')
    plt.grid(True, which="both", ls="--")
    plt.legend()
    
    plt.savefig(os.path.join(output_dir, 'watts_strogatz_figura2_reproducao.png'), dpi=300)
    plt.show()