import heapq
from graph_list import GraphList

def dijkstra(graph: GraphList, v0: int):
    num_vertices = graph.num_vertices
    parent = [-1] * num_vertices
    distance = [float('inf')] * num_vertices
    checked = [False] * num_vertices

    # Inicializa o vértice inicial
    parent[v0] = v0
    distance[v0] = 0

    # Fila de prioridade (min-heap)
    heap = []
    heapq.heappush(heap, (0, v0))  # (distância, vértice)

    while heap:
        dist_v1, v1 = heapq.heappop(heap)

        # Se já processado, pula
        if checked[v1]:
            continue

        # Se a distância ainda é infinita, interrompe
        if distance[v1] == float('inf'):
            break

        # Relaxa as arestas de v1
        for v2, peso in graph.adj_list[v1]:
            if not checked[v2]:
                custo = peso
                if distance[v1] + custo < distance[v2]:
                    distance[v2] = distance[v1] + custo
                    parent[v2] = v1
                    heapq.heappush(heap, (distance[v2], v2))

        checked[v1] = True

    return parent, distance
