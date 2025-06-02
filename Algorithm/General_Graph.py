from Algorithm.Check_Graph import isTree

def FIND_TRANSACTIONS(V, T):
    transactions = []
    vertices = V['V']
    weights = V['w']
    n = 0
    for _ in vertices:
        n += 1

    V_copy_V = []
    for i in range(n):
        V_copy_V.append(vertices[i])
    V_copy_w = []
    for i in range(n):
        V_copy_w.append(weights[i])
        
    T_copy_V = []
    for i in range(n):
        T_copy_V.append(vertices[i])
    
    T_copy_adj = {}
    keys = []
    for k in T:
        keys.append(k)
    for k in keys:
        neighbors = T[k]
        new_neighbors = []
        for i in range(len(neighbors)):
            new_neighbors.append(neighbors[i])
        T_copy_adj[k] = new_neighbors

    visited = {}
    for i in range(n):
        visited[vertices[i]] = False

    spanning_tree_edges = []
    new_adj = {}
    for i in range(n):
        new_adj[vertices[i]] = []

    def DFS(u):
        visited[u] = True
        neighbors = T_copy_adj[u]
        m = 0
        for _ in neighbors:
            m += 1
        for i in range(m):
            v = neighbors[i]
            if not visited[v]:
                spanning_tree_edges.append((u, v))
                new_adj[u].append(v)
                new_adj[v].append(u)
                DFS(v)

    DFS(vertices[0])

    T_copy_adj = new_adj
    T_copy_V = vertices

    parent = {}
    for i in range(n):
        parent[vertices[i]] = None

    def set_parents(u, p):
        parent[u] = p
        neighbors = T_copy_adj[u]
        m = 0
        for _ in neighbors:
            m += 1
        for i in range(m):
            v = neighbors[i]
            if v != p:
                set_parents(v, u)

    set_parents(vertices[0], None)

    temp_adj = {}
    for i in range(n):
        u = vertices[i]
        neighbors = T_copy_adj[u]
        new_neighbors = []
        m = 0
        for _ in neighbors:
            m += 1
        for j in range(m):
            new_neighbors.append(neighbors[j])
        temp_adj[u] = new_neighbors

    remaining_vertices = []
    for i in range(n):
        remaining_vertices.append(vertices[i])

    while True:
        length = 0
        for _ in remaining_vertices:
            length += 1
        if length <= 1:
            break
        
        vc = None
        found = False
        for i in range(length):
            node = remaining_vertices[i]
            neighbors = temp_adj[node]
            deg = 0
            for _ in neighbors:
                deg += 1
            if deg == 1:
                vc = node
                found = True
                break
        
        if not found:
            break
        
        neighbors_vc = temp_adj[vc]
        deg_vc = 0
        for _ in neighbors_vc:
            deg_vc += 1
        if deg_vc == 0:
            break
        
        vp = neighbors_vc[0]

        w_vc = 0
        for i in range(n):
            if vertices[i] == vc:
                w_vc = V_copy_w[i]
                break
        
        if w_vc < 0:
            amount = -w_vc
        else:
            amount = w_vc

        idx_vp = -1
        idx_vc = -1
        for i in range(n):
            if vertices[i] == vp:
                idx_vp = i
            if vertices[i] == vc:
                idx_vc = i

        if idx_vp == -1 or idx_vc == -1:
            break

        if V_copy_w[idx_vc] > 0:
            transactions.append((vc, vp, amount))
        else:
            transactions.append((vp, vc, amount))
        
        V_copy_w[idx_vp] = V_copy_w[idx_vp] + V_copy_w[idx_vc]

        new_list = []
        neighbors_vp = temp_adj[vp]
        for i in range(len(neighbors_vp)):
            if neighbors_vp[i] != vc:
                new_list.append(neighbors_vp[i])
        temp_adj[vp] = new_list

        temp_adj[vc] = []

        new_remaining = []
        for i in range(len(remaining_vertices)):
            if remaining_vertices[i] != vc:
                new_remaining.append(remaining_vertices[i])
        remaining_vertices = new_remaining

    return transactions
