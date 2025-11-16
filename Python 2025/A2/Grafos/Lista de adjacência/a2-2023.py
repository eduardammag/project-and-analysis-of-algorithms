import heapq
from collections import deque

"""
Questão 1 (2 pontos)
--------------------
Dado um grafo G = (V, E) crie um algoritmo capaz de verificar se G é bipartido,
e analise a sua complexidade. Um grafo é bipartido se os vértices podem ser 
divididos em dois conjuntos V1 e V2 de forma que toda aresta e_k seja incidente 
em (v_i, v_j) tal que v_i ∈ V1 e v_j ∈ V2.

Nessa questão NÃO é permitido apenas fazer referência aos algoritmos vistos em aula;
eles podem ser usados, mas devem ser descritos explicitamente.

OBS: Usamos BFS porque ela percorre o grafo por camadas, o que se encaixa 
perfeitamente no processo de 2-colorir um grafo.
"""

def is_bipartite(graph):
    """
    Verifica se um grafo é bipartido usando BFS.
    Complexidade: O(V + E)
    """
    color = {}

    for start in graph:
        if start in color:
            continue

        color[start] = 0
        queue = deque([start])

        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if v not in color:
                    color[v] = 1 - color[u]
                    queue.append(v)
                else:
                    if color[v] == color[u]:
                        return False, {}

    return True, color



"""
Questão 2 (3 pontos)
--------------------
Precisamos projetar uma rede eficiente para uma nova planta industrial,
composta de várias unidades conectadas por fibra óptica.

Para cada par de unidades pode-se definir uma conexão e sabemos a largura
de banda que ela poderia atingir. A planta deseja a maior eficiência possível
com o MENOR número de conexões possível, sem redundância, conectando todas
as unidades.

Isso implica construir uma ÁRVORE GERADORA que maximize a soma das eficiências:
ou seja, uma Maximum Spanning Tree (MST máxima).

Nessa questão, algoritmos vistos em aula podem ser usados, mas DEVEM ser 
descritos explicitamente.
"""

def maximum_spanning_tree_prim(num_nodes, edges):
    """
    Constrói a Maximum Spanning Tree (MST máxima) usando Prim.
    - num_nodes: número de nós (assume nós 0..num_nodes-1)
    - edges: lista de tuplas (u, v, w) com peso w (eficiência)
    Retorna (mst_edges, total_weight)
    Lança ValueError se o grafo for desconexo (não for possível conectar todos).
    """
    # Montar lista de adjacência
    adj = [[] for _ in range(num_nodes)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))

    visited = [False] * num_nodes
    max_heap = []  # usaremos heapq com pesos negativos para simular max-heap
    mst_edges = []
    total = 0.0

    def add_node(start):
        """
        Marca 'start' como visitado e empurra no heap todas arestas (start->v)
        que levam a nós não visitados.
        """
        visited[start] = True
        for (v, w) in adj[start]:
            if not visited[v]:
                # empurra (peso_negativo, from, to)
                heapq.heappush(max_heap, (-w, start, v))

    # Inicializar Prim a partir do nó 0 (ou próximo não-visitado)
    # Para detectar desconexão, tentamos iniciar Prim em componentes não-visitadas.
    components_started = 0
    for node in range(num_nodes):
        if not visited[node]:
            # se já iniciámos uma componente e ainda existem componentes extras,
            # então o grafo é desconexo e não existe spanning tree única que conecte tudo.
            components_started += 1
            if components_started > 1:
                # ainda vamos tentar, mas ao final verificaremos se formou uma árvore completa
                pass
            add_node(node)

            # extrair arestas até não ser possível ou até termos n-1 arestas na MST
            while max_heap and len(mst_edges) < num_nodes - 1:
                negw, u, v = heapq.heappop(max_heap)
                if visited[v]:
                    # aresta para nó já visitado -> ignora
                    continue
                w = -negw
                # escolhemos essa aresta para a MST máxima
                mst_edges.append((u, v, w))
                total += w
                add_node(v)

            # se já temos num_nodes-1 arestas, podemos parar
            if len(mst_edges) == num_nodes - 1:
                break

    if len(mst_edges) != num_nodes - 1:
        raise ValueError("Grafo desconexo — não é possível conectar todas as unidades com uma única árvore.")

    return mst_edges, total



"""
Questão 3 (3 pontos)
--------------------
Um viajante deseja fazer uma viagem de X km pelo litoral do Brasil.

O motorhome possui autonomia de Y km com tanque cheio. 
Há vários postos de gasolina ao longo da rodovia, em distâncias conhecidas 
e ordenadas desde o início da viagem.

Deseja-se determinar o número mínimo de paradas necessárias para completar 
a viagem, ou indicar que ela é impossível.

Exemplo:
X = 620
Y = 120
postos = [20, 50, 90, 135, 180, 250, 260, 290, 360, 425, 480, 520, 600]

A estratégia ótima é GULOSA:
sempre abastecer no posto mais distante que ainda está ao alcance.
"""

def min_stops_for_trip(X, Y, stations):
    """
    Retorna o número mínimo de paradas, ou -1 se impossível.
    Complexidade: O(n)
    """
    if Y >= X:
        return 0

    stations = list(stations) + [X]

    pos = 0
    stops = 0
    i = 0
    n = len(stations)

    while pos + Y < X:
        last_ok = -1

        while i < n and stations[i] <= pos + Y:
            last_ok = i
            i += 1

        if last_ok == -1:
            return -1

        if stations[last_ok] == X:
            pos = X
            break

        pos = stations[last_ok]
        stops += 1

    return stops
