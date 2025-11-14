class GraphMatrix:
    def __init__(self, num_vertices: int):
        self.num_vertices = num_vertices
        self.num_edges = 0

        #Criando a matriz nxn
        self.edges = [[False for _ in range(num_vertices)] for _ in range(num_vertices)] 

    
    def has_edge(self, v1: int, v2: int) -> bool:
        return self.edges[v1][v2]
        
    def add_edge(self, v1: int, v2: int):
        if not self.has_edge(v1, v2):
            self.edges[v1][v2] = True
            self.num_edges +=1

    def remove_edges(self, v1: int, v2: int):
        if self.has_edge(v1,v2):
            self.edges[v1][v2] = False
            self.num_edges -= 1       

    def print_edges(self):
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                if self.has_edge(i,j):
                    print(f"({i}, {j})", end = " " ) #qualquer coisa dentro das chaves {} será avaliada e substituída pelo valor da variável correspondente
            print()  #quebra de linha       

    def print_matriz(self):
        for i in range(self.num_vertices):
            for j in range(self.num_vertices):
                print( 1 if self.has_edge(i,j) else 0, end = " ")
            print()    

