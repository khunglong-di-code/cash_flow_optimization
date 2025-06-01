import csv
import collections

    def add_edge(self, u_numeric_id: int, v_numeric_id: int, is_undirected: bool = True) -> None:
        num_nodes = len(self._vertices)
        if not (0 <= u_numeric_id < num_nodes and 0 <= v_numeric_id < num_nodes): return
        if u_numeric_id == v_numeric_id: return

        if v_numeric_id not in self._adj_lists[u_numeric_id]:
            self._adj_lists[u_numeric_id].append(v_numeric_id)
        if is_undirected:
            if u_numeric_id not in self._adj_lists[v_numeric_id]:
                self._adj_lists[v_numeric_id].append(u_numeric_id)
    
    def get_vertex_by_numeric_id(self, numeric_id: int) -> Vertex | None:
        if 0 <= numeric_id < len(self._vertices):
            if self._vertices[numeric_id].get_id() == numeric_id:
                 return self._vertices[numeric_id]
        return None
        
    def get_all_vertices(self) -> list[Vertex]:
        return list(self._vertices)

    def extract_all_net_balances(self) -> list[float]:
        return [v.get_balance() for v in self._vertices]

    def get_vertices_with_balances_for_output(self) -> list[list[int|float]]:
        return [[v.get_id(), v.get_balance()] for v in self._vertices]

    def get_adj_lists_for_output(self) -> list[list[int]]:
        return [list(neighbors) for neighbors in self._adj_lists]
        
    def get_nodes_count(self) -> int: return len(self._vertices)
    def get_edges_count(self, is_undirected: bool = True) -> int:
        count = 0
        if is_undirected:
            for u_id, neighbors in enumerate(self._adj_lists):
                for v_id in neighbors:
                    if u_id < v_id: count += 1
        else: 
            for neighbors in self._adj_lists: count += len(neighbors)
        return count

    def check_graph_connectivity(self) -> bool:
        num_nodes = self.get_nodes_count()
        if num_nodes == 0: return True 
        if not self._adj_lists or num_nodes == 1: return True
        start_node_id = 0 
        q = collections.deque([start_node_id])
        visited = [False] * num_nodes
        if start_node_id >= num_nodes : return False
        visited[start_node_id] = True
        count_visited = 1
        while q:
            u_id = q.popleft()
            if u_id < len(self._adj_lists):
                for v_id in self._adj_lists[u_id]:
                    if v_id < num_nodes and not visited[v_id]: 
                        visited[v_id] = True
                        q.append(v_id)
                        count_visited += 1
        return count_visited == num_nodes

def round_and_adjust_balances_for_graph(graph: DebtGraph) -> None:
    all_vertices = graph.get_all_vertices()
    if not all_vertices:
        return
    float_balances = [v.get_balance() for v in all_vertices]
    int_balances_rounded = [int(round(b)) for b in float_balances]
    current_sum = sum(int_balances_rounded)
    num_people = len(all_vertices)
    if current_sum != 0:
        adjustment_per_step = -1 if current_sum > 0 else 1
        remaining_diff = abs(current_sum)      
        idx_to_adjust = 0
        while remaining_diff > 0:
            if num_people > 0:
                v_to_adjust = graph.get_vertex_by_numeric_id(idx_to_adjust % num_people)
                if v_to_adjust: 
                    current_v_balance = int_balances_rounded[idx_to_adjust % num_people]
                    v_to_adjust.set_balance(current_v_balance + adjustment_per_step)
                    int_balances_rounded[idx_to_adjust % num_people] += adjustment_per_step 
                idx_to_adjust += 1
            remaining_diff -= 1
    final_balances_after_adjustment = [v.get_balance() for v in all_vertices]
    final_check_sum = sum(final_balances_after_adjustment)
    if final_check_sum != 0 and all_vertices:
        last_vertex = all_vertices[-1]
        last_vertex.set_balance(last_vertex.get_balance() - final_check_sum)

def preprocess_and_load_into_debtgraph(csv_filepath: str,
                                   predefined_connections_str: list[tuple[str, str]] = None,
                                   assume_complete_graph: bool = False,
                                   ensure_integer_balances: bool = True) -> DebtGraph | None:
    graph = DebtGraph()
    temp_event_data_for_balance_calc = []
    try:
        with open(csv_filepath, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row_idx, row in enumerate(reader):
                try:
                    if not all(key in row and row[key] is not None for key in ['paid_by', 'participants', 'total_cost']):
                        continue 
                    paid_by_str = row['paid_by'].strip()
                    participants_str_list_raw = [p.strip() for p in row['participants'].split(';') if p.strip()]
                    if not paid_by_str or not participants_str_list_raw:
                        continue
                    graph.add_vertex(paid_by_str, 0.0) 
                    for p_str in participants_str_list_raw:
                        graph.add_vertex(p_str, 0.0)
                    
                    temp_event_data_for_balance_calc.append({
                        "total_cost": float(row['total_cost']),
                        "paid_by": paid_by_str,
                        "participants": participants_str_list_raw
                    })
                except ValueError: continue
                except Exception: continue 
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file {csv_filepath}")
        return None
    except Exception as e:
        print(f"Lỗi khi xử lý file CSV: {e}")
        return None
    if graph.get_nodes_count() == 0:
        print("Không có người dùng nào được xử lý từ file CSV.")
        return None
    for event_data in temp_event_data_for_balance_calc:
        total_cost = event_data["total_cost"]
        paid_by_str = event_data["paid_by"]
        participants_str_list = event_data["participants"]
        try:
            paid_by_vertex = graph.get_vertex_by_name(paid_by_str)
            if paid_by_vertex is None or not participants_str_list: 
                continue
            cost_per_participant = total_cost / len(participants_str_list)
            paid_by_vertex.update_balance(-total_cost) 
            for p_str in participants_str_list:
                participant_vertex = graph.get_vertex_by_name(p_str)
                if participant_vertex is not None:
                    participant_vertex.update_balance(cost_per_participant)
        except ZeroDivisionError: 
            continue
        except Exception: 
            continue
    if ensure_integer_balances:
        round_and_adjust_balances_for_graph(graph)
    if predefined_connections_str:
        for u_str, v_str in predefined_connections_str:
            u_vertex = graph.get_vertex_by_name(u_str)
            v_vertex = graph.get_vertex_by_name(v_str)
            if u_vertex is not None and v_vertex is not None:
                graph.add_edge(u_vertex.get_id(), v_vertex.get_id())
    elif assume_complete_graph:
        num_total_nodes = graph.get_nodes_count()
        for i in range(num_total_nodes):
            for j in range(i + 1, num_total_nodes):
                graph.add_edge(i, j)
    return graph