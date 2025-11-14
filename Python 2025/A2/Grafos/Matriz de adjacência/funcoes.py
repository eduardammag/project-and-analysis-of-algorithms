from graph_matrix import GraphMatrix

# 1) para G e H com o mesmo número de vertices, H e subgrafo de G?

def is_subgraph(G: GraphMatrix, H: GraphMatrix) -> bool:
    if G.num_vertices != H.num_vertices:
        return False
    
    for i in range(H.num_vertices):
        for j in range(H.num_vertices):
            if H.has_edge(i,j) and not G.has_edge(i,j):
                return False

    return True    #complexidade O(V²)


# 2) Dado 𝐺 = (𝑉,𝐸) e um caminho 𝑃 composto por uma sequência de vertices.
# 𝑃 e um caminho de 𝐺? O caminho e simples (sem repetiçao de vertices)?

def is_path(graph: GraphMatrix, path: list[int]) -> tuple[bool, bool]:
    """Retorna: (is_valid_path, is_simple_path)"""
    length = len(path)

    # Um caminho precisa ter pelo menos 2 vertices
    if length < 2: 
        return False, False

    # Flag para indicar se o caminho e simples
    is_simple = True

    # Conjunto para armazenar os vertices ja visitados
    visited = set()

    # Percorre cada par consecutivo de vertices no caminho
    for i in range(length -1):
        v1 = path[i]
        v2 = path[i+1]

        # Verifica se ha uma aresta entre v1 e v2 no grafo
        if not graph.has_edge(v1,v2):
            return False, False
        
        # Verifica se o vertice atual ja foi visitado
        if v1 in visited:
            is_simple = False
        else:
            visited.add(v1)    
    
    # Checando a simplicidade do último vertice
    if path[-1] in visited:
        is_simple = False

    return True, is_simple   # A complexidade é O(len(path))  



# 3) Crie um algoritmo que verifica se a numeração dos vértices de um grafo G=(𝑉,𝐸) é topológica.

def is_topological(graph: GraphMatrix) -> bool:
    """
    Verifica se a numeração dos vértices é topológica.
    Ou seja, se para toda aresta (i -> j), temos i < j.
    """ 
    num_vertices = graph.num_vertices
    # Percorre todos os vértices
    for i in range(num_vertices):
        # Percorre todos os possíveis vizinhos j
        for j in range(num_vertices):
            # Se existe aresta i -> j
            if graph.has_edge(i, j):
                # Verifica se i >= j → então não é topológica
                if i >= j:
                    return False
    # Se nenhuma aresta violou a condição, é topológica
    return True

# 4) Crie um algoritmo para determinar se um grafo possui ordenação topológica e determiná-la

def has_topological_order(graph: "GraphMatrix"):
    """
    Determina se um grafo direcionado possui ordenação topológica e, se existir,
    retorna essa ordenação.

    Parâmetros:
        graph (GraphMatrix): Grafo representado por matriz de adjacência.

    Retorna:
        (bool, list): 
            - True e lista com a ordem topológica se o grafo for acíclico.
            - False e lista vazia se o grafo contiver ciclos.
    """

    num_vertices = graph.num_vertices  # Número total de vértices no grafo
    in_degree = [0] * num_vertices     # Lista para armazenar o grau de entrada de cada vértice

    # Calcula o grau de entrada (in-degree) de cada vértice
    # Para cada aresta u -> v, incrementa in_degree[v]
    for u in range(num_vertices):
        for v in range(num_vertices):
            if graph.has_edge(u, v):
                in_degree[v] += 1

    # Inicializa a fila de vértices com grau de entrada zero
    # Esses vértices podem começar a ordenação topológica
    queue = [v for v in range(num_vertices) if in_degree[v] == 0]

    processed = []  # Lista para armazenar a ordem de processamento dos vértices

    index = 0  # Índice para simular a remoção de elementos da fila sem usar pop(0)
    while index < len(queue):
        v = queue[index]  # Pega o próximo vértice da fila
        index += 1        # Avança o índice (equivalente a remover da fila)
        processed.append(v)  # Adiciona o vértice à ordem topológica

        # Para cada vértice adjacente a v
        # Reduz o grau de entrada, pois removemos v da "fila"
        for u in range(num_vertices):
            if graph.has_edge(v, u):
                in_degree[u] -= 1
                # Se o grau de entrada de u chegou a zero, adiciona à fila
                if in_degree[u] == 0:
                    queue.append(u)

    # Se todos os vértices foram processados, o grafo é acíclico e possui ordenação topológica
    has_order = len(processed) == num_vertices

    # Retorna True + lista com a ordem topológica ou False + lista parcial/vazia
    return has_order, processed
