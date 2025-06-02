def FIND_TRANSACTIONS(V, T):
    transactions = []
    n = len(V['V'])
    V_copy = {'V': list(V['V']), 'w': list(V['w'])}
    T_copy = {
        'V': list(T['V']),
        'E': list(T['E']),
        'adj': {k: list(v) for k, v in T['adj'].items()}
    }
    if not isTree(T_copy['V'], T_copy['adj']):
        # Tạo cây khung bằng DFS
        visited = [False] * n
        spanning_tree_edges = []
        new_adj = {i: [] for i in range(n)}
        
        def DFS(u):
            visited[u] = True
            for v in T_copy['adj'][u]:
                if not visited[v]:
                    spanning_tree_edges.append((u, v))
                    new_adj[u].append(v)
                    new_adj[v].append(u)
                    DFS(v)
        
        DFS(T_copy['V'][0])
        
        # Cập nhật lại T thành cây khung
        T_copy['E'] = spanning_tree_edges
        T_copy['adj'] = new_adj

    parent = [-1] * n
    def set_parents(u, p):
        parent[u] = p
        for v in T_copy['adj'][u]:
            if v != p:
                set_parents(v, u)
    set_parents(T_copy['V'][0], -1)

    temp_adj = {i: list(T_copy['adj'][i]) for i in T_copy['V']}
    remaining_vertices = set(T_copy['V'])

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
        amount = abs(V_copy['w'][vc])
        if V_copy['w'][vc] > 0:
            transactions.append((vc, vp, amount))
        else:
            transactions.append((vp, vc, amount))
        V_copy['w'][vp] += V_copy['w'][vc]
        temp_adj[vp].remove(vc)
        temp_adj[vc].remove(vp)
        remaining_vertices.remove(vc)
    return transactions
