import heapq

""""
Obs:
import heapq

pq = []  # cria uma lista vazia (a heap)
heapq.heappush(pq, (5, "A"))
heapq.heappush(pq, (3, "B"))
heapq.heappush(pq, (8, "C")) 
Agora pq internamente guarda os itens em ordem de prioridade:
[(3, "B"), (5, "A"), (8, "C")]
"""


""" 1)Em uma antiga cidade mágica, existem N portais conectados por passagens unidirecionais. 
Cada passagem leva um certo tempo para ser atravessada.
Um aprendiz de mago deseja saber o menor tempo possível para ir do portal 1 até o portal N.
Caso não exista caminho entre eles, deve informar que é impossível chegar. """

# Aplicação de Djisktra em um grafo de N vértices. 
# Cada aresta tem um peso.
# O peso é o tempo que ela leva para ser atravessada.
# Passagem unidirecional = grafo direcionado

def dijkstra(n, adj):
    """
    Calcula o menor tempo do portal 1 até o portal N.
    Reconstrói o caminho mínimo se ele existir.

    Parâmetros:
        n   -> número total de portais (vértices)
        adj -> lista de adjacência, onde adj[u] = [(v, tempo), ...]

    Retorna:
        (dist[n], caminho) se for possível chegar ao portal N
        ou ("impossivel", []) se não houver caminho
    """

    INF = float("inf")

    #dist guarda a menor distância conhecida de cada vértice até a origem (portal 1)
    dist = [INF] * (n+1)    #dist[u] =  menor distância conhecida de 1 até u
    dist[1] = 0             # distância da origem até ela mesma

    # parent também é uma lista, usada para reconstruir o caminho
    parent = [-1] * (n+1)   # parent[u] = nó anterior no caminho mínimo até u

    # Cada item da fila pq é uma tupla (distância_atual, vértice)
    pq = [(0,1)]            # heap min - fila de prioridade

    # enquanto houver vértices para processar:
    while pq:
            d,u = heapq.heappop(pq)

            # se já encontramos um caminho melhor antes, ignorar
            if d > dist[u]:
                    continue
                    
            # percorre todos os vizinhos de u
            for v, tempo in adj[u]:
                    
                    #custo total para chegar em v passando por u
                    novo_custo = dist[u] + tempo  

                    # se encontrar um caminho melhor, atualiza:
                    if novo_custo < dist[v]:
                            dist[v] = novo_custo
                            parent[v] = u # registra de onde veio
                            heapq.heappush(pq, (novo_custo, v))  

    # se o portal N for inalcançável
    if dist[n] == INF:
            return "impossível", []

    # reconstruindo o caminho 1 -> N usando o vetor parent
    caminho = []
    atual = n
    while atual != -1:
           caminho.append(atual)
           atual = parent[atual]
    caminho.reverse()

    return dist[n], caminho       
                                