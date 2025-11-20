from graph_list import GraphList
import heapq
from collections import deque

"""1) Uma enchente inundou uma cidade representada 
por uma grade N x M. Cada célula pode ser:
. (terreno seco)
# (alagado)
S (posição inicial do socorrista)
V (vítima a ser resgatada)

O socorrista só pode andar por terrenos secos
(células . ou V), nas quatro direções. Seu objetivo é
determinar quantas vítimas podem ser alcançadas
 a partir de S. """
# mapa é a matriz do problema

def vitimas_regastadas(mapa):
    N = len(mapa)
    M = len(mapa[0])

    for i in range(N):
       for j in range(M):
             if mapa[i][j] == 'S':
                   sx,sy = i,j

    # Matriz para marcar se a célula já foi visitada                  
    visit = [[False]*M for _ in range(N)]
    # Cria uma lista com M elementos e repete isso N vezes

    # Fila do BFS, começando da posição inicial
    fila = deque([sx,sy])

    # parent[x][y] será a célula que levou até (x, y)
    parent = [[None] * M for _ in range(N)]  
    caminhos = []     # Lista para guardar o caminho até cada vítima encontrada

    visit[sx][sy] = True # ponto inicial visitado
    dirs = [(1,0), (-1,0), (0,1), (0,-1)] # direções possíveis: baixo, cima, direita, esquerda
    total = 0 # contador de vítimas encontradas

    # Início do BFS
    while fila:
        x,y = fila.popleft()
        if mapa[x][y] == 'V':
              caminho = []        # lista para guardar o caminho até esta vítima
              cx, cy = x, y       # começa da célula da vítima
              total += 1
              # Caminha de trás pra frente até chegar em S
              while (cx, cy) != (sx, sy):
                caminho.append((cx, cy))        # adiciona posição atual
                cx, cy = parent[cx][cy]        # anda para o pai da posição atual
                caminho.append((sx, sy)) # adiciona a posição inicial
                caminho.reverse()             # Como o caminho foi montado ao contrário, invertê-lo
                caminhos.append(caminho)             # Armazena o caminho final

        # Tenta mover para as 4 direções possíveis
        for dx, dy in dirs:
              nx, ny = x + dx , y + dy      
              # Verifica se a nova posição está nos limites do mapa
              if 0 <= nx < N and 0<= ny < M:
                    # Não podemos visitar célular alagadas ou que já foram descobertas
                    if not visit[nx][ny] and mapa[nx][ny] != "#":
                        visit[nx][ny] = True
                        parent[nx][ny] = (x, y)       # salva de onde veio
                        fila.append((nx,ny))
    return total, caminhos                    

# Complexidade: O(NM)


"""2)Uma empresa tem N computadores conectados
por cabos bidirecionais. Cada cabo tem um tempo
de transmissão (em milissegundos), que pode ser
negativo (um canal otimizado experimental).
Você precisa calcular o menor tempo de transmissão
entre o computador 1 e todos os outros."""

def tempo_transmissao(graph = GraphList):
      N = graph.num_vertices
      dist = [float('inf')]* N    # dist[v] é a menor distância conhecida de 0 a v, começa com todas as distancia infinitas
      dist[0] = 0 
      edges = []
      for u in range(N): # percorre todos os vértices
        for v,w in graph.adj_list[u]:
              edges.append((u,v,w))

    # Etapa principal do Bellman-Ford
    # Relaxa todas as arestas N-1 vezes
    # Isso garante a menor distância possível se não houver ciclo negativo
      for _ in range(N - 1):  # repete N-1 rodadas de relaxamento
        mudou = False       # flag que detecta se alguma aresta mudou

        # percorre cada aresta (u, v, w)
        for u, v, w in edges:
            # se a distância para u não é infinita e passar por u melhora v...
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                # atualiza dist[v]
                dist[v] = dist[u] + w
                mudou = True  # marca que houve mudança

        # se nenhuma distância mudou na rodada inteira, pode parar antes
        if not mudou:
            break

      for u, v, w in edges:
        # se ainda dá pra melhorar dist[v], há ciclo negativo
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            return "Ciclo negativo achado"

    # retorna o vetor de distâncias finais
      return dist


"""3)Você deve conectar N ilhas por pontes. 
Cada ponte tem um custo de construção. O objetivo
é construir pontes suficientes para que todas
as ilhas fiquem conectadas, com o menor custo
total possível. """

def custo_mst_ilhas_prim(graph: GraphList):
    N = graph.num_vertices
    # Caso especial: grafo vazio não tem arestas e o custo é zero
    if N == 0:
        return 0

    # vetor para marcar quais vértices já foram incluídos na MST
    visitado = [False] * N

    # min_heap guardará tuplas (peso, u, v)
    # onde "peso" é a chave usada para ordenar a heap
    # e u -> v é a aresta que estamos considerando
    min_heap = []

    # Escolha arbitrária de um vértice inicial (0)
    # Prim pode começar de qualquer ponto, pois a MST existe
    # em grafos conectados e não depende do start.
    visitado[0] = True  # marca o vértice 0 como visitado (entrou na MST)

    # Insere na heap TODAS as arestas que saem do vértice 0
    # Isso inicializa a fronteira da MST.
    for v, w in graph.adj_list[0]:
        # heapq.heappush mantém a min-heap ordenada pelo primeiro elemento da tupla
        heapq.heappush(min_heap, (w, 0, v))

    # total acumula o custo da MST final
    total = 0

    # "usados" conta quantas arestas já foram adicionadas na MST
    # Uma MST de N vértices precisa ter exatamente N-1 arestas
    usados = 0

    # Loop principal do Prim
    # Pegamos sempre a menor aresta que liga a MST a um vértice não visitado
    # enquanto houver opções na heap.
    while min_heap:
        # Extraímos a aresta de menor peso disponível
        w, u, v = heapq.heappop(min_heap)

        # Se o vértice v já está visitado, essa aresta não serve mais
        # (pois formaria um ciclo ou é redundante), então ignoramos
        if visitado[v]:
            continue

        # Caso contrário, essa é a menor aresta que expande a MST
        # então incluímos v na árvore
        visitado[v] = True

        # acumulamos o seu custo ao total da MST
        total += w

        # marcamos que mais uma aresta foi usada
        usados += 1

        # Agora precisamos adicionar na heap todas as arestas
        # que saem de v e apontam para vértices ainda não visitados.
        # Isso expande a fronteira da MST.
        for viz, peso in graph.adj_list[v]:
            if not visitado[viz]:
                heapq.heappush(min_heap, (peso, v, viz))

    # Após o loop, verificamos se realmente conseguimos formar
    # uma MST válida.
    #
    # Para isso, precisamos ter usado exatamente N-1 arestas.
    # Se usamos menos, significa que o grafo tinha componentes desconexas.
    if usados != N - 1:
        return "impossível conectar"

    # Retorna o custo total da MST calculada
    return total



"""4)Você está desenvolvendo um sistema de rotas
para uma cidade com N cruzamentos e M ruas de mão única.
Cada rua tem um tempo de deslocamento. Calcule o
tempo mínimo para ir do cruzamento 1 ao cruzamento N."""

import heapq  # biblioteca padrão para usar min-heap (priority queue)

def menor_rota(graph: GraphList):
    N = graph.num_vertices
    dist = [float('inf')] * N
    dist[0] = 0

    # heap guarda pares (distância, vértice)
    # começamos com o vértice 0 tendo custo 0
    heap = [(0, 0)]

    # Loop principal do Dijkstra
    # Sempre extraímos o vértice com menor distância atual
    while heap:
        # heappop retorna o menor elemento da heap
        d, u = heapq.heappop(heap)

        # Se esse valor d é maior que a distância "oficial" dist[u],
        # então esse item está desatualizado e deve ser ignorado.
        # (isso evita processar caminhos piores)
        if d > dist[u]:
            continue

        # Percorre todas as arestas que saem de u:
        # u -> v com peso w
        for v, w in graph.adj_list[u]:

            # Relaxamento da aresta:
            # Se ao passar por u conseguimos chegar em v com um custo menor,
            # atualizamos dist[v]
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

                # Empurramos a nova distância para a heap,
                # permitindo que Dijkstra a considere futuramente
                heapq.heappush(heap, (dist[v], v))

    # Após o Dijkstra terminar, verificamos se existe caminho
    # até o último vértice (N-1).
    # Se a distância ainda for infinita, não há rota possível.
    # Se não existe caminho até o último vértice, retorne -1.
    if dist[N - 1] == float('inf'):
        return -1

    # Caso contrário, retorne a menor distância encontrada.
    return dist[N - 1]

"""5)Um império possui várias cidades conectadas
por pontes e túneis secretos. As pontes podem ser
destruídas por inimigos, mas os túneis são subterrâneos
e seguros. Você precisa identificar todas as pontes
críticas — arestas que, se destruídas,
desconectam o grafo."""

def pontes_no_grafo(graph: GraphList):
    # Número de vértices do grafo
    N = graph.num_vertices

    # "tempo" é usado para registrar a ordem de descoberta na DFS
    tempo = 0

    # tin[u] = tempo em que o vértice u foi descoberto
    tin = [-1] * N

    # low[u] = menor tempo de descoberta alcançável a partir de u
    # (incluindo subir por uma aresta de retorno/back-edge)
    low = [-1] * N

    # lista final de pontes
    pontes = []

    # DFS que calcula tin[], low[] e identifica pontes.
    # Argumentos:
    #   u      = vértice atual
    #   parent = pai de u na DFS (para não voltar por onde veio)
    def dfs(u, parent):
        nonlocal tempo  # permite modificar 'tempo' definido fora da função

        # Marca tempo de descoberta
        tempo += 1
        tin[u] = low[u] = tempo

        # Explora vizinhos de u
        for v, _ in graph.adj_list[u]:
            # Ignora a aresta de onde acabamos de vir (u -> parent)
            if v == parent:
                continue

            # Caso o vértice v ainda não tenha sido visitado...
            if tin[v] == -1:
                # Explora recursivamente v
                dfs(v, u)

                # Após voltar do DFS de v, atualizamos low[u]
                # pois v pode alcançar ancestrais de u
                low[u] = min(low[u], low[v])

        
                # Checagem da condição de ponte:
                # low[v] > tin[u]  significa que NÃO há caminho alternativo
                # para voltar a u ou seus ancestrais a partir de v.
                #
                # Logo, a única ligação entre os dois lados do grafo é (u, v).
        
                if low[v] > tin[u]:
                    # armazenamos a ponte em ordem crescente (u, v)
                    pontes.append(tuple(sorted((u, v))))

            else:
                # Se v já foi visitado e não é o pai,
                # então (u, v) é uma back-edge.
                # Atualizamos low[u] com o tin[v],
                # mostrando que u pode voltar a um ancestral via v.
                low[u] = min(low[u], tin[v])

    # A DFS pode iniciar de qualquer vértice, mas o grafo pode
    # ter múltiplas componentes, então rodamos para todos.
    for i in range(N):
        if tin[i] == -1:   # ainda não visitado
            dfs(i, -1)     # não tem pai, então parent = -1

    # Ordena as pontes para ficarem em ordem previsível
    pontes.sort()

    # Retorna a lista final de pontes
    return pontes


""" 6)Em uma antiga cidade mágica, existem N portais conectados por passagens unidirecionais. 
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
                                

""" 7) Os reinos de um continente estão formando alianças. Cada aliança entre dois reinos tem um custo de manutenção anual.
O conselho deseja criar alianças suficientes para que todos os reinos estejam conectados (direta ou indiretamente), mas gastando o mínimo possível."""     

import heapq  # para usar min-heap

def custo_minimo_reinos(graph: GraphList):
    """
    Calcula o custo mínimo para conectar todos os reinos (vértices)
    usando o algoritmo de Prim para construir a MST.

    graph.adj_list[u] deve conter pares (v, w),
    onde existe aresta u -> v com peso w.
    """

    N = graph.num_vertices

    # Caso trivial: grafo vazio ou com 1 vértice
    if N <= 1:
        return 0

    # vetor que marca quais vértices já entraram na MST
    visitado = [False] * N

    # heap de prioridades: guarda tuplas (peso, u, v)
    # peso = custo da aresta
    # u = vértice que está na MST
    # v = vértice novo que pode entrar
    heap = []

    # Começamos arbitrariamente pelo vértice 0
    visitado[0] = True

    # Inserimos na min-heap TODAS as arestas que saem do vértice 0
    for v, w in graph.adj_list[0]:
        heapq.heappush(heap, (w, 0, v))

    total = 0       # custo da MST
    usados = 0      # quantas arestas já foram adicionadas

    # Enquanto ainda houver arestas candidatas
    while heap:
        w, u, v = heapq.heappop(heap)

        # Se v já está visitado, essa aresta é inútil
        if visitado[v]:
            continue

        # Aresta escolhida: ela conecta a MST a um novo vértice
        visitado[v] = True
        total += w
        usados += 1

        # Agora, adicionamos todas as arestas que saem de v
        # e levam para vértices ainda não visitados
        for viz, peso in graph.adj_list[v]:
            if not visitado[viz]:
                heapq.heappush(heap, (peso, v, viz))

    # Verificação: uma MST válida precisa de exatamente N - 1 arestas
    if usados != N - 1:
        return "impossível conectar"

    return total


"""8)Você recebeu o mapa de uma floresta dividida em N x M células. 
Cada célula pode conter:
. (terreno livre)
# (árvore gigante intransponível)
S (posição inicial do explorador)
T (tesouro escondido)
Descubra se o explorador consegue chegar até o tesouro movendo-se
apenas nas quatro direções (cima, baixo, esquerda, direita) por terrenos livres."""

def pode_chegar_tesouro(mapa):
    N = len(mapa)
    M = len(mapa[0])

    for i in range(N):
        for j in range(M):
            if mapa[i][j] == 'S':
                sx, sy = i, j

    fila = deque([(sx, sy)])
    visit = [[False]*M for _ in range(N)]
    visit[sx][sy] = True
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]

    while fila:
        x, y = fila.popleft()

        if mapa[x][y] == 'T':
            return "sim"

        for dx, dy in dirs:
            nx, ny = x+dx, y+dy
            if 0 <= nx < N and 0 <= ny < M:
                if not visit[nx][ny] and mapa[nx][ny] != '#':
                    visit[nx][ny] = True
                    fila.append((nx, ny))

    return "nao"


"""9)O governo deseja planejar o transporte ferroviário entre N cidades.
Algumas conexões já existem, e cada trilho tem um comprimento em quilômetros.
Um trem parte da cidade 1 e precisa visitar todas as outras cidades que sejam possíveis de alcançar.
Determine quantas cidades podem ser alcançadas a partir da cidade 1."""

def cidades_alcancaveis(graph: GraphList):
    N = graph.num_vertices
    visit = [False] * N

    def dfs(u):
        visit[u] = True
        for v, _ in graph.adj_list[u]:
            if not visit[v]:
                dfs(v)

    dfs(0)  # cidade 1 → índice 0
    return sum(visit)


"""10)Há N templos interligados por corredores subterrâneos
bidirecionais. Alguns corredores são frágeis — se forem
destruídos, podem dividir a rede de templos em partes
desconectadas. Descubra quais corredores são críticos,
ou seja, se forem removidos, a conexão entre os templos
será perdida."""

def pontes_criticas(graph: GraphList):
    # Número total de vértices (templos)
    N = graph.num_vertices

    # 'tempo' é um contador global usado para marcar a ordem de descoberta (tin)
    tempo = 0

    # tin[u] = tempo em que o vértice u foi descoberto pela DFS
    tin = [-1] * N

    # low[u] = menor tempo de descoberta alcançável a partir de u
    # seguindo qualquer quantidade de arestas da DFS (incluindo retorno)
    low = [-1] * N

    # Lista final onde serão guardadas as pontes (corredores críticos)
    pontes = []

    # FUNÇÃO DFS (profundidade) PARA DETECTAR PONTES
    def dfs(u, parent):
        nonlocal tempo
        
        # Avança o tempo global e marca o tempo de descoberta de u
        tempo += 1
        tin[u] = low[u] = tempo  

        # Percorre todos os vizinhos de u
        for v, _ in graph.adj_list[u]:

            # Ignora a aresta que volta para o "pai" (parent)
            if v == parent:
                continue

            # Se v ainda não foi visitado, seguimos a DFS
            if tin[v] == -1:
                dfs(v, u)

                # Após retornar da DFS de v, atualizamos low[u]
                low[u] = min(low[u], low[v])

                # -----------------------------------------------------
                # CONDIÇÃO DE PONTE:
                # se low[v] > tin[u], NÃO existe caminho alternativo
                # para voltar a u ou a algum ancestral.
                # Ou seja, essa aresta é crítica.
                # -----------------------------------------------------
                if low[v] > tin[u]:
                    pontes.append(tuple(sorted((u, v))))

            else:
                # Encontramos uma aresta de retorno (back-edge)
                # que liga u a um ancestral.
                # Isso diminui o valor de low[u].
                low[u] = min(low[u], tin[v])

    # Roda DFS a partir de todos os vértices não visitados
    # (importante em grafos desconexos)
    for i in range(N):
        if tin[i] == -1:
            dfs(i, -1)  # -1 indica que não há "pai" no início

    # Ordenamos para facilitar leitura
    pontes.sort()

    return pontes
