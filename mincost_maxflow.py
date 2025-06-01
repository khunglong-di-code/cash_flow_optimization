INF = float('inf')

class MinHeap:
    def __init__(self):
        self.heap = []
    
    def push(self, item):
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)
    
    def pop(self):
        if len(self.heap) == 1:
            return self.heap.pop()
        
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root
    
    def empty(self):
        return len(self.heap) == 0
    
    def _heapify_up(self, idx):
        parent = (idx - 1) // 2
        if idx > 0 and self.heap[idx] < self.heap[parent]:
            self.heap[idx], self.heap[parent] = self.heap[parent], self.heap[idx]
            self._heapify_up(parent)
    
    def _heapify_down(self, idx):
        left = 2 * idx + 1
        right = 2 * idx + 2
        smallest = idx
        
        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left
        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right
        
        if smallest != idx:
            self.heap[idx], self.heap[smallest] = self.heap[smallest], self.heap[idx]
            self._heapify_down(smallest)

class Queue:
    def __init__(self):
        self.items = []
        self.front = 0
    
    def append(self, item):
        self.items.append(item)
    
    def popleft(self):
        item = self.items[self.front]
        self.front += 1
        # Reset nếu queue trống để tiết kiệm bộ nhớ
        if self.front == len(self.items):
            self.items = []
            self.front = 0
        return item
    
    def empty(self):
        return self.front >= len(self.items)

class Edge:
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
        """Hàm tự định nghĩa thay thế enumerate()"""
        index = start
        for value in iterable:
            yield index, value
            index += 1
    
    def add_edge(self, u, v, cap, cost):
        self.adj[u].append(Edge(v, len(self.adj[v]), cap, cost))
        self.adj[v].append(Edge(u, len(self.adj[u]) - 1, 0, -cost))
    
    def spfa(self, s):
        self.dist = [INF] * self.V
        self.pre = [-1] * self.V
        in_queue = [False] * self.V
        q = Queue()  # Sử dụng Queue tự định nghĩa
        
        self.dist[s] = 0
        q.append(s)
        in_queue[s] = True
        
        while not q.empty():
            u = q.popleft()
            in_queue[u] = False
            
            for i, e in self.my_enumerate(self.adj[u]):
                if e.cap > e.flow:
                    v = e.to
                    if self.dist[v] > self.dist[u] + e.cost:
                        self.dist[v] = self.dist[u] + e.cost
                        self.pre[v] = i
                        self.prev_node[v] = u
                        if not in_queue[v]:
                            q.append(v)
                            in_queue[v] = True
    
    def dijkstra(self, s):
        self.dist = [INF] * self.V
        self.pre = [-1] * self.V
        self.prev_node = [-1] * self.V
        self.vis = [False] * self.V
        
        self.dist[s] = 0
        pq = MinHeap()  # Sử dụng MinHeap tự định nghĩa
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
    
    def reweight(self):
        for u in range(self.V):
            for e in self.adj[u]:
                e.cost += self.dist[u] - self.dist[e.to]
    
    def calc(self, s, t):
        self.spfa(s)
        total_flow = 0
        total_cost = 0
        fcost = self.dist[t]
        
        while True:
            self.reweight()
            self.dijkstra(s)
            
            if self.pre[t] == -1:
                break
            
            fcost += self.dist[t]
            flow = INF
            v = t
            
            while v != s:
                u = self.prev_node[v]
                e = self.adj[u][self.pre[v]]
                flow = min(flow, e.cap - e.flow)
                v = u
            
            v = t
            while v != s:
                u = self.prev_node[v]
                e = self.adj[u][self.pre[v]]
                e.flow += flow
                self.adj[e.to][e.rev].flow -= flow
                v = u
            
            total_flow += flow
            total_cost += flow * fcost
        
        return total_flow, total_cost

def solve_debt_settling(vertices, adj_lists):
    """
    Giải bài toán debt settling bằng Min-Cost Max Flow
    
    Args:
        vertices: List [[node_id, balance], ...] 
        adj_lists: List of adjacency lists cho từng đỉnh
    
    Returns:
        max_flow, min_cost, transactions
    """
    
    n = len(vertices)  # Số đỉnh gốc
    
    # Tạo đồ thị mới: n đỉnh gốc + source (n) + sink (n+1)
    source = n      # đỉnh 20
    sink = n + 1    # đỉnh 21
    total_nodes = n + 2  # 22 đỉnh tổng cộng
    
    # Khởi tạo Min-Cost Max Flow
    mcmf = MinCostMaxFlow(total_nodes)
    
    # Bước 1: Thêm cạnh từ source và đến sink
    total_positive = 0
    total_negative = 0
    
    for i in range(n):
        node_id = vertices[i][0]
        balance = vertices[i][1]
        
        if balance > 0:  # Đỉnh nợ (cần trả tiền)
            mcmf.add_edge(source, node_id, balance, 0)
            total_positive += balance
        elif balance < 0:  # Đỉnh cho vay (cần nhận tiền)
            mcmf.add_edge(node_id, sink, -balance, 0)
            total_negative += (-balance)
    
    # Bước 2: Thêm các cạnh gốc với capacity vô hạn, cost = 1
    for i in range(n):
        node_id = vertices[i][0]
        neighbors = adj_lists[i]
        for neighbor in neighbors:
            # Thêm cạnh từ node_id đến neighbor với capacity vô hạn, cost = 1
            mcmf.add_edge(node_id, neighbor, INF, 1)
    
    # Bước 3: Tính Min-Cost Max Flow
    max_flow, min_cost = mcmf.calc(source, sink)
    
    # Bước 4: Trích xuất các giao dịch
    transactions = []
    
    for u in range(n):
        for edge in mcmf.adj[u]:
            # Chỉ xét cạnh có flow > 0 và không phải cạnh đến source/sink
            if edge.flow > 0 and edge.to != source and edge.to != sink and u != source and u != sink:
                transactions.append([u, edge.to, edge.flow])
    
    # In kết quả
    
    return transactions

# Chạy thuật toán với dữ liệu mẫu
if __name__ == "__main__":
    # Dữ liệu mẫu
    sample_vertices = [[0, 17652684], [1, 8130897], [2, 950600], [3, 31893719], [4, -1524840], 
                       [5, 2620968], [6, -8991864], [7, -9136731], [8, -25377808], [9, 15611920], 
                       [10, -22597256], [11, -19072822], [12, -10505176], [13, -1024932], [14, 16571429], 
                       [15, 11856578], [16, 2212217], [17, 21079211], [18, -29688096], [19, -660698]]
    
    sample_adj_lists = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 
                        [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 
                        [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 
                        [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 
                        [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 
                        [0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 
                        [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 
                        [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 
                        [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 
                        [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19], 
                        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19], 
                        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19], 
                        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19], 
                        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19], 
                        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19], 
                        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19], 
                        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19], 
                        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19], 
                        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19], 
                        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]]
    
    transactions =   solve_debt_settling(sample_vertices, sample_adj_lists)
    
    for transaction in transactions:
        from_node, to_node, amount = transaction
        print(f"{from_node} -> {to_node}: {amount}")

    print("Số giao dịch tối thiểu: ", len(transactions))