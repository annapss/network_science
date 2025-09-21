import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import os

def simulacao():
    n_vertices = 100
    n_instancias = 1000
    
    graus_medios_a_testar = np.logspace(-1, 1, 100)
    
    media_tamanho_gcc = []
    total_steps = len(graus_medios_a_testar)

    for i, atual_k in enumerate(graus_medios_a_testar):
        lista_tamanho_gcc = []
        p = atual_k / (n_vertices - 1) if (n_vertices - 1) > 0 else 0
        for _ in range(n_instancias):
            modelo = nx.erdos_renyi_graph(n_vertices, p)
            componentes = list(nx.connected_components(modelo))
            tamanho_gcc = 0
            if componentes:
                tamanho_gcc = len(max(componentes, key=len))
            lista_tamanho_gcc.append(tamanho_gcc)
        media = np.mean(lista_tamanho_gcc)
        media_tamanho_gcc.append(media)
        progresso = ((i + 1) / total_steps) * 100
        print(f"Progresso: {progresso:.1f}% completo (k_avg = {atual_k:.2f})")
    return graus_medios_a_testar, media_tamanho_gcc

if __name__ == '__main__':
    grau_medio, gcc_size = simulacao()

    output_dir = './erdos_renyi_model'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.figure(figsize=(10, 6))
    plt.plot(grau_medio, gcc_size, marker='o', linestyle='-', markersize=4)
    
    plt.xscale('log')
    
    plt.axvline(x=1, color='r', linestyle='--', label='Ponto Crítico (k=1)')
    plt.title('Modelo Erdős-Rényi: Transição de Fase (n=100) - Escala Log')
    plt.xlabel('Grau Médio (<k>) - Escala Log')
    plt.ylabel('Tamanho Médio da Componente Gigante (GCC)')
    plt.grid(True, which="both", ls="--")
    plt.legend()
    
    plt.savefig(os.path.join(output_dir, 'er_phase_transition_logscale.png'), dpi=300)
    plt.show()