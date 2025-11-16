"""
Questão 1 (3 pontos)

Uma organização ambiental desenvolveu um sistema para monitoramento de florestas 
cuja comunicação é baseada em uma rede de sensores sem fio. 
Um sensor A consegue enviar uma mensagem para um sensor B diretamente se a distância entre eles 
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
Analise a complexidade do algoritmo proposto.

É permitido fazer referência a estruturas de dados da aula.
"""

import math
import heapq

# -----------------------------------------------------------
# Função que calcula a distância euclidiana entre dois pontos
# -----------------------------------------------------------
def distancia(a, b):
    # Fórmula da distância: sqrt((x1-x2)^2 + (y1-y2)^2)
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)


# -----------------------------------------------------------
# Constrói o grafo baseado nas capacidades dos sensores
# sensores[i] = (x, y, r)
# Um sensor i pode se conectar a j se a distância entre eles
# for <= ao raio de ambos.
# O grafo é representado como lista de adjacências.
# -----------------------------------------------------------
def construir_grafo(sensores):
    n = len(sensores)                        # número de sensores (vértices)
    adj = [[] for _ in range(n)]             # lista de adjacências

    # Verifica cada par de sensores (i, j)
    for i in range(n):
        x1, y1, r1 = sensores[i]
        for j in range(n):
            if i == j:                       # ignora laço próprio
                continue
            x2, y2, r2 = sensores[j]
            d = distancia((x1, y1), (x2, y2))

            # Se ambos podem transmitir um ao outro
            if d <= r1 and d <= r2:
                adj[i].append((j, d))        # adiciona aresta i → j com peso d

    return adj


# -----------------------------------------------------------
# Implementação clássica do Dijkstra com min-heap (heapq)
# Retorna o caminho mínimo entre 'start' e 'end'
# -----------------------------------------------------------
def dijkstra(adj, start, end):
    n = len(adj)
    dist = [float('inf')] * n                # distâncias mínimas
    parent = [-1] * n                        # para reconstruir caminho
    dist[start] = 0                          # distância do início é 0

    pq = [(0, start)]                        # heap (distância, vértice)

    while pq:
        d, u = heapq.heappop(pq)             # pega vértice de menor distância atual

        if d > dist[u]:                      # ignora entrada atrasada
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


# -----------------------------------------------------------
# Monta grafo e calcula rota total si → sf e sf → si
# Se algum sentido não possuir caminho, retorna None
# -----------------------------------------------------------
def rota_completa(sensores, si, sf):
    adj = construir_grafo(sensores)          # constrói o grafo
    ida = dijkstra(adj, si, sf)              # caminho de ida
    volta = dijkstra(adj, sf, si)            # caminho de volta

    if ida is None or volta is None:         # se qualquer lado for impossível
        return None

    # remove duplicação do vértice central (sf)
    return ida + volta[1:]


# -----------------------------------------------------------
# ANÁLISE COMPLETA DE COMPLEXIDADE
# -----------------------------------------------------------

# construir_grafo(sensores):
#   - Loop duplo sobre todos os pares (i, j)
#   - Para cada par, cálculo O(1) de distância
#   - Portanto:  O(n^2)
#
# dijkstra(adj):
#   - Usa heapq, custo para push/pop = O(log n)
#   - Cada aresta relaxada no máximo 1 vez
#   - Tempo total: O(E log V)
#
# rota_completa():
#   - Chama construir_grafo → O(n^2)
#   - Chama dijkstra duas vezes → 2 * O(E log V)
#   - Como o grafo pode ter até E = O(n^2) arestas no pior caso,
#     então:
#         O(E log V) = O(n^2 log n)
#
# COMPLEXIDADE TOTAL:
#     O(n^2) + 2 * O(n^2 log n)
#     = O(n^2 log n)
#
# Portanto, a função rota_completa tem complexidade:
#
#              Θ(n² log n)
#
# No pior caso (grafo denso).
# -----------------------------------------------------------


"""
Questão 2 (2 pontos)

Considere um grafo G = (V, E) conexo e não-dirigido.
Dizemos que uma aresta e ∈ E é uma ponte se sua remoção produzir um grafo G' não-conexo.

a) Se existir uma aresta e = (vi, vj) que não é uma ponte podemos afirmar 
   que existe um ciclo em G que contém os vértices vi e vj. Por quê?

b) Projete um algoritmo que receba uma aresta e = (vi, vj) e determine 
   se a mesma é uma ponte.

Não é permitido apenas fazer referência a algoritmos da aula, 
é necessário descrever.
"""

# -----------------------------------------------------------
# Verifica se uma aresta (u, v) é ponte em um grafo não-direcionado.
#
# Uma aresta é ponte se, ao removê-la, o número de componentes
# conexas do grafo aumenta — ou seja, ela é essencial para
# conectar partes do grafo.
#
# O algoritmo usa DFS com arrays tin[] e low[], técnica clássica
# de Tarjan para encontrar pontes.
# -----------------------------------------------------------

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

    # -------------------------------------------------------
    # DFS para calcular tin[x] e low[x]
    # parent: pai no DFS (para não contar aresta de retorno
    # como aresta de árvore)
    # -------------------------------------------------------
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


# -----------------------------------------------------------
# ANÁLISE DE COMPLEXIDADE
# -----------------------------------------------------------

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
# -----------------------------------------------------------

"""
Questão 3 (3 pontos)

Uma empresa está projetando a infraestrutura de comunicação para sua nova planta industrial.
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

from heapq import heappush, heappop

# -----------------------------------------------------------
# PRIM – Gera a Árvore Geradora Mínima (AGM)
#
# adj[u] = lista de tuplas (v, peso, banda)
# A AGM é representada como lista de arestas (u, v)
# -----------------------------------------------------------
def prim_agm(adj):
    """
    Executa PRIM para gerar a árvore geradora mínima.
    adj[u] = lista (v, peso, banda)
    Retorna lista de arestas (u, v)
    """

    n = len(adj)                       # número de vértices
    visited = [False] * n              # indica se o vértice já foi inserido na AGM
    mst_edges = []                     # lista final de arestas da AGM

    pq = [(0, 0, -1)]                  # heap: (peso, vértice atual, pai)
                                       # começa pelo vértice 0 com custo 0

    while pq:
        w, u, parent = heappop(pq)     # remove menor peso disponível no heap

        if visited[u]:                 # se já foi incluído na AGM, ignora
            continue

        visited[u] = True              # marca que entrou na AGM

        if parent != -1:
            mst_edges.append((parent, u))  # adiciona aresta escolhida

        # examina todos vizinhos de u
        for v, peso, banda in adj[u]:
            if not visited[v]:
                # empurra para heap usando peso como chave de minimização
                heappush(pq, (peso, v, u))

    return mst_edges


# -----------------------------------------------------------
# BFS filtrando por banda mínima
# Verifica se há caminho entre u e v usando apenas arestas
# cuja banda >= W.
# -----------------------------------------------------------
def existe_caminho(adj, u, v, W):
    """
    Verifica se existe caminho entre u e v usando apenas arestas banda >= W.
    BFS simples.
    """

    from collections import deque
    q = deque([u])              # fila do BFS
    visited = {u}               # conjunto de vértices visitados

    while q:
        x = q.popleft()         # remove da fila

        if x == v:              # chegou ao destino
            return True

        # explora vizinhos respeitando banda mínima
        for y, peso, banda in adj[x]:
            if banda >= W and y not in visited:
                visited.add(y)
                q.append(y)

    return False                # nenhum caminho respeitou banda mínima


# -----------------------------------------------------------
# Verifica redundância para cada aresta da AGM.
# A redundância exige que entre cada aresta (u, v) da AGM
# exista um segundo caminho alternativo que respeite banda >= W.
# -----------------------------------------------------------
def redundancia(adj, W):
    """
    adj[u] = (v, custo, banda)
    W = banda mínima

    Retorna lista de arestas extras necessárias ou None se impossível.
    """

    mst_edges = prim_agm(adj)           # AGM gerada pela engenharia
    extras = []                         # arestas redundantes encontradas

    # Para cada aresta da AGM, verifica se existe outro caminho alternativo
    for u, v in mst_edges:

        # Se NÃO existir caminho alternativo com banda mínima W, então
        # a rede não é redundante.
        if not existe_caminho(adj, u, v, W):
            return None  # impossível garantir redundância

        # Caso exista, apenas registramos que a redundância foi satisfeita
        extras.append((u, v))

    return extras


# -----------------------------------------------------------
# ANÁLISE COMPLETA DE COMPLEXIDADE
# -----------------------------------------------------------

# Suponha:
#   V = número de vértices
#   E = número de arestas
#
# 1) prim_agm(adj)
#    - Cada aresta pode ser empurrada para o heap no máximo uma vez.
#    - heappush / heappop custam O(log V)
#    - Custo total:  O(E log V)
#
# 2) existe_caminho(adj, u, v, W)
#    - BFS limitado pelas arestas válidas
#    - No pior caso examina todas as arestas uma vez:  O(V + E)
#
# 3) redundancia(adj, W)
#    - Chama PRIM:                        O(E log V)
#    - Para cada aresta da AGM (são V - 1 arestas):
#         chama existe_caminho → O(V + E)
#
#    Custo total:
#        O(E log V) + (V - 1) * O(V + E)
#      = O(E log V + V*(V + E))
#
#    Para grafos densos (E ≈ V²):
#        O(V² log V + V*(V + V²)) = O(V³)
#
#    Para grafos esparsos (E ≈ V):
#        O(V log V + V*(2V)) = O(V²)
#
#
# COMPLEXIDADE FINAL DA FUNÇÃO redundancia
#
#        Θ(V*(V + E))          no pior caso
#
# Em grafos densos → Θ(V³)
# Em grafos esparsos → Θ(V²)
# -----------------------------------------------------------
