class GraphList:
    def __init__(self, num_vertices: int, direcionado: bool = True):
        self.num_vertices = num_vertices
        self.num_edges = 0
        self.direcionado = direcionado
        self.adj_list = [[] for _ in range(num_vertices)]

    def has_edge(self, v1: int, v2: int) -> bool:
        return any(v2 == viz for viz, _ in self.adj_list[v1])

    def add_edge(self, v1: int, v2: int, peso: int = 1):
        """
        Adiciona uma aresta de v1 → v2 (ou em ambos os sentidos, se o grafo for não direcionado)
        Se o peso não for informado, assume valor 1.
        """
        if not self.has_edge(v1, v2):
            self.adj_list[v1].append((v2, peso))
            self.num_edges += 1

            # Se o grafo for não direcionado, adiciona o inverso também
            if not self.direcionado and not self.has_edge(v2, v1):
                self.adj_list[v2].append((v1, peso))
                self.num_edges += 1

    def remove_edge(self, v1: int, v2: int):
        for i, (viz, _) in enumerate(self.adj_list[v1]):
            if viz == v2:
                del self.adj_list[v1][i]
                self.num_edges -= 1
                break
        if not self.direcionado:
            for i, (viz, _) in enumerate(self.adj_list[v2]):
                if viz == v1:
                    del self.adj_list[v2][i]
                    self.num_edges -= 1
                    break

    def print_edges(self):
        for v1 in range(self.num_vertices):
            for v2, peso in self.adj_list[v1]:
                print(f"({v1}, {v2}, peso={peso})", end=" ")
            print()

    def print_list(self):
        for v in range(self.num_vertices):
            print(f"{v}: {self.adj_list[v]}")

    