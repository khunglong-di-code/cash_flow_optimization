from Algorithm.Check_Graph import isTree

def FIND_TRANSACTIONS(V, T):
    transactions = []

    if not isTree(T):
        visited = [False for _ in range(len(T['V']))]
        parent = [-1 for _ in range(len(T['V']))]
        deg = [0 for _ in range(len(T['V']))]
        spanning_tree_edges = []

        def DFS(u):
            visited[u] = True
            for v in T['adj'][u]:
                if not visited[v]:
                    parent[v] = u
                    deg[u] += 1
                    deg[v] += 1
                    spanning_tree_edges.append((u, v))
                    DFS(v)

        for node in T['V']:
            if not visited[node]:
                DFS(node)

        T = {
            'V': T['V'][:],
            'E': spanning_tree_edges,
            'adj': {i: [] for i in T['V']}
        }
        for u, v in spanning_tree_edges:
            T['adj'][u].append(v)
            T['adj'][v].append(u)

    else:
        parent = [-1 for _ in range(len(T['V']))]
        def set_parents(u, p):
            parent[u] = p
            for v in T['adj'][u]:
                if v != p:
                    set_parents(v, u)
        set_parents(0, -1)

    while len(T['V']) > 1:
        vc = -1
        for node in T['V']:
            if len(T['adj'][node]) == 1:
                vc = node
                break

        vp = parent[vc]

        if V['w'][vc] > 0:
            transactions.append((vc, vp, abs(V['w'][vc])))
        else:
            transactions.append((vp, vc, abs(V['w'][vc])))

        V['w'][vp] += V['w'][vc]

        T['adj'][vp].remove(vc)
        T['adj'][vc].remove(vp)
        T['V'].remove(vc)
        T['E'] = [(u, v) for (u, v) in T['E'] if not (u == vc or v == vc)]

    return transactions
