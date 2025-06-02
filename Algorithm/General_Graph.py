from Algorithm.Check_Graph import isTree

def FIND_TRANSACTIONS(V, T):
    transactions = []
    n = 0
    for _ in V['V']:
        n += 1

    V_copy = {'V': [], 'w': []}
    for x in V['V']:
        V_copy['V'].append(x)
    for x in V['w']:
        V_copy['w'].append(x)

    T_copy = {'V': [], 'E': [], 'adj': {}}
    for x in T['V']:
        T_copy['V'].append(x)
    for x in T['E']:
        T_copy['E'].append(x)
    for k in T['adj']:
        T_copy['adj'][k] = []
        for v in T['adj'][k]:
            T_copy['adj'][k].append(v)

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

        start = vertices[0]
        if not dfs(start, -1):
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
    for i in T_copy['V']:
        temp_adj[i] = []
        for x in T_copy['adj'][i]:
            temp_adj[i].append(x)

    remaining_vertices = []
    for x in T_copy['V']:
        remaining_vertices.append(x)

    while len(remaining_vertices) > 1:
        vc = -1
        for node in remaining_vertices:
            count = 0
            for _ in temp_adj[node]:
                count += 1
            if count == 1:
                vc = node
                break
        if vc == -1:
            break
        if len(temp_adj[vc]) > 0:
            vp = temp_adj[vc][0]
        else:
            vp = -1
        if vp == -1:
            break

        amount = V_copy['w'][V_copy['V'].index(vc)]
        if amount > 0:
            transactions.append((vc, vp, amount))
        else:
            transactions.append((vp, vc, -amount))

        idx_vp = V_copy['V'].index(vp)
        idx_vc = V_copy['V'].index(vc)
        V_copy['w'][idx_vp] += V_copy['w'][idx_vc]

        temp_adj[vp] = [x for x in temp_adj[vp] if x != vc]
        temp_adj[vc] = [x for x in temp_adj[vc] if x != vp]

        remaining_vertices = [x for x in remaining_vertices if x != vc]

    return transactions
