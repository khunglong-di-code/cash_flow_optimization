import csv
import collections
import os
import random

def get_nodes_count(person_names_list: list[str]) -> int:
    return len(person_names_list)

def get_balance_by_id(numeric_id: int, balances_list: list) -> float | int | None:
    if 0 <= numeric_id < len(balances_list):
        return balances_list[numeric_id]
    return None
def add_transaction_channel(numeric_id_u: int,
                            numeric_id_v: int,
                            adj_lists: list[list[int]],
                            num_nodes: int,
                            is_directed: bool = False) -> None:
    if not (0 <= numeric_id_u < num_nodes and 0 <= numeric_id_v < num_nodes):
        return
    if numeric_id_v not in adj_lists[numeric_id_u]:
        adj_lists[numeric_id_u].append(numeric_id_v)
    if not is_directed:
        if numeric_id_u not in adj_lists[numeric_id_v]:
            adj_lists[numeric_id_v].append(numeric_id_u)
            
def get_edges_count(adj_lists: list[list[int]], is_undirected: bool = True) -> int:
    count = 0
    if is_undirected:
        counted_edges = []
        for u, neighbors in enumerate(adj_lists):
            for v in neighbors:
                edge = sorted([u, v])
                if edge not in counted_edges:
                    counted_edges.append(edge)
                    count += 1
    else:
        for neighbors in adj_lists:
            count += len(neighbors)
    return count

def is_graph_connected(num_nodes: int, adj_lists: list[list[int]]) -> bool:
    if num_nodes == 0: return True
    if not adj_lists or num_nodes == 1: return True
    start_node = -1
    for i in range(min(num_nodes, len(adj_lists))):
        if adj_lists[i] or num_nodes == 1 :
             start_node = i
             break
    if start_node == -1 and adj_lists:
        if num_nodes > 0: start_node = 0
        else: return True
    if start_node == -1 : return num_nodes <= 1
    q = collections.deque([start_node])
    visited_count = 0
    visited_nodes = [False] * num_nodes
    visited_nodes[start_node] = True
    visited_count = 1
    while q:
        node = q.popleft()
        if node < len(adj_lists):
            for neighbor in adj_lists[node]:
                if neighbor < num_nodes and not visited_nodes[neighbor]:
                    visited_nodes[neighbor] = True
                    q.append(neighbor)
                    visited_count += 1
    return visited_count == num_nodes

def round_and_adjust_balances(float_balances: list[float]) -> list[int]:
    if not float_balances: return []
    int_balances = [int(round(b)) for b in float_balances]
    current_sum = sum(int_balances)
    if current_sum != 0:
        num_people = len(int_balances)
        adjustment_per_step = -1 if current_sum > 0 else 1
        remaining_diff = abs(current_sum)
        idx_to_adjust = 0
        while remaining_diff > 0:
            if num_people > 0 :
                int_balances[idx_to_adjust % num_people] += adjustment_per_step
                idx_to_adjust += 1
            remaining_diff -=1
    final_check_sum = sum(int_balances)
    if final_check_sum != 0 and int_balances:
        int_balances[-1] -= final_check_sum
    return int_balances

def get_numeric_id_by_name(person_name_str: str, person_names_list: list[str]) -> int | None:
    try:
        return person_names_list.index(person_name_str)
    except ValueError:
        return None

def update_person_balance(numeric_id: int,
                          amount_change: float,
                          balances_list: list) -> None:
    if 0 <= numeric_id < len(balances_list):
        balances_list[numeric_id] += amount_change

def preprocess_to_lists(csv_filepath: str,
                        predefined_connections_str: list = None,
                        assume_complete_graph: bool = False,
                        ensure_integer_balances: bool = True) -> tuple[list[str], list, list[list[int]]]:
    person_names_list = []
    temp_event_data_for_balance_calc = []
    all_unique_person_str_ids_ordered = []
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
                    if paid_by_str not in all_unique_person_str_ids_ordered:
                        all_unique_person_str_ids_ordered.append(paid_by_str)
                    for p_str in participants_str_list_raw:
                        if p_str not in all_unique_person_str_ids_ordered:
                            all_unique_person_str_ids_ordered.append(p_str)
                    temp_event_data_for_balance_calc.append({
                        "total_cost": float(row['total_cost']),
                        "paid_by": paid_by_str,
                        "participants": participants_str_list_raw
                    })
                except ValueError: continue
                except Exception: continue
    except FileNotFoundError: return [], [], []
    except Exception: return [], [], []

    person_names_list = all_unique_person_str_ids_ordered
    num_unique_people = get_nodes_count(person_names_list)
    if num_unique_people == 0: return [], [], []

    float_balances_list = [0.0] * num_unique_people
    adj_lists = [[] for _ in range(num_unique_people)]

    for event_data in temp_event_data_for_balance_calc:
        total_cost = event_data["total_cost"]
        paid_by_str = event_data["paid_by"]
        participants_str_list = event_data["participants"]
        try:
            paid_by_numeric_id = get_numeric_id_by_name(paid_by_str, person_names_list)
            if paid_by_numeric_id is None: continue
            if not participants_str_list: continue
            cost_per_participant = total_cost / len(participants_str_list)
            update_person_balance(paid_by_numeric_id, -total_cost, float_balances_list)
            for p_str in participants_str_list:
                p_numeric_id = get_numeric_id_by_name(p_str, person_names_list)
                if p_numeric_id is not None:
                    update_person_balance(p_numeric_id, cost_per_participant, float_balances_list)
        except ZeroDivisionError: continue
        except Exception: continue
            
    final_balances_list: list[int] | list[float]
    if ensure_integer_balances:
        final_balances_list = round_and_adjust_balances(float_balances_list)
    else:
        final_balances_list = float_balances_list
            
    if predefined_connections_str:
        for u_str, v_str in predefined_connections_str:
            u_numeric = get_numeric_id_by_name(u_str, person_names_list)
            v_numeric = get_numeric_id_by_name(v_str, person_names_list)
            if u_numeric is not None and v_numeric is not None:
                add_transaction_channel(u_numeric, v_numeric, adj_lists, num_unique_people)
    elif assume_complete_graph:
        for i in range(num_unique_people):
            for j in range(i + 1, num_unique_people):
                add_transaction_channel(i, j, adj_lists, num_unique_people)
    
    return person_names_list, final_balances_list, adj_lists

def create_empty_adj_list(num_nodes: int) -> list[list[int]]:
    return [[] for _ in range(num_nodes)]

def create_complete_adj_list(num_nodes: int) -> list[list[int]]:
    adj = [[] for _ in range(num_nodes)]
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            add_transaction_channel(i, j, adj, num_nodes)
    return adj

def create_tree_adj_list(num_nodes: int, tree_type: str = "path") -> list[list[int]]:
    adj = [[] for _ in range(num_nodes)]
    if num_nodes <= 1: return adj
    if tree_type == "path":
        for i in range(num_nodes - 1):
            add_transaction_channel(i, i + 1, adj, num_nodes)
    elif tree_type == "star":
        if num_nodes > 1:
            for i in range(1, num_nodes):
                add_transaction_channel(0, i, adj, num_nodes)
    return adj

def create_grid_adj_list(num_rows: int, num_cols: int) -> list[list[int]]:
    num_nodes = num_rows * num_cols
    if num_nodes == 0: return []
    adj = [[] for _ in range(num_nodes)]
    for r in range(num_rows):
        for c in range(num_cols):
            current_node_numeric_id = r * num_cols + c
            if r + 1 < num_rows:
                neighbor_numeric_id = (r + 1) * num_cols + c
                add_transaction_channel(current_node_numeric_id, neighbor_numeric_id, adj, num_nodes)
            if c + 1 < num_cols:
                neighbor_numeric_id = r * num_cols + (c + 1)
                add_transaction_channel(current_node_numeric_id, neighbor_numeric_id, adj, num_nodes)
    return adj

def create_general_connected_adj_list(num_nodes: int, extra_edges_factor: float = 0.1) -> list[list[int]]:
    if num_nodes == 0: return []
    adj = create_tree_adj_list(num_nodes, "path")
    max_possible_edges = num_nodes * (num_nodes - 1) // 2
    current_edges = get_edges_count(adj)
    num_extra_edges_to_add = int((max_possible_edges - current_edges) * extra_edges_factor)
    edges_added = 0
    attempts = 0
    while edges_added < num_extra_edges_to_add and attempts < num_extra_edges_to_add * 5:
        if num_nodes < 2: break
        u, v = random.sample(range(num_nodes), 2)
        is_existing = False
        if v in adj[u]: is_existing = True
        if not is_existing:
            add_transaction_channel(u, v, adj, num_nodes)
            edges_added += 1
        attempts +=1
    return adj

def create_small_pathwidth_adj_list(num_nodes: int) -> list[list[int]]:
    if num_nodes == 0: return []
    adj = [[] for _ in range(num_nodes)]
    if num_nodes == 1: return adj
    if num_nodes == 2:
        add_transaction_channel(0,1,adj,num_nodes)
        return adj
    for i in range(num_nodes - 1):
        add_transaction_channel(i, i + 1, adj, num_nodes)
    if num_nodes > 3: add_transaction_channel(0, 2, adj, num_nodes)
    if num_nodes > 4: add_transaction_channel(1, 3, adj, num_nodes)
    return adj

def write_graph_to_txt_minimal(filename: str,
                               balances: list,
                               adj: list[list[int]],
                               ensure_integer_balances_flag: bool):
    with open(filename, "w", encoding="utf-8") as f_out:
        f_out.write("Tập hợp đỉnh (numeric_id, balance):\n")
        vertices_output_list_for_file = []
        for i in range(len(balances)): 
            balance_value = balances[i]
            processed_balance = int(balance_value) if ensure_integer_balances_flag and balance_value is not None else balance_value
            vertices_output_list_for_file.append([i, processed_balance])
        f_out.write(str(vertices_output_list_for_file) + "\n") 
        
        f_out.write("\nTập hợp cạnh (danh sách kề - adj_lists):\n")
        f_out.write(str(adj) + "\n") 
    print(f"Output tối giản cho file '{filename}' đã được tạo.") 

if __name__ == "__main__":
    csv_file = "cash_flow_optimization_dataset.csv"
    if not os.path.exists(csv_file):
        print("Tạo file CSV mẫu đơn giản...")
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["event_id","description","total_cost","paid_by","participants"])
            for i in range(1, 21):
                p_ids = [f"P{j}" for j in range(1,21)]
                num_participants_event = random.randint(2,7)
                event_participants = random.sample(p_ids, num_participants_event)
                event_paid_by = random.choice(event_participants)
                writer.writerow([
                    f"event_main{i}", 
                    random.choice(["Ăn chung", "Mua sắm chung", "Du lịch nhóm"]), 
                    str(random.randint(5,50)*10000), 
                    event_paid_by, 
                    ";".join(event_participants)
                ])
    SHOULD_ENSURE_INTEGER_BALANCES = True 
    names_map, balances, _ = preprocess_to_lists(
        csv_file,
        ensure_integer_balances=SHOULD_ENSURE_INTEGER_BALANCES,
        assume_complete_graph=False,
        predefined_connections_str=None
    )

    if not names_map:
        print("Không xử lý được dữ liệu từ CSV. Kết thúc.")
    else:
        num_people = get_nodes_count(names_map)

        # Alg1: Đồ thị đầy đủ
        adj_alg1 = create_complete_adj_list(num_people)
        write_graph_to_txt_minimal("output_alg1_complete.txt", balances, adj_alg1, SHOULD_ENSURE_INTEGER_BALANCES)

        # Alg2 & Alg6: Đồ thị tổng quát liên thông
        adj_alg2_6 = create_general_connected_adj_list(num_people, extra_edges_factor=0.25)
        write_graph_to_txt_minimal("output_alg2_6_general.txt", balances, adj_alg2_6, SHOULD_ENSURE_INTEGER_BALANCES)

        # Alg3: Tree
        adj_alg3_path = create_tree_adj_list(num_people, tree_type="path")
        write_graph_to_txt_minimal("output_alg3_tree_path.txt", balances, adj_alg3_path, SHOULD_ENSURE_INTEGER_BALANCES)
        
        adj_alg3_star = create_tree_adj_list(num_people, tree_type="star")
        write_graph_to_txt_minimal("output_alg3_tree_star.txt", balances, adj_alg3_star, SHOULD_ENSURE_INTEGER_BALANCES)

        # Alg4: Grid
        if num_people > 0:
            potential_rows, potential_cols = 0, 0
            for r_test in range(1, int(num_people**0.5) + 2):
                if r_test == 0: continue
                if num_people % r_test == 0:
                    potential_rows = r_test
                    potential_cols = num_people // r_test
            
            if potential_rows * potential_cols == num_people and potential_rows > 0:
                 adj_alg4 = create_grid_adj_list(potential_rows, potential_cols)
                 write_graph_to_txt_minimal(f"output_alg4_grid_{potential_rows}x{potential_cols}.txt", balances, adj_alg4, SHOULD_ENSURE_INTEGER_BALANCES)
            elif num_people == 1:
                 adj_alg4_single = create_grid_adj_list(1,1)
                 write_graph_to_txt_minimal(f"output_alg4_grid_1x1.txt", balances, adj_alg4_single, SHOULD_ENSURE_INTEGER_BALANCES)
            elif num_people > 1 : 
                 adj_alg4_path = create_grid_adj_list(1, num_people)
                 write_graph_to_txt_minimal(f"output_alg4_grid_1x{num_people}.txt", balances, adj_alg4_path, SHOULD_ENSURE_INTEGER_BALANCES)

        # Alg5: Fixed Pathwidth Graph
        adj_alg5 = create_small_pathwidth_adj_list(num_people)
        write_graph_to_txt_minimal("output_alg5_small_pathwidth.txt", balances, adj_alg5, SHOULD_ENSURE_INTEGER_BALANCES)