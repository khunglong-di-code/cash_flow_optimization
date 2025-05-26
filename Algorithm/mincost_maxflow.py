from collections import deque

class Edge:
    def __init__(self, to, rev, capacity, cost):
        self.to = to
        self.rev = rev
        self.capacity = capacity
        self.cost = cost

class EdmondsKarp:
    def __init__(self, N):
        self.N = N
        self.graph = [[] for _ in range(N)]

    def add_edge(self, fr, to, capacity):
        forward = Edge(to, len(self.graph[to]), capacity, 0)
        backward = Edge(fr, len(self.graph[fr]), 0, 0)
        self.graph[fr].append(forward)
        self.graph[to].append(backward)

    def bfs(self, s, t, parent):
        visited = [False] * self.N
        queue = deque([s])
        visited[s] = True

        while queue:
            u = queue.popleft()
            for i, edge in enumerate(self.graph[u]):
                if not visited[edge.to] and edge.capacity > 0:
                    visited[edge.to] = True
                    parent[edge.to] = (u, i)
                    if edge.to == t:
                        return True
                    queue.append(edge.to)
        return False

    def max_flow(self, s, t):
        parent = [None] * self.N
        max_flow = 0

        while self.bfs(s, t, parent):
            path_flow = float('Inf')
            v = t
            while v != s:
                u, idx = parent[v]
                path_flow = min(path_flow, self.graph[u][idx].capacity)
                v = u

            max_flow += path_flow
            v = t
            while v != s:
                u, idx = parent[v]
                self.graph[u][idx].capacity -= path_flow
                self.graph[v][self.graph[u][idx].rev].capacity += path_flow
                v = u

        return max_flow

# Example usage:
if __name__ == "__main__":
    N = 6  # Number of vertices
    ek = EdmondsKarp(N)
    # Add edges: from, to, capacity
    ek.add_edge(0, 1, 16)
    ek.add_edge(0, 2, 13)
    ek.add_edge(1, 2, 10)
    ek.add_edge(1, 3, 12)
    ek.add_edge(2, 1, 4)
    ek.add_edge(2, 4, 14)
    ek.add_edge(3, 2, 9)
    ek.add_edge(3, 5, 20)
    ek.add_edge(4, 3, 7)
    ek.add_edge(4, 5, 4)

    s = 0  # Source
    t = 5  # Sink

    flow = ek.max_flow(s, t)
    print("Maximum flow:", flow)
