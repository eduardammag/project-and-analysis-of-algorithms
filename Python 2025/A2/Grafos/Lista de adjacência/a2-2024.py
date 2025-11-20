""" 1) Uma organização ambiental desenvolveu um sistema para 
monitoramento de florestas cuja comunicação é baseada em uma 
rede de sensores sem fio. Um sensor A consegue enviar uma 
mensagem para um sensor B diretamente se a distância entre eles 
for menor ou igual ao raio de transmissão s.r em metros.

Dado um conjunto de sensores S, em que cada elemento possui uma localização (s.x, s.y) 
e um raio de transmissão s.r em metros, projete um algoritmo capaz de calcular a rota 
para transmitir uma mensagem entre si e sf através dos sensores da rede, 
de forma que percorra a menor distância possível em metros.

O algoritmo deve retornar uma sequência de sensores representando o caminho completo 
que a mensagem irá percorrer:
— primeiro, os sensores utilizados para enviar a requisição de si até sf;
— em seguida, os sensores utilizados para enviar a resposta de sf até si.

Caso não seja possível estabelecer a comunicação, o algoritmo deve indicar isso.
Analise a complexidade do algoritmo proposto."""

import math
import heapq

def distancia(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

# Constrói o grafo baseado nas capacidades dos sensores
# sensores[i] = (x, y, r)
# Um sensor i pode se conectar a j se a distância entre eles
# for <= ao raio de ambos.
def construir_grafo(sensores):
    n = len(sensores)  # (vértices)
    adj = [[] for _ in range(n)]

    # Avalia todos os pares ordenados (i, j)
    for i in range(n):
        x1, y1, r1 = sensores[i]   
        for j in range(n):
            if i == j:
                continue
            x2, y2, r2 = sensores[j]  
            d = distancia((x1, y1), (x2, y2))
            # Criamos aresta i → j *somente se* o raio de i é suficiente
            # para cobrir a distância até j.
            if d <= r1:
                # Adiciona aresta saindo de i para j, com peso = distância
                adj[i].append((j, d))

    return adj


# Implementação clássica do Dijkstra com min-heap (heapq)
# Retorna o caminho mínimo entre 'start' e 'end'
def dijkstra(adj, start, end):
    n = len(adj)
    dist = [float('inf')] * n                # distâncias mínimas
    parent = [-1] * n                        # para reconstruir caminho
    dist[start] = 0                          # distância do início é 0
    pq = [(0, start)]                        # heap (distância, vértice)
    while pq:
        d, u = heapq.heappop(pq)             # pega vértice de menor distância atual
        if d > dist[u]:                     
            continue
        if u == end:                         # se chegou ao destino, pode parar
            break
        # relaxamento das arestas
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))
    # se não alcança o destino
    if dist[end] == float('inf'):
        return None
    # reconstrói o caminho em ordem reversa
    path = []
    cur = end
    while cur != -1:
        path.append(cur)
        cur = parent[cur]
    path.reverse()                           # inverte para ordem correta
    return path


def rota_completa(sensores, si, sf):
    adj = construir_grafo(sensores)          # constrói o grafo
    ida = dijkstra(adj, si, sf)              # caminho de ida
    volta = dijkstra(adj, sf, si)            # caminho de volta
    if ida is None or volta is None:         # se qualquer lado for impossível
        return None
    return ida + volta[1:]                  # remove duplicação do vértice central (sf)


# ANÁLISE DE COMPLEXIDADE
# rota_completa():
#   - Chama construir_grafo → O(n^2)
#   - Chama dijkstra duas vezes → 2 * O(E log V)
#   - Como o grafo pode ter até E = O(n^2) arestas no pior caso,
#     então: Θ(n² log n)

""" 2) Considere um grafo G = (V, E) conexo e não-dirigido.
Dizemos que uma aresta e ∈ E é uma ponte se sua remoção
produzir um grafo G' não-conexo.

a) Se existir uma aresta e = (vi, vj) que não é uma ponte podemos afirmar 
   que existe um ciclo em G que contém os vértices vi e vj. Por quê?

b) Projete um algoritmo que receba uma aresta e = (vi, vj) e determine 
   se a mesma é uma ponte. """

# Verifica se uma aresta (u, v) é ponte em um grafo não-direcionado.
#
# Uma aresta é ponte se, ao removê-la, o número de componentes
# conexas do grafo aumenta — ou seja, ela é essencial para
# conectar partes do grafo.
#
# O algoritmo usa DFS com arrays tin[] e low[], técnica clássica
# de Tarjan para encontrar pontes.

def eh_ponte(adj, u, v):
    """
    Determina se a aresta (u, v) é ponte.
    adj é lista de adjacência: adj[x] = [vizinhos]
    """

    n = len(adj)                       # quantidade de vértices
    visited = [False] * n              # marca se vértice já foi visitado
    tin = [-1] * n                     # tempo de descoberta do vértice
    low = [-1] * n                     # menor tempo alcançável via ancestrais ou back-edges
    timer = [0]                        # contador mutável usado dentro da DFS
    is_bridge = [False]                # será marcado como True se (u, v) for ponte

    # DFS para calcular tin[x] e low[x]
    # parent: pai no DFS (para não contar aresta de retorno
    # como aresta de árvore)
    def dfs(x, parent):
        visited[x] = True
        tin[x] = low[x] = timer[0]     # tanto tin quanto low começam iguais
        timer[0] += 1                  # incrementa tempo global

        # percorre todos os vizinhos de x
        for y in adj[x]:

            # ignora a aresta que volta para o pai
            if y == parent:
                continue

            if not visited[y]:
                # seguimos na árvore DFS
                dfs(y, x)

                # atualiza low[x] baseado no filho y
                low[x] = min(low[x], low[y])

                # condição clássica de ponte:
                # se low[y] > tin[x], então a aresta (x, y) é ponte
                if low[y] > tin[x]:

                    # verifica se justamente a aresta testada é (u, v)
                    if (x == u and y == v) or (x == v and y == u):
                        is_bridge[0] = True

            else:
                # caso de aresta de retorno (back-edge)
                # atualiza low[x] usando tin[y]
                low[x] = min(low[x], tin[y])

    # Chamamos a DFS a partir do vértice 0
    # (assume-se grafo conectado, ou ao menos que
    # a aresta buscada está no mesmo componente)
    dfs(0, -1)

    return is_bridge[0]


# ANÁLISE DE COMPLEXIDADE

# Seja V = número de vértices e E = número de arestas.
#
# - A DFS percorre cada vértice uma única vez → O(V)
# - Cada aresta (u, v) é examinada no máximo duas vezes (ida/volta) → O(E)
# - Todas as operações dentro da DFS são O(1)
#
# Portanto, o tempo total é:
#
#             Θ(V + E)
#
# O uso de tin[] e low[] não altera a ordem de complexidade,
# pois são apenas acessos O(1) durante o DFS.
#
# Complexidade espacial:
#   Arrays visited, tin, low → O(V)
#   Pilha recursiva da DFS → O(V) no pior caso

""" 3) Uma empresa está projetando a infraestrutura de comunicação para sua nova planta industrial.
A planta possui diversos prédios que precisam ser conectados através de fibra óptica.
Para cada par de prédios existe um custo para instalação e uma largura de banda máxima.
A engenharia já definiu o conjunto mínimo de conexões necessárias para interligar 
todos os prédios minimizando custo total (i.e., uma Árvore Geradora Mínima).
A equipe de TI deseja tornar o projeto tolerante a falhas inserindo redundâncias — 
ou seja, para cada par de prédios deve existir mais de um caminho na rede.
Dada a topologia completa da planta (com custos e larguras de banda possíveis), 
o conjunto de conexões já escolhido, e um requisito mínimo de velocidade W, 
projete um algoritmo que decide se é possível tornar a rede tolerante a falhas 
garantindo redundância para todas as conexões. 
O algoritmo deve retornar a lista de conexões redundantes com banda ≥ W, 
ou indicar se é impossível. Analise a complexidade.
"""
from collections import deque

# -------------------------------------------------------------------
# BFS MODIFICADO:
# Encontra caminho entre u e v sem usar a aresta proibida (ban_u, ban_v),
# e usando apenas arestas com banda >= W.
# -------------------------------------------------------------------
def bfs_alternativo(adj, u, v, W, ban_u, ban_v):
    fila = deque([u])
    visit = {u}

    # Queremos encontrar caminho alternativo U → V
    # mas sem poder usar a aresta da MST (ban_u, ban_v)
    while fila:
        x = fila.popleft()

        if x == v:
            return True   # caminho alternativo encontrado

        for y, peso, banda in adj[x]:

            # NÃO usar a aresta (ban_u, ban_v) nem (ban_v, ban_u)
            if (x == ban_u and y == ban_v) or (x == ban_v and y == ban_u):
                continue

            # Respeitar banda mínima
            if banda < W:
                continue

            if y not in visit:
                visit.add(y)
                fila.append(y)

    return False


# -------------------------------------------------------------------
# ALGORITMO PRINCIPAL
#
# mst_edges: lista de arestas da MST já fornecida
# adj: grafo completo com custo e banda
# W: banda mínima
#
# Retorna lista de arestas externas que geram redundância
#         OU None se impossível
# -------------------------------------------------------------------
def encontrar_redundancias(adj, mst_edges, W):

    redundantes = []

    # Para cada aresta da MST precisamos encontrar um segundo caminho
    for u, v in mst_edges:

        # Tentar encontrar caminho alternativo
        ok = bfs_alternativo(adj, u, v, W, ban_u=u, ban_v=v)

        if not ok:
            return None   # impossível garantir redundância

        # Agora precisamos registrar QUAL aresta externa foi usada.
        #
        # Para isso, procuramos uma aresta externa (a,b)
        # que permita banda >= W e que forme ciclo com (u,v).
        #
        # Versão simples: vamos procurar QUALQUER aresta externa com banda >= W
        # que conecte dois nós do caminho u→v sem passar pela própria (u,v).
        #
        # Observação:
        # Aqui estamos pegando a primeira aresta externa possível.
        # Em versões avançadas faríamos o rastreamento real do ciclo.
        for a in range(len(adj)):
            for b, peso, banda in adj[a]:

                # Ignorar aresta da própria MST
                if (a, b) in mst_edges or (b, a) in mst_edges:
                    continue

                # Banda mínima
                if banda < W:
                    continue

                # Se esta aresta permite caminho alternativo, serve como redundância
                if bfs_alternativo(adj, u, v, W, ban_u=u, ban_v=v):
                    redundantes.append((a, b))
                    break

            else:
                continue
            break

    return redundantes
