def FindTransactions(V, T):
    V_w = V.copy()
    nodes = set(V_w.keys())
    transactions = []

    def find_leaf_node():
        children_count = dict((node, 0) for node in nodes)
        for node in nodes:
            p = T[node]
            if p is not None and p in nodes:
                children_count[p] += 1
        for node in nodes:
            if children_count[node] == 0 and T[node] is not None:
                return node
        return None

    while True:
        if len(nodes) == 1:
            root = next(iter(nodes))
            assert abs(V_w[root]) < 1e-9, "Residual debt not zero at root."
            break

        vc = find_leaf_node()
        if vc is None:
            break
        vp = T[vc]
        transaction_amount = V_w[vc]
        transactions.append((vc, vp, transaction_amount))
        V_w[vp] += V_w[vc]
        nodes.remove(vc)
        del V_w[vc]

    transactions = [t for t in transactions if abs(t[2]) > 1e-9]
    return transactions

def build_spanning_tree(G, root):
    visited = {}
    parent = {}
    for node in G:
        visited[node] = False
        parent[node] = None

    stack = [root]
    visited[root] = True

    while stack:
        current = stack.pop()
        for neighbor in G[current]:
            if not visited[neighbor]:
                visited[neighbor] = True
                parent[neighbor] = current
                stack.append(neighbor)
    return parent

def main():
    n = int(input().strip())
    V = {}
    vertices_order = []
    for _ in range(n):
        line = input().strip().split()
        vertex = line[0]
        weight = float(line[1])
        V[vertex] = weight
        vertices_order.append(vertex)

    m = int(input().strip())
    G = {}
    for v in V:
        G[v] = []
    for _ in range(m):
        u, v = input().strip().split()
        G[u].append(v)
        G[v].append(u)

    root = vertices_order[0]
    T = build_spanning_tree(G, root)
    transactions = FindTransactions(V, T)

    print("Transactions (vc -> vp : amount):")
    for (vc, vp, amount) in transactions:
        if amount < 0:
            print(f"{vp} pays {vc} ${-amount:.2f}")
        else:
            print(f"{vc} pays {vp} ${amount:.2f}")

if __name__ == "__main__":
    main()
