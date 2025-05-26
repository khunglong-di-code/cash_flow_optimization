from collections import defaultdict, deque

class Vertex:
    def __init__(self, name, debt):
        self.name = name
        self.debt = debt
        self.children = []
        self.parent = None

def read_graph(filepath):
    vertices = {}
    edges = []
    with open(filepath, "r") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    for line in lines:
        parts = line.split()
        if len(parts) == 2 and parts[1].lstrip('-').isdigit():
            name, debt = parts
            vertices[name] = Vertex(name, int(debt))
        elif len(parts) == 2:
            edges.append((parts[0], parts[1]))

    return vertices, edges

def is_tree(n, edges):
    if len(edges) != n - 1:
        return False
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()
    queue = deque([edges[0][0]])  

    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                queue.append(neighbor)

    return len(visited) == n

def build_spanning_tree(vertices_dict, edges):
    visited = set()
    root_name = next(iter(vertices_dict))
    root = vertices_dict[root_name]
    queue = deque([root])
    visited.add(root_name)

    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    while queue:
        current = queue.popleft()
        for neighbor_name in graph[current.name]:
            if neighbor_name not in visited:
                child = vertices_dict[neighbor_name]
                current.children.append(child)
                child.parent = current
                visited.add(neighbor_name)
                queue.append(child)

    return root

def FindTransactions(vertices, T_root):
    transactions = []

    def settle(vertex):
        if not vertex.children:
            if vertex.parent is None:
                assert vertex.debt == 0
                return
            transactions.append((vertex.name, vertex.parent.name, vertex.debt))
            vertex.parent.debt += vertex.debt
            vertex.debt = 0
        else:
            for child in vertex.children:
                settle(child)
            if vertex.parent is not None:
                transactions.append((vertex.name, vertex.parent.name, vertex.debt))
                vertex.parent.debt += vertex.debt
                vertex.debt = 0
            else:
                assert vertex.debt == 0

    settle(T_root)
    return [t for t in transactions if t[2] != 0]

if __name__ == "__main__":
    filepath = "graph.txt"  
    vertices, edges = read_graph(filepath)
    n = len(vertices)

    if is_tree(n, edges):
        print("Do thi la mot cay.")
        T_root = build_spanning_tree(vertices, edges)
    else:
        print("Do thi khong phai  mot cay. Giai theo huong do thi tong quat.")
        T_root = build_spanning_tree(vertices, edges)

    transactions = FindTransactions(list(vertices.values()), T_root)
    for frm, to, amt in transactions:
        if amt < 0:
            print(f"{to} -> {frm}: {-amt}")
        else:
            print(f"{frm} -> {to}: {amt}")
