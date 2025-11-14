from graph_list import GraphList

def bellman_ford(graph: GraphList, v0: int):
    num_vertices = graph.num_vertices
    parent = [-1] * num_vertices
    distance = [float('inf')] * num_vertices

    # Inicializa o vértice de origem
    parent[v0] = v0
    distance[v0] = 0

    # Relaxa todas as arestas V-1 vezes
    for _ in range(num_vertices - 1):
        for v1 in range(num_vertices):
            for v2, cost in graph.adj_list[v1]:
                if distance[v1] != float('inf') and distance[v1] + cost < distance[v2]:
                    distance[v2] = distance[v1] + cost
                    parent[v2] = v1

    # Verifica se há ciclo negativo
    for v1 in range(num_vertices):
        for v2, cost in graph.adj_list[v1]:
            if distance[v1] != float('inf') and distance[v1] + cost < distance[v2]:
                print("Ciclo negativo detectado!")
                return parent, distance, False

    return parent, distance, True
