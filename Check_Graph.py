def readGraph(filename):
    
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    vertex_line = ""
    for line in lines:
        if "Tập hợp đỉnh" in line:
            vertex_line = lines[lines.index(line) + 1].strip()
            break

    edge_line = ""
    for line in lines:
        if "Tập hợp cạnh" in line:
            edge_line = lines[lines.index(line) + 1].strip()
            break

    vertex_data = eval(vertex_line)
    edge_data = eval(edge_line)

    return vertex_data, edge_data

def isConnect(vertex_data, edge_data):

    n = len(vertex_data)
    visited = [0] * n
    stack = [0]

    while stack:
        u = stack.pop()
        if not visited[u]:
            visited[u] = 1
            for v in edge_data[u]:
                if not visited[v]:
                    stack.append(v)

    return all(visited)

def isTree(vertex_data, edge_data):
    if not isConnect(vertex_data, edge_data):
        return False
    
    n = len(vertex_data)
    edge_count = 0
    for neighbors in edge_data:
        edge_count += len(neighbors)
    edge_count //= 2 

    if edge_count != n - 1:
        return False

    visited = [0] * n
    parent = [-1] * n
    stack = [0]

    while stack:
        u = stack.pop()
        if not visited[u]:
            visited[u] = 1
            for v in edge_data[u]:
                if not visited[v]:
                    parent[v] = u
                    stack.append(v)
                elif v != parent[u]:
                    return False  
    return True

def isComplete(vertex_data, edge_data):
    if not isConnect(vertex_data, edge_data):
        return False
    
    n = len(vertex_data)

    for i in range(n):
        for j in range(i + 1, n):
            if j not in edge_data[i] or i not in edge_data[j]:
                return False

    return True

def complete_set(vertex_data):
    
    debts = []
    subset = []

    for item in vertex_data:
        subset.append(item[0])
        debts.append(item[1])

    return debts, subset

def isGrid(vertex_data, edge_data):
    if not isConnect(vertex_data, edge_data):
        return False

    n = len(vertex_data)

    for r in range(1, n + 1):
        if n % r != 0:
            continue
        c = n // r

        ok = True
        for i in range(n):
            expected_neighbors = []
            row = i // c
            col = i % c

            if row > 0:
                expected_neighbors.append(i - c)
            if row < r - 1:
                expected_neighbors.append(i + c)
            if col > 0:
                expected_neighbors.append(i - 1)
            if col < c - 1:
                expected_neighbors.append(i + 1)

            actual_neighbors = edge_data[i]

            for v in expected_neighbors:
                if v not in actual_neighbors:
                    ok = False
                    break
                if i not in edge_data[v]:
                    ok = False
                    break

            if not ok:
                break

        if ok:
            return True

    return False

def grid_set(vertex_data):
    weights = [v[1] for v in vertex_data]
    n = len(weights)

    for r in range(1, n + 1):
        if n % r != 0:
            continue
        c = n // r
        grid = []
        ok = True
        for i in range(r):
            row = []
            for j in range(c):
                index = i * c + j
                row.append(weights[index])
            grid.append(row)
        return r, c, grid
