from Algorithm.Check_Graph import isTree
from Algorithm.Check_Graph import isTree

def FIND_TRANSACTIONS(V, T):
    transactions = []
    vertices = V['V']
    n = len(vertices)
    index_to_node = {i: node for i, node in enumerate(vertices)}
    node_to_index = {node: i for i, node in enumerate(vertices)}
    V_copy_w = [V['w'][i] for i in range(n)]
    T_copy_V = list(vertices)
    T_copy_E = list(T['E'])
    T_copy_adj = {k: list(v) for k, v in T['adj'].items()}
    if not isTree(T_copy_V, T_copy_adj):
        visited = {node: False for node in vertices}
        spanning_tree_edges = []
        new_adj = {node: [] for node in vertices}
        def DFS(u):
            visited[u] = True
            for v in T_copy_adj[u]:
                if not visited[v]:
                    spanning_tree_edges.append((u, v))
                    new_adj[u].append(v)
                    new_adj[v].append(u)
                    DFS(v)
        DFS(vertices[0])
        T_copy_E = spanning_tree_edges
        T_copy_adj = new_adj
    parent = {node: -1 for node in vertices}
    def set_parents(u, p):
        parent[u] = p
        for v in T_copy_adj[u]:
            if v != p:
                set_parents(v, u)
    set_parents(vertices[0], -1)
    temp_adj = {node: list(T_copy_adj[node]) for node in vertices}
    remaining_vertices = set(vertices)
    w = {node: V_copy_w[node_to_index[node]] for node in vertices}
    while len(remaining_vertices) > 1:
        vc = None
        for node in remaining_vertices:
            if len(temp_adj[node]) == 1:
                vc = node
                break
        if vc is None:
            break
        vp = temp_adj[vc][0]
        amount = abs(w[vc])
        if w[vc] > 0:
            transactions.append((vc, vp, amount))
        else:
            transactions.append((vp, vc, amount))
        w[vp] += w[vc]
        temp_adj[vp].remove(vc)
        temp_adj[vc].remove(vp)
        remaining_vertices.remove(vc)
    return transactions

