from Algorithm.Check_Graph import isTree

def FIND_TRANSACTIONS(vertex_data, edge_data):
    V = {'V': [], 'w': []}
    for i in range(len(vertex_data)):
        V['V'].append(vertex_data[i][0])
        V['w'].append(0)

    T = {'V': [], 'E': [], 'adj': {}}
    for i in range(len(vertex_data)):
        u = vertex_data[i][0]
        T['V'].append(u)
        T['adj'][u] = []

    for i in range(len(edge_data)):
        u, v, w = edge_data[i]
        T['E'].append((u, v))
        T['adj'][u].append(v)
        for j in range(len(V['V'])):
            if V['V'][j] == u:
                V['w'][j] -= w
            if V['V'][j] == v:
                V['w'][j] += w

    transactions = []
    n = len(V['V'])
    V_copy = {'V': [], 'w': []}
    for i in range(n):
        V_copy['V'].append(V['V'][i])
        V_copy['w'].append(V['w'][i])

    T_copy = {'V': [], 'E': [], 'adj': {}}
    for i in range(len(T['V'])):
        u = T['V'][i]
        T_copy['V'].append(u)
        T_copy['adj'][u] = []
    for i in range(len(T['E'])):
        T_copy['E'].append(T['E'][i])
    for u in T['adj']:
        for v in T['adj'][u]:
            T_copy['adj'][u].append(v)

    def isTree(vertices, adj):
        visited = {}
        for v in vertices:
            visited[v] = False
        def dfs(u, parent):
            visited[u] = True
            for w in adj[u]:
                if not visited[w]:
                    if not dfs(w, u):
                        return False
                elif w != parent:
                    return False
            return True
        if not dfs(vertices[0], -1):
            return False
        for v in visited:
            if not visited[v]:
                return False
        return True

    if not isTree(T_copy['V'], T_copy['adj']):
        visited = {}
        for v in T_copy['V']:
            visited[v] = False
        spanning_tree_edges = []
        new_adj = {}
        for v in T_copy['V']:
            new_adj[v] = []
        def DFS(u):
            visited[u] = True
            for v in T_copy['adj'][u]:
                if not visited[v]:
                    spanning_tree_edges.append((u, v))
                    new_adj[u].append(v)
                    new_adj[v].append(u)
                    DFS(v)
        DFS(T_copy['V'][0])
        T_copy['E'] = spanning_tree_edges
        T_copy['adj'] = new_adj

    parent = {}
    for v in T_copy['V']:
        parent[v] = -1
    def set_parents(u, p):
        parent[u] = p
        for v in T_copy['adj'][u]:
            if v != p:
                set_parents(v, u)
    set_parents(T_copy['V'][0], -1)

    temp_adj = {}
    for u in T_copy['V']:
        temp_adj[u] = []
        for v in T_copy['adj'][u]:
            temp_adj[u].append(v)

    remaining_vertices = []
    for v in T_copy['V']:
        remaining_vertices.append(v)

    while len(remaining_vertices) > 1:
        vc = -1
        for node in remaining_vertices:
            if len(temp_adj[node]) == 1:
                vc = node
                break
        if vc == -1:
            break
        vp = temp_adj[vc][0] if temp_adj[vc] else -1
        if vp == -1:
            break
        for i in range(len(V_copy['V'])):
            if V_copy['V'][i] == vc:
                w_vc = V_copy['w'][i]
        if w_vc > 0:
            transactions.append((vc, vp, w_vc))
        else:
            transactions.append((vp, vc, -w_vc))
        for i in range(len(V_copy['V'])):
            if V_copy['V'][i] == vp:
                idx_vp = i
            if V_copy['V'][i] == vc:
                idx_vc = i
        V_copy['w'][idx_vp] += V_copy['w'][idx_vc]
        temp_adj[vp] = [v for v in temp_adj[vp] if v != vc]
        temp_adj[vc] = [v for v in temp_adj[vc] if v != vp]
        remaining_vertices = [v for v in remaining_vertices if v != vc]

    return transactions
