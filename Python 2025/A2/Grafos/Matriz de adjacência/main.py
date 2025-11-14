from graph_matrix import *
from funcoes import *
from dfs import *

# ======================
# 1. BASIC GRAPH TESTS
# ======================
print("=== BASIC GRAPH TESTS ===")

# Create empty graph
g1 = GraphMatrix(6)
print("Empty graph matrix:")
g1.print_matriz()
print("###############################")

# Add edges
g1.add_edge(0, 1)
g1.add_edge(0, 2)
g1.add_edge(1, 3)
g1.add_edge(1, 4)
g1.add_edge(2, 4)
g1.add_edge(3, 4)
g1.add_edge(4, 5)
g1.add_edge(4, 1)  # Duplicate edge

print("Matrix after adding edges:")
g1.print_matriz()
print("###############################")

# Test edge removal
print("Edge removal test:")
print(f"Has edge (4,5)? {g1.has_edge(4,5)}")
g1.remove_edges(4,5)
print(f"Has edge (4,5) after removal? {g1.has_edge(4,5)}")
print("###############################")

# Show final matrix and edge list
print("Final matrix:")
g1.print_matriz()
print("###############################")
print("Edge list:")
g1.print_edges()

# ======================
# 2. SUBGRAPH TESTS
# ======================
print("\n=== SUBGRAPH TESTS ===")

# Create graphs for subgraph testing
g2 = GraphMatrix(6)
g2.add_edge(0, 1)
g2.add_edge(1, 2)

g3 = GraphMatrix(4)
g3.add_edge(0, 1)
g3.add_edge(1, 2)
g3.add_edge(2, 3)
g3.add_edge(0, 3)

g4 = GraphMatrix(4)
g4.add_edge(0, 1)
g4.add_edge(1, 2)

# Test subgraph relationships
print(f"g2 is subgraph of g1? {is_subgraph(g1, g2)}")
print(f"g4 is subgraph of g3? {is_subgraph(g3, g4)}")

# ======================
# 3. PATH TESTS
# ======================
print("\n=== PATH TESTS ===")

g5 = GraphMatrix(5)
g5.add_edge(0, 1)
g5.add_edge(1, 2)
g5.add_edge(2, 3)
g5.add_edge(3, 4)

# Test different paths
print("Path tests on g5:")
print(f"Path [0, 1, 2, 3] (valid and simple): {is_path(g5, [0, 1, 2, 3])}")
print(f"Path [0, 1, 2, 1, 2] (valid, not simple): {is_path(g5, [0, 1, 2, 1, 2])}")
print(f"Path [0, 1, 2, 3, 1] (invalid): {is_path(g5, [0, 1, 2, 3, 1])}")

# ======================
# 4. DFS TESTS
# ======================
print("\n=== DFS TESTS ===")

# DFS on normal graph
g6 = GraphMatrix(5)
g6.add_edge(0, 1)
g6.add_edge(0, 2)
g6.add_edge(1, 3)
g6.add_edge(3, 4)

print("DFS on g6 (default start):")
dfs(g6)

# DFS with specific start vertex
g7 = GraphMatrix(3)
g7.add_edge(0, 1)
g7.add_edge(1, 2)

print("\nDFS on g7 (starting at vertex 1):")
dfs(g7, start_vertex=1)

# DFS on cyclic graph
g8 = GraphMatrix(6)
g8.add_edge(0, 1)
g8.add_edge(1, 2)
g8.add_edge(2, 3)
g8.add_edge(3, 4)
g8.add_edge(4, 5)
g8.add_edge(5, 0)  # Creates cycle

print("\nDFS on g8 (graph with cycle):")
dfs(g8)

# ======================
# 5. TOPOLOGICAL SORTING TESTS
# ======================
print("\n=== TOPOLOGICAL SORTING TESTS ===")

# Test acyclic graph
g9 = GraphMatrix(4)
g9.add_edge(0, 1)
g9.add_edge(1, 2)
g9.add_edge(2, 3)

print(f"g9 is topological? {is_topological(g9)}")

# Add cycle and test again
g9.add_edge(3, 1)
print(f"g9 with cycle is topological? {is_topological(g9)}")

# Complete topological order test
g10 = GraphMatrix(6)
g10.add_edge(5, 2)
g10.add_edge(5, 0)
g10.add_edge(4, 0)
g10.add_edge(4, 1)
g10.add_edge(2, 3)
g10.add_edge(3, 1)

g11 = GraphMatrix(3)
g11.add_edge(0, 1)
g11.add_edge(1, 2)
g11.add_edge(2, 0)  # Creates cycle

print("\nTopological order tests:")
has_order, order = has_topological_order(g10)
print(f"g10 has topological order? {has_order}")
print(f"Topological order of g10: {order}")

has_order, order = has_topological_order(g11)
print(f"g11 has topological order? {has_order}")
print(f"Topological order of g11: {order}")