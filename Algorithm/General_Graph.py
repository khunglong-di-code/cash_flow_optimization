from Algorithm.Check_Graph import isTree

def FIND_TRANSACTIONS(vertex_data, edge_data):
    V = {'V': [], 'w': []}
    i = 0
    while i < 1000:  
        if i >= len(vertex_data):
            break
        V['V'] += [vertex_data[i]]
        V['w'] += [0]
        i += 1

    T = {'V': [], 'E': [], 'adj': {}}
    i = 0
    while i < len(vertex_data):
        T['V'] += [vertex_data[i]]
        T['adj'][vertex_data[i]] = []
        i += 1

    i = 0
    while i < len(edge_data):
        u = edge_data[i][0]
        v = edge_data[i][1]
        w = edge_data[i][2]

        T['E'] += [(u, v)]
        T['adj'][u] += [v]

        j = 0
        while j < len(V['V']):
            if V['V'][j] == u:
                V['w'][j] = V['w'][j] - w
            if V['V'][j] == v:
                V['w'][j] = V['w'][j] + w
            j += 1
        i += 1

    transactions = []
    n = len(V['V'])

    V_copy = {'V': [], 'w': []}
    i = 0
    while i < n:
        V_copy['V'] += [V['V'][i]]
        V_copy['w'] += [V['w'][i]]
        i += 1

    T_copy = {'V': [], 'E': [], 'adj': {}}
    i = 0
    while i < len(T['V']):
        T_copy['V'] += [T['V'][i]]
        T_copy['adj'][T['V'][i]] = []
        i += 1
    i = 0
    while i < len(T['E']):
        T_copy['E'] += [T['E'][i]]
        i += 1
    for k in T['adj']:
        T_copy['adj'][k] = []
        j = 0
        while j < len(T['adj'][k]):
            T_copy['adj'][k] += [T['adj'][k][j]]
            j += 1

    def isTree(vertices, adj):
        visited = {}
        for v in vertices:
            visited[v] = False

        def dfs(u, parent):
            visited[u] = True
            i = 0
            while i < len(adj[u]):
                w = adj[u][i]
                if visited[w] == False:
                    if not dfs(w, u):
                        return False
                elif w != parent:
                    return False
                i += 1
            return True

        if not dfs(vertices[0], -1):
            return False

        for v in visited:
            if visited[v] == False:
                return False
        return True

    if not isTree(T_copy['V'], T_copy['adj']):
        visited = {}
        i = 0
        while i < len(T_copy['V']):
            visited[T_copy['V'][i]] = False
            i += 1
        spanning_tree_edges = []
        new_adj = {}
        i = 0
        while i < len(T_copy['V']):
            new_adj[T_copy['V'][i]] = []
            i += 1

        def DFS(u):
            visited[u] = True
            i = 0
            while i < len(T_copy['adj'][u]):
                v = T_copy['adj'][u][i]
                if visited[v] == False:
                    spanning_tree_edges += [(u, v)]
                    new_adj[u] += [v]
                    new_adj[v] += [u]
                    DFS(v)
                i += 1

        DFS(T_copy['V'][0])
        T_copy['E'] = spanning_tree_edges
        T_copy['adj'] = new_adj

    parent = {}
    i = 0
    while i < len(T_copy['V']):
        parent[T_copy['V'][i]] = -1
        i += 1

    def set_parents(u, p):
        parent[u] = p
        i = 0
        while i < len(T_copy['adj'][u]):
            v = T_copy['adj'][u][i]
            if v != p:
                set_parents(v, u)
            i += 1

    set_parents(T_copy['V'][0], -1)

    temp_adj = {}
    i = 0
    while i < len(T_copy['V']):
        u = T_copy['V'][i]
        temp_adj[u] = []
        j = 0
        while j < len(T_copy['adj'][u]):
            temp_adj[u] += [T_copy['adj'][u][j]]
            j += 1
        i += 1

    remaining_vertices = []
    i = 0
    while i < len(T_copy['V']):
        remaining_vertices += [T_copy['V'][i]]
        i += 1

    while True:
        count = 0
        i = 0
        while i < len(remaining_vertices):
            count += 1
            i += 1
        if count <= 1:
            break

        vc = -1
        i = 0
        while i < len(remaining_vertices):
            node = remaining_vertices[i]
            deg = 0
            j = 0
            while j < len(temp_adj[node]):
                deg += 1
                j += 1
            if deg == 1:
                vc = node
                break
            i += 1

        if vc == -1:
            break
        if len(temp_adj[vc]) > 0:
            vp = temp_adj[vc][0]
        else:
            vp = -1
        if vp == -1:
            break

        i = 0
        while i < len(V_copy['V']):
            if V_copy['V'][i] == vc:
                w_vc = V_copy['w'][i]
            i += 1

        if w_vc > 0:
            transactions += [(vc, vp, w_vc)]
        else:
            transactions += [(vp, vc, -w_vc)]

        i = 0
        while i < len(V_copy['V']):
            if V_copy['V'][i] == vp:
                idx_vp = i
            if V_copy['V'][i] == vc:
                idx_vc = i
            i += 1
        V_copy['w'][idx_vp] = V_copy['w'][idx_vp] + V_copy['w'][idx_vc]

        new_temp = []
        i = 0
        while i < len(temp_adj[vp]):
            if temp_adj[vp][i] != vc:
                new_temp += [temp_adj[vp][i]]
            i += 1
        temp_adj[vp] = new_temp

        new_temp = []
        i = 0
        while i < len(temp_adj[vc]):
            if temp_adj[vc][i] != vp:
                new_temp += [temp_adj[vc][i]]
            i += 1
        temp_adj[vc] = new_temp

        new_remaining = []
        i = 0
        while i < len(remaining_vertices):
            if remaining_vertices[i] != vc:
                new_remaining += [remaining_vertices[i]]
            i += 1
        remaining_vertices = new_remaining

    return transactions

