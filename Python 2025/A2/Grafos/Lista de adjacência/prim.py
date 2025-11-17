import heapq
import math
from graph_list import GraphList

def prim(graph = GraphList):
    num_vertices = graph.num_vertices

    # parent[v] = quem é o pai de v na MST
    parent = [-1] * num_vertices

    # Marca se o vértice já foi incluído na MST
    in_tree = [False] * num_vertices

    # Custos mínimos para chegar a cada vértice
    vertex_cost = [math.inf] * num_vertices
    vertex_cost[0] = 0  # Começamos do vértice 0

    # Heap de prioridades (min-heap)
    # Cada item será (custo, vertice)
    heap = []

    # Inicializa o heap com todos os vértices
    for v in range(num_vertices):
        heapq.heappush(heap, (vertex_cost[v], v))

    # Enquanto houver vértices a processar
    while heap:
        cost, v1 = heapq.heappop(heap)

        # Evita processar entradas obsoletas do heap
        if in_tree[v1]:
            continue

        # Se o custo for infinito, não há mais conexões válidas
        if cost == math.inf:
            break

        in_tree[v1] = True

        # Explora todos os vizinhos de v1
        for (v2, peso) in graph.adj_list[v1]:

            # Se ainda não está na MST e o peso é menor que o custo atual
            if not in_tree[v2] and peso < vertex_cost[v2]:
                vertex_cost[v2] = peso
                parent[v2] = v1
                heapq.heappush(heap, (vertex_cost[v2], v2))

    return parent