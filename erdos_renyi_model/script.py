import networkx as nx
import numpy as np
import matplotlib.pyplot as plt 


def simulacao():
    n_vertices = 100
    n_instancias = 100
    max_grau_medio = 10
    media_tamanho_gcc = []
    graus_medios_a_testar = np.arange(0, max_grau_medio, 0.1)
    for atual_k in graus_medios_a_testar:
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
        progresso = (atual_k / max(graus_medios_a_testar)) * 100
        print(f"Progresso: {progresso:.1f}% completo (k_avg = {atual_k:.1f})")
    return graus_medios_a_testar, media_tamanho_gcc

if __name__ == '__main__':
    grau_medio, gcc_size = simulacao()

    plt.figure(figsize=(10, 6))
    plt.plot(grau_medio, gcc_size, marker='o', linestyle='-', markersize=4)
    plt.axvline(x=1, color='r', linestyle='--', label='Ponto Crítico (k=1)')
    plt.title('Modelo Erdős-Rényi: Transição de Fase (n=100)')
    plt.xlabel('Grau Médio (<k>)')
    plt.ylabel('Tamanho Médio da Componente Gigante (GCC)')
    plt.grid(True)
    plt.legend()
    plt.savefig('./erdos_renyi_model/er_phase_transition.png', dpi=300)
    plt.show()
