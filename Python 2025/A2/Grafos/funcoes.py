from classe_graph_list import *
from collections import deque

def bfs(graph: GraphList, start: int):
    visited = [False] * graph.num_vertices
    ordem = []
    fila = deque([start])
    visited[start] = True

    while fila:
        v = fila.popleft()
        ordem.append(v)
        for viz, _ in graph.adj_list[v]:
            if not visited[viz]:
                visited[viz] = True
                fila.append(viz)
    return ordem










def dfs(graph: GraphList, start: int):
    visited = [False] * graph.num_vertices
    ordem = []

    def _dfs(v):
        visited[v] = True
        ordem.append(v)
        for viz, _ in graph.adj_list[v]:
            if not visited[viz]:
                _dfs(viz)

    _dfs(start)
    return ordem







import heapq

def dijkstra(graph: GraphList, start: int):
    dist = [float('inf')] * graph.num_vertices
    dist[start] = 0
    pq = [(0, start)]  # (distância, vértice)

    while pq:
        d, v = heapq.heappop(pq)
        if d > dist[v]:
            continue
        for viz, peso in graph.adj_list[v]:
            nova_dist = dist[v] + peso
            if nova_dist < dist[viz]:
                dist[viz] = nova_dist
                heapq.heappush(pq, (nova_dist, viz))

    return dist













def bellman_ford(graph: GraphList, start: int):
    dist = [float('inf')] * graph.num_vertices
    dist[start] = 0

    # Relaxa as arestas N-1 vezes
    for _ in range(graph.num_vertices - 1):
        for v1 in range(graph.num_vertices):
            for v2, peso in graph.adj_list[v1]:
                if dist[v1] + peso < dist[v2]:
                    dist[v2] = dist[v1] + peso

    # Detecta ciclos negativos
    for v1 in range(graph.num_vertices):
        for v2, peso in graph.adj_list[v1]:
            if dist[v1] + peso < dist[v2]:
                raise ValueError("Grafo contém ciclo negativo!")

    return dist





def prim(graph: GraphList, start: int = 0):
    visited = [False] * graph.num_vertices
    pq = [(0, start, -1)]  # (peso, v, pai)
    mst = []
    total = 0

    while pq:
        peso, v, pai = heapq.heappop(pq)
        if visited[v]:
            continue
        visited[v] = True
        total += peso
        if pai != -1:
            mst.append((pai, v, peso))
        for viz, w in graph.adj_list[v]:
            if not visited[viz]:
                heapq.heappush(pq, (w, viz, v))

    return mst, total










def kruskal(graph: GraphList):
    # Reúne todas as arestas (sem duplicar)
    arestas = []
    for v1 in range(graph.num_vertices):
        for v2, peso in graph.adj_list[v1]:
            if graph.direcionado or v1 < v2:  # evita duplicar se for não direcionado
                arestas.append((peso, v1, v2))

    # Ordena pelo peso
    arestas.sort()

    # Funções do union-find
    pai = list(range(graph.num_vertices))
    rank = [0] * graph.num_vertices

    def find(v):
        if pai[v] != v:
            pai[v] = find(pai[v])
        return pai[v]

    def union(v1, v2):
        raiz1, raiz2 = find(v1), find(v2)
        if raiz1 != raiz2:
            if rank[raiz1] < rank[raiz2]:
                pai[raiz1] = raiz2
            elif rank[raiz1] > rank[raiz2]:
                pai[raiz2] = raiz1
            else:
                pai[raiz2] = raiz1
                rank[raiz1] += 1
            return True
        return False

    mst = []
    total = 0

    for peso, v1, v2 in arestas:
        if union(v1, v2):
            mst.append((v1, v2, peso))
            total += peso

    return mst, total






g = GraphList(5, direcionado=False)
g.add_edge(0, 1, 2)
g.add_edge(0, 2, 4)
g.add_edge(1, 2, 1)
g.add_edge(1, 3, 7)
g.add_edge(2, 4, 3)

print("BFS:", bfs(g, 0))
print("DFS:", dfs(g, 0))
print("Dijkstra:", dijkstra(g, 0))
print("Bellman-Ford:", bellman_ford(g, 0))
print("Prim:", prim(g))
print("Kruskal:", kruskal(g))
