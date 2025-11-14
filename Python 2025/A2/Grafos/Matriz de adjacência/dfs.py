from graph_matrix import GraphMatrix

def dfs_recursive(graph: GraphMatrix, v: int, pre_order: list[int], counter: list[int]) -> None:
    """
    Função recursiva da DFS.
    Marca o vértice `v` como visitado e explora seus vizinhos recursivamente.
    
    Args:
        graph: objeto GraphMatrix representando o grafo
        v: vértice atual sendo visitado
        pre_order: lista que armazena o instante de descoberta de cada vértice
        counter: lista de tamanho 1 usada como contador (simula passagem por referência)
    """

    # Marca o vértice atual com o contador atual (momento de descoberta)
    pre_order[v] = counter[0]

    # Imprime o vértice visitado, a lista pre_order atual e o contador
    print(f"Visitando vertice {v} -> pre_order = {pre_order}, contador = {counter[0]}")

    # Incrementa o contador para o próximo vértice
    counter[0] += 1

    # Percorre todos os vértices do grafo para verificar vizinhos
    for u in range(graph.num_vertices):
        # Se existe uma aresta de v para u e u ainda não foi visitado
        if graph.has_edge(v, u) and pre_order[u] == -1:
            # Imprime a ação de ir de v para u
            print(f" Indo de {v} -> {u}")
            # Chamada recursiva para visitar u
            dfs_recursive(graph, u, pre_order, counter)

    # Imprime quando a função retorna de um vértice (fim da exploração de todos os vizinhos)
    print(f"Retornando de {v}")


def dfs(graph: GraphMatrix, start_vertex: int = 0) -> list[int]:
    """
    Realiza a busca em profundidade (DFS) em um grafo usando matriz de adjacência.

    Args:
        graph: objeto GraphMatrix
        start_vertex: vértice inicial da busca (padrão 0)

    Returns:
        pre_order: lista onde cada posição indica o instante de descoberta do vértice correspondente
    """
    num_vertices = graph.num_vertices

    # Inicializa a lista de pre_order com -1 indicando que nenhum vértice foi visitado
    pre_order = [-1] * num_vertices

    # Inicializa o contador como lista de tamanho 1 (para simular passagem por referência)
    counter = [0]

    # Imprime início da DFS a partir do vértice especificado
    print(f"\n--- Iniciando DFS a partir do vertice {start_vertex} ---")

    # Chama a função recursiva a partir do vértice inicial
    dfs_recursive(graph, start_vertex, pre_order, counter)

    # Para cobrir componentes desconexas, verifica todos os vértices
    for v in range(num_vertices):
        # Se o vértice ainda não foi visitado, inicia uma nova DFS
        if pre_order[v] == -1:
            print(f"\n--- Iniciando nova DFS em componente desconexa a partir do vertice {v} ---")
            dfs_recursive(graph, v, pre_order, counter)

    
    print("\nDFS finalizada. Ordem final de visita:")
    print(pre_order)
    return pre_order    # A complexidade será Θ(𝑉²) .

# --------------------------------------------------------------
# COMPLEXIDADE DO DFS EM MATRIZ DE ADJACÊNCIA
#
# 1. Inicialização:
#    - pre_order = [-1] * V        -> O(V) tempo e espaço
#    - counter = [0]                -> O(1) tempo e espaço
#
# 2. Função dfs_recursive:
#    - Cada chamada marca o vértice atual como visitado -> O(1)
#    - Loop 'for u in range(V)' percorre todos os vértices para checar vizinhos
#      -> Cada iteração do loop é O(1) para has_edge, mas percorre V vértices -> O(V)
#    - Cada vértice é visitado apenas uma vez
#    - Portanto, total dfs_recursive para todos os vértices: O(V^2)
#
# 3. Função dfs (loop principal):
#    - Garante que todas as componentes desconexas sejam visitadas
#    - Cada vértice ainda é visitado apenas uma vez
#    - Não altera a complexidade total → continua O(V^2)
#
# 4. Espaço usado:
#    - pre_order -> O(V)
#    - pilha de recursão -> profundidade máxima V -> O(V)
#    - matriz de adjacência -> V x V -> O(V^2)
#    - Espaço total dominante: O(V^2)
#
# 5. Resumo final:
#    - Tempo: O(V^2) (matriz de adjacência percorre todos os vértices para cada vértice)
#    - Espaço: O(V^2) dominante pela matriz + O(V) para listas/pilha de recursão
# --------------------------------------------------------------

# --------------------------------------------------------------
# COMPLEXIDADE DFS (MATRIZ DE ADJACÊNCIA)
#
# Tempo:
#   - Cada vértice é visitado uma vez
#   - Para cada vértice, percorremos todos os V vértices para checar vizinhos
#   → O(V^2)
#
# Espaço:
#   - Matriz de adjacência: O(V^2)
#   - Lista pre_order + pilha de recursão: O(V)
#   → Total dominante: O(V^2)
# --------------------------------------------------------------
