import collections 

class DebtGraph:
    def __init__(self):
        self._vertices: list[Vertex] = []
        self._adj_lists: list[list[int]] = []
        self._next_numeric_id: int = 0

    def add_vertex(self, person_name: str, initial_balance: float) -> int:
        for v_obj in self._vertices:
            if v_obj.get_name() == person_name:
                return v_obj.get_id()
        new_numeric_id = self._next_numeric_id
        new_vertex = Vertex(new_numeric_id, person_name, initial_balance)
        self._vertices.append(new_vertex)
        self._adj_lists.append([])
        self._next_numeric_id += 1
        return new_numeric_id

    def add_edge(self, u_numeric_id: int, v_numeric_id: int, is_undirected: bool = True) -> None:
        num_nodes = len(self._vertices)
        if not (0 <= u_numeric_id < num_nodes and 0 <= v_numeric_id < num_nodes):
            return
        if u_numeric_id == v_numeric_id: #em tránh khuyên ạ
            return

    def get_vertex_by_numeric_id(self, numeric_id: int) -> Vertex | None:
        if 0 <= numeric_id < len(self._vertices):
            return self._vertices[numeric_id]
        return None

    def get_vertex_by_name(self, person_name: str) -> Vertex | None:
        for v_obj in self._vertices:
            if v_obj.get_name() == person_name:
                return v_obj
        return None

    def get_all_vertices(self) -> list[Vertex]:
        return list(self._vertices) 

    def extract_all_net_balances(self) -> list[float]:
        return [v.get_balance() for v in self._vertices]

    def get_vertices_with_balances_for_output(self) -> list[list[int|float]]:
        return [[v.get_id(), v.get_balance()] for v in self._vertices]

    def get_adj_lists_for_output(self) -> list[list[int]]:
        return [list(neighbors) for neighbors in self._adj_lists]


    def get_nodes_count(self) -> int:
        return len(self._vertices)

    def get_edges_count(self, is_undirected: bool = True) -> int:
        count = 0
        if is_undirected:
            for u_id, neighbors in enumerate(self._adj_lists):
                for v_id in neighbors:
                    if u_id < v_id: # em để do đồ thị vô hướng
                        count += 1
        else: # Đồ thị có hướng
            for neighbors in self._adj_lists:
                count += len(neighbors)
        return count

    def check_graph_connectivity(self) -> bool:
        num_nodes = self.get_nodes_count()
        if num_nodes == 0:
            return True 
        if not self._adj_lists or num_nodes == 1:
             return True
        start_node_id = 0 # Bắt đầu từ đỉnh đầu tiên
        q = collections.deque([start_node_id])
        visited = [False] * num_nodes
        visited[start_node_id] = True
        count_visited = 1
        while q:
            u_id = q.popleft()
            for v_id in self._adj_lists[u_id]:
                if not visited[v_id]:
                    visited[v_id] = True
                    q.append(v_id)
                    count_visited += 1
        return count_visited == num_nodes

    def __str__(self):
        output = f"DebtGraph (Số đỉnh: {self.get_nodes_count()}, Số cạnh: {self.get_edges_count()}):\n"
        output += "Đỉnh (ID, Tên, Số dư):\n"
        for vertex in self._vertices:
            output += f"  {vertex}\n"
        output += "Danh sách kề (ID số):\n"
        for i, neighbors in enumerate(self._adj_lists):
            vertex_name = self._vertices[i].get_name() if i < len(self._vertices) else "Unknown"
            output += f"  Đỉnh {i} ('{vertex_name}'): {neighbors}\n"
        return output