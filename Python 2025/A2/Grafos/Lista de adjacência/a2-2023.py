import heapq
from graph_list import GraphList
from collections import deque

""" 1) Dado um grafo G = (V, E) crie um algoritmo capaz de verificar se G é bipartido,
e analise a sua complexidade. Um grafo é bipartido se os vértices podem ser 
divididos em dois conjuntos V1 e V2 de forma que toda aresta e_k seja incidente 
em (v_i, v_j) tal que v_i ∈ V1 e v_j ∈ V2.

OBS: Usamos BFS porque ela percorre o grafo por camadas, o que se encaixa 
perfeitamente no processo de 2-colorir um grafo. Complexidade: O(V + E)
"""

def is_bipartite(graph = GraphList):
    num_vertices = graph.num_vertices
    # Dicionário que guarda a cor de cada vértice: 0 ou 1
    color = {}

    # Percorre todos os vértices do grafo (necessário caso o grafo seja desconexo)
    for start in range(num_vertices):
        if start in color:
            continue

        # Atribui cor inicial (0) ao componente que começa em 'start'
        color[start] = 0

        # Inicia uma fila de BFS contendo apenas o vértice inicial
        queue = deque([start])

        while queue:
            u = queue.popleft()
            for v, _ in graph.adj_list[u]:
                if v not in color:
                    color[v] = 1 - color[u]
                    queue.append(v)
                else:
                    if color[v] == color[u]:
                        return False, {}
    return True, color


""" 2) Precisamos projetar uma rede eficiente para uma nova planta industrial,
que consiste em várias unidades interconectadas por uma rede de fibra óptica,
buscando a maior velocidade de comunicação possível. Para cada par de unidades
existente pode-se definir uma conexão, e sabemos a largura de banda que a mesma
poderia atingir, se escolhida para a rede. Em função de cortes de orçamento,
a empresa determinou que a planta deve ser projetada com o menor número de
conexões possível, sem redundância, no entanto conectando todas as unidades na
planta (observe que duas unidades podem se comunicar indiretamente pela rede,
mesmo sem uma conexão direta entre elas). Projete um algoritmo capaz de
encontrar o menor conjunto de conexões que atenda essa especificação,
maximizando a eficiência global da rede. Analise a complexidade do algoritmo
proposto – quanto mais eficiente melhor."""

#Isso implica construir uma ÁRVORE GERADORA que maximize a soma das eficiências:
#ou seja, uma Maximum Spanning Tree (MST máxima).

# O heapq do Python é min-heap (sempre retorna o menor elemento). 
# O algoritmo de Prim aqui precisa extrair a maior aresta que liga o conjunto 
# visitado ao não-visitado (max-heap). Uma forma simples de simular um max-heap
# com heapq é inverter o sinal do peso

def maximum_spanning_tree_prim(graph: GraphList):
    num_nodes = graph.num_vertices
    visited = [False] * num_nodes
    max_heap = []          # heap de arestas, usando pesos negativos para max-heap
    mst_edges = []         # lista de arestas da MST máxima (u, v, peso)
    total = 0.0            # peso total da MST

    def add_node(u):
        """
        Marca o nó u como visitado e insere no heap todas as arestas
        (u -> v) que levam a nós ainda não-visitados.
        """
        visited[u] = True
        for (v, w) in graph.adj_list[u]:  # acessa do seu grafo
            if not visited[v]:
                heapq.heappush(max_heap, (-w, u, v))  # peso negativo → simula max-heap

    # Controle para detectar se o grafo é desconexo
    components_started = 0

    # Tenta iniciar Prim a partir de cada componente não visitada
    for node in range(num_nodes):
        if not visited[node]:
            components_started += 1
            add_node(node)

            # Extrai arestas até conseguir n-1 ou terminarem as possíveis
            while max_heap and len(mst_edges) < num_nodes - 1:
                neg_w, u, v = heapq.heappop(max_heap)
                if visited[v]:
                    # Se v já foi visitado, essa aresta não serve
                    continue
                w = -neg_w  # volta para peso positivo

                # Aresta adicionada à Maximum Spanning Tree
                mst_edges.append((u, v, w))
                total += w

                add_node(v)

            # Se já formamos a MST completa, paramos
            if len(mst_edges) == num_nodes - 1:
                break

    # Se terminamos e não temos n-1 arestas, não existe árvore geradora
    if len(mst_edges) != num_nodes - 1:
        raise ValueError("Grafo desconexo — não é possível formar uma única Maximum Spanning Tree.")

    return mst_edges, total

# O(ElogV)


""" 3) Um viajante deseja fazer uma viagem de X km pelo litoral do Brasil.
O motorhome possui autonomia de Y km com tanque cheio. Há vários postos de
gasolina ao longo da rodovia, em distâncias conhecidas e ordenadas desde o
início da viagem. Deseja-se determinar o número mínimo de paradas
necessárias para completar a viagem, ou indicar que ela é impossível.
Exemplo: X = 620, Y = 120, postos = [20, 50, 90, 135, 180, 250, 260, 290, 360, 425, 480, 520, 600]"""

#A estratégia ótima é GULOSA:
#sempre abastecer no posto mais distante que ainda está ao alcance.

def min_stops_for_trip(X, Y, stations):
    # Caso de não precisar parar em nenhum posto.
    if Y >= X:
        return 0, []

    # Tratamos X como um “posto final” 
    stations = list(stations) + [X]

    pos = 0 # posição atual do viajante (início = km 0)
    stops = 0 # Contador de paradas
    chosen_stops = []   # Lista para os postos escolhidos
    i = 0 # Índice para percorrer a lista de postos
    n = len(stations)

    # Enquanto a autonomia atual não permitir chegar no destino
    while pos + Y < X:
        last_ok = -1 # índice do posto mais distante que conseguimos alcançar

        # Avançamos enquanto houver postos dentro do alcance (pos + Y)
        while i < n and stations[i] <= pos + Y:
            last_ok = i      # atualizamos o último posto possível
            i += 1           # avançamos no array de postos

        # Se nenhum posto está ao alcance, não há solução possível
        if last_ok == -1:
            return -1, []

        # Se o posto alcançável mais distante for o destino,
        # não precisamos mais parar.
        if stations[last_ok] == X:
            pos = X          # chegamos ao destino
            break            # fim do processo

        # Caso contrário, paramos no posto mais distante possível
        pos = stations[last_ok]      # avançamos até o posto escolhido
        chosen_stops.append(pos)     # registramos esse posto na lista
        stops += 1                   # aumentamos o número de paradas

    # Retorna a quantidade total de paradas e os postos usados
    return stops, chosen_stops

#O(n)