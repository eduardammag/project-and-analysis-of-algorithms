class GraphList:
    def __init__(self, num_vertices, direcionado: bool = True):
        self.num_vertices = num_vertices
        self.num_edges = 0
        self.direcionado = direcionado

        # Cria uma lista vazia para cada vértice
        # Cada posição conterá uma lista de tuplas (vizinho, peso)
        self.adj_list = [[] for _ in range(num_vertices)]

    def has_edge(self, v1, v2):
        for vizinho in self.adj_list[v1]:
            if vizinho == v2:
                return True
        return False

    def add_edge(self, v1, v2, peso = 1.0):
        if not self.has_edge(v1, v2):
            self.adj_list[v1].append((v2, peso))
            self.num_edges += 1

            # se o grafo não é direcionado, adiciona a aresta contrária também
            if not self.direcionado:
                self.adj_list[v2].append((v1, peso))
                self.num_edges += 1

    def remove_edge(self, v1, v2):
        # procura e remove a aresta (v1, v2)
        for vizinho, peso in list(self.adj_list[v1]):
            if vizinho == v2:
                self.adj_list[v1].remove((vizinho, peso))
                self.num_edges -= 1
                break

        # se o grafo não for direcionado, remove também o inverso
        if not self.direcionado:
            for vizinho, peso in list(self.adj_list[v2]):
                if vizinho == v1:
                    self.adj_list[v2].remove((vizinho, peso))
                    self.num_edges -= 1
                    break

    def print_edges(self):
        print("Arestas do grafo:")
        for v1 in range(self.num_vertices):
            for v2, peso in self.adj_list[v1]:
                print(f"({v1} -> {v2}, peso = {peso})")
        print()

    def print_list(self):
        # Mostra cada vértice e os vértices alcançáveis a partir dele
        print("Lista de adjacência:")
        for v in range(self.num_vertices):
            print(f"{v}: {self.adj_list[v]}")
        print()
