from Data import *
INF = float('inf')

class Edge_MCMF:
    def __init__(self, to, rev, cap, cost):
        self.to = to
        self.rev = rev
        self.cap = cap
        self.cost = cost
        self.flow = 0

class MinCostMaxFlow:
    def __init__(self, V):
        self.V = V
        self.adj = [[] for _ in range(V)]
        self.dist = [INF] * V
        self.pre = [-1] * V
        self.prev_node = [-1] * V
        self.vis = [False] * V

    def my_enumerate(self, iterable, start=0):
        index = start
        for value in iterable:
            yield index, value
            index += 1

    def add_edge(self, u, v, cap, cost):
        self.adj[u].append(Edge_MCMF(v, len(self.adj[v]), cap, cost))
        self.adj[v].append(Edge_MCMF(u, len(self.adj[u]) - 1, 0, -cost))

    def dijkstra(self, s):
        self.dist = [INF] * self.V
        self.pre = [-1] * self.V
        self.prev_node = [-1] * self.V
        self.vis = [False] * self.V

        self.dist[s] = 0
        pq = MinHeap()
        pq.push((0, s))

        while not pq.empty():
            d, u = pq.pop()
            if self.vis[u]:
                continue
            self.vis[u] = True

            for i, e in self.my_enumerate(self.adj[u]):
                if e.cap > e.flow:
                    v = e.to
                    if self.dist[v] > self.dist[u] + e.cost:
                        self.dist[v] = self.dist[u] + e.cost
                        self.pre[v] = i
                        self.prev_node[v] = u
                        pq.push((self.dist[v], v))

    def calc(self, s, t):
        total_flow = 0
        total_cost = 0

        while True:
            self.dijkstra(s)
            if self.dist[t] == INF:
                break

            flow = INF
            v = t
            while v != s:
                u = self.prev_node[v]
                e = self.adj[u][self.pre[v]]
                if e.cap - e.flow < flow:
                    flow = e.cap - e.flow
                v = u

            v = t
            while v != s:
                u = self.prev_node[v]
                e = self.adj[u][self.pre[v]]
                e.flow += flow
                self.adj[e.to][e.rev].flow -= flow
                v = u

            total_flow += flow
            total_cost += flow * self.dist[t]

        return total_flow, total_cost

def solve_debt_MCMF(vertices, adj_lists):
    n = len(vertices)
    s = n        
    t = n + 1    
    total_nodes = n + 2

    mcmf = MinCostMaxFlow(total_nodes)

    for i in range(n):
        node_id = vertices[i][0]
        balance = vertices[i][1]
        if balance > 0:
            mcmf.add_edge(s, node_id, balance, 0)
        elif balance < 0:
            mcmf.add_edge(node_id, t, -balance, 0)

    for i in range(n):
        node_id = vertices[i][0]
        neighbors = adj_lists[i]
        for neighbor in neighbors:
            mcmf.add_edge(node_id, neighbor, INF, 1)

    max_flow, min_cost = mcmf.calc(s, t)

    transactions = []
    for u in range(n):
        for edge in mcmf.adj[u]:
            if edge.flow > 0 and edge.to != s and edge.to != t and u != s and u != t:
                transactions.append([u, edge.to, edge.flow])

    return transactions