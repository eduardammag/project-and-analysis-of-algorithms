from graph_list import GraphList
from collections import deque

def bfs(graph: GraphList, v0: int):
    num_vertices = graph.num_vertices
    order = [-1] * num_vertices    
    parent = [-1] * num_vertices    
    queue = deque()                 
    counter = 0

    order[v0] = counter
    counter += 1
    parent[v0] = v0
    queue.append(v0)

    while queue:
        v1 = queue.popleft()
        for v2, _ in graph.adj_list[v1]:
            if order[v2] == -1: 
                order[v2] = counter
                parent[v2] = v1
                counter += 1
                queue.append(v2)
    return order, parent

def reconstruir_caminho(parent, origem, destino):
    if parent[destino] == -1:
        return None
    
    caminho = [destino]
    while caminho[-1] != origem:
        caminho.append(parent[caminho[-1]])
    caminho.reverse()
    return caminho







