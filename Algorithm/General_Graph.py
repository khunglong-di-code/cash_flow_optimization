from Algorithm.Check_Graph import isTree

def FIND_TRANSACTIONS(V, T):
    transactions = []
    n = 0
    for _ in V['V']:
        n += 1

    V_copy_w = []
    i = 0
    while i < n:
        V_copy_w.append(V['w'][i])
        i += 1

    T_copy_V = []
    i = 0
    while i < n:
        T_copy_V.append(V['V'][i])
        i += 1

    T_copy_E = []
    i = 0
    while i < len(T['E']):
        T_copy_E.append(T['E'][i])
        i += 1

    T_copy_adj = {}
    keys = []
    for key in T['adj']:
        keys.append(key)

    for key_i in range(len(keys)):
        key = keys[key_i]
        adj_list = []
        vals = T['adj'][key]
        j = 0
        while j < len(vals):
            adj_list.append(vals[j])
            j += 1
        T_copy_adj[key] = adj_list

    if not isTree(T_copy_V, T_copy_adj):
        visited = {}
        for i in range(n):
            visited[T_copy_V[i]] = False

        spanning_tree_edges = []
        new_adj = {}
        for i in range(n):
            new_adj[T_copy_V[i]] = []

        def DFS(u):
            visited[u] = True
            neighbors = T_copy_adj[u]
            j = 0
            while j < len(neighbors):
                v = neighbors[j]
                if not visited[v]:
                    spanning_tree_edges.append((u, v))
                    new_adj[u].append(v)
                    new_adj[v].append(u)
                    DFS(v)
                j += 1

        DFS(T_copy_V[0])

        T_copy_E = spanning_tree_edges
        T_copy_adj = new_adj

    parent = {}
    for i in range(n):
        parent[T_copy_V[i]] = -1

    def set_parents(u, p):
        parent[u] = p
        neighbors = T_copy_adj[u]
        j = 0
        while j < len(neighbors):
            v = neighbors[j]
            if v != p:
                set_parents(v, u)
            j += 1

    set_parents(T_copy_V[0], -1)

    temp_adj = {}
    for i in range(n):
        node = T_copy_V[i]
        adj_list = []
        neighbors = T_copy_adj[node]
        j = 0
        while j < len(neighbors):
            adj_list.append(neighbors[j])
            j += 1
        temp_adj[node] = adj_list

    remaining_vertices = []
    for i in range(n):
        remaining_vertices.append(T_copy_V[i])

    w = {}
    for i in range(n):
        node = T_copy_V[i]
        w[node] = V_copy_w[i]

    while True:
        vc = None
        i = 0
        length_remaining = 0
        while i < len(remaining_vertices):
            length_remaining += 1
            i += 1

        i = 0
        while i < length_remaining:
            node = remaining_vertices[i]
            if len(temp_adj[node]) == 1:
                vc = node
                break
            i += 1
        if vc is None:
            break

        if len(temp_adj[vc]) == 0:
            break

        vp = temp_adj[vc][0]

        amount = w[vc]
        if amount < 0:
            amount = -amount

        if w[vc] > 0:
            transactions.append((vc, vp, amount))
        else:
            transactions.append((vp, vc, amount))

        w[vp] += w[vc]

        new_adj_vp = []
        j = 0
        while j < len(temp_adj[vp]):
            if temp_adj[vp][j] != vc:
                new_adj_vp.append(temp_adj[vp][j])
            j += 1
        temp_adj[vp] = new_adj_vp

        new_adj_vc = []
        j = 0
        while j < len(temp_adj[vc]):
            if temp_adj[vc][j] != vp:
                new_adj_vc.append(temp_adj[vc][j])
            j += 1
        temp_adj[vc] = new_adj_vc

        new_remaining = []
        i = 0
        while i < len(remaining_vertices):
            if remaining_vertices[i] != vc:
                new_remaining.append(remaining_vertices[i])
            i += 1
        remaining_vertices = new_remaining

        if len(remaining_vertices) <= 1:
            break

    return transactions
