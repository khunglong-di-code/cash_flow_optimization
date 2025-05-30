import json
import re
import math

def read_graph_data(filepath):
    """
    Đọc và xử lý dữ liệu đồ thị từ một file.

    Hàm này sẽ đọc file, trích xuất thông tin về số đỉnh,
    trọng số (balance) của mỗi đỉnh, và danh sách kề của mỗi đỉnh.

    Args:
        filepath (str): Đường dẫn đến file chứa dữ liệu đồ thị.

    Returns:
        tuple: Một tuple chứa (num_vertices, vertex_balances, adj_lists)
               - num_vertices (int): Tổng số đỉnh.
               - vertex_balances (list): Danh sách các trọng số (balance),
                                         trong đó vertex_balances[i] là balance của đỉnh i.
               - adj_lists (list of list of int): Danh sách kề,
                                                  adj_lists[i] là list các đỉnh kề của đỉnh i.
        Hoặc trả về (None, None, None) nếu có lỗi xảy ra khi đọc hoặc xử lý file.
    """
    raw_vertices_str = ""
    raw_adj_lists_str = ""
    
    capturing_vertices = False
    capturing_adj_lists = False
    adj_lists_lines_buffer = [] # Để lưu các dòng của danh sách kề

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line_stripped = line.strip()

                # Loại bỏ tag ở đầu dòng nếu có
                # (Lưu ý: các tag trong file ví dụ dường như là metadata của file,
                # không phải là một phần của chuỗi JSON thực sự của dữ liệu đỉnh/cạnh.
                # Nếu chúng là một phần của chuỗi, logic parse JSON sẽ cần phức tạp hơn.
                # Đoạn code này giả định các dòng dữ liệu JSON không chứa các tag đó bên trong chuỗi.)
                
                # Xử lý cho các dòng có tag ở đầu
                cleaned_line = re.sub(r"^\\s*", "", line_stripped)

                if "Tập hợp đỉnh" in cleaned_line:
                    capturing_vertices = True
                    capturing_adj_lists = False
                    adj_lists_lines_buffer = [] # Reset buffer khi chuyển section
                    continue 
                elif "Tập hợp cạnh" in cleaned_line:
                    capturing_vertices = False
                    capturing_adj_lists = True
                    adj_lists_lines_buffer = [] # Reset buffer
                    continue

                if capturing_vertices:
                    # Dữ liệu đỉnh thường nằm trên một dòng ngay sau tiêu đề
                    if cleaned_line.startswith("[[") and cleaned_line.endswith("]]"):
                        raw_vertices_str = cleaned_line
                        capturing_vertices = False # Đã lấy xong dữ liệu đỉnh
                elif capturing_adj_lists:
                    # Nối các phần của danh sách kề nếu nó nằm trên nhiều dòng
                    # (Giả định cleaned_line bây giờ chỉ chứa phần dữ liệu JSON của dòng đó)
                    adj_lists_lines_buffer.append(cleaned_line)
        
        # Ghép các dòng của danh sách kề lại thành một chuỗi duy nhất
        if adj_lists_lines_buffer:
            raw_adj_lists_str = "".join(adj_lists_lines_buffer)
            # Loại bỏ các khoảng trắng thừa có thể xuất hiện do nối chuỗi
            # và đảm bảo nó là một chuỗi JSON hợp lệ.
            raw_adj_lists_str = "".join(raw_adj_lists_str.split())


        if not raw_vertices_str or not raw_adj_lists_str:
            # print("Không tìm thấy đủ dữ liệu đỉnh hoặc danh sách kề.")
            return None, None, None

        # Parse dữ liệu đỉnh
        parsed_vertices_data = json.loads(raw_vertices_str)
        num_vertices = len(parsed_vertices_data)
        
        vertex_balances = [0] * num_vertices
        for v_data in parsed_vertices_data:
            if len(v_data) == 2:
                vertex_id, balance = v_data
                if 0 <= vertex_id < num_vertices:
                    vertex_balances[vertex_id] = balance
                else:
                    # print(f"ID đỉnh không hợp lệ: {vertex_id}")
                    return None, None, None 
            else:
                # print("Dữ liệu đỉnh không đúng định dạng [id, balance].")
                return None, None, None

        # Parse danh sách kề
        adj_lists = json.loads(raw_adj_lists_str)

        if len(adj_lists) != num_vertices:
            # print("Số lượng danh sách kề không khớp với số đỉnh.")
            return None, None, None
            
        return num_vertices, vertex_balances, adj_lists

    except FileNotFoundError:
        # print(f"Lỗi: Không tìm thấy file tại đường dẫn '{filepath}'")
        return None, None, None
    except json.JSONDecodeError as e:
        # print(f"Lỗi khi parse JSON: {e}")
        # print(f"Chuỗi đỉnh thô: '{raw_vertices_str}'")
        # print(f"Chuỗi kề thô: '{raw_adj_lists_str}'")
        return None, None, None
    except Exception as e:
        # print(f"Một lỗi không xác định đã xảy ra: {e}")
        return None, None, None

def isConnected(num_vertices, adj_lists):
    """
    Kiểm tra xem đồ thị có liên thông không bằng thuật toán BFS.

    Args:
        num_vertices (int): Tổng số đỉnh trong đồ thị.
        adj_lists (list of list of int): Danh sách kề của đồ thị.
                                          adj_lists[i] là danh sách các đỉnh kề với đỉnh i.

    Returns:
        bool: True nếu đồ thị liên thông, False nếu không.
    """
    if num_vertices == 0:
        return True 
    # Nếu không có danh sách kề (ví dụ, file không có phần adj_lists,
    # hoặc adj_lists là None do lỗi đọc file) và có đỉnh,
    # thì chỉ liên thông nếu có đúng 1 đỉnh (không có cạnh).
    if not adj_lists and num_vertices > 0 : 
        return num_vertices == 1

    visited = [False] * num_vertices
    queue = []

    # Bắt đầu BFS từ một đỉnh bất kỳ (ví dụ đỉnh 0)
    # Cần đảm bảo có ít nhất một đỉnh để bắt đầu
    if num_vertices > 0:
        start_node = 0 
        queue.append(start_node)
        visited[start_node] = True
        count_visited_nodes = 1
    else: # Trường hợp num_vertices == 0 đã được xử lý
        count_visited_nodes = 0


    while queue:
        u = queue.pop(0)

        # Kiểm tra xem u có nằm trong phạm vi của adj_lists không
        if u < len(adj_lists): 
            for v in adj_lists[u]:
                # Kiểm tra xem đỉnh kề v có hợp lệ không
                if 0 <= v < num_vertices: 
                    if not visited[v]:
                        visited[v] = True
                        queue.append(v)
                        count_visited_nodes += 1
                # else:
                    # (Tùy chọn) Xử lý hoặc ghi log nếu đỉnh kề không hợp lệ
                    # print(f"Cảnh báo: Đỉnh kề {v} của đỉnh {u} không hợp lệ và bị bỏ qua.")


    return count_visited_nodes == num_vertices

def isTree(num_vertices, adj_lists, is_connected_status):
    """
    Kiểm tra xem đồ thị có phải là cây không.
    Một đồ thị là cây nếu nó liên thông và có num_vertices - 1 cạnh.

    Args:
        num_vertices (int): Tổng số đỉnh trong đồ thị.
        adj_lists (list of list of int): Danh sách kề của đồ thị.
        is_connected_status (bool): Kết quả từ việc kiểm tra tính liên thông (True nếu liên thông).

    Returns:
        bool: True nếu đồ thị là cây, False nếu không.
    """
    # Điều kiện 1: Đồ thị phải liên thông
    if not is_connected_status:
        return False

    # Xử lý các trường hợp đặc biệt
    if num_vertices == 0: # Đồ thị rỗng không được coi là cây theo định nghĩa V-1 cạnh
        return False
    if num_vertices == 1: # Đồ thị có 1 đỉnh và 0 cạnh là một cây
        # Kiểm tra số cạnh (phải là 0)
        if adj_lists and adj_lists[0]: # Nếu có danh sách kề cho đỉnh 0 và nó không rỗng
            return False # Có cạnh, không phải cây
        return True


    # Điều kiện 2: Đồ thị phải có num_vertices - 1 cạnh
    # Tính tổng số bậc của tất cả các đỉnh
    sum_of_degrees = 0
    for i in range(num_vertices):
        if i < len(adj_lists): # Đảm bảo i nằm trong phạm vi của adj_lists
            sum_of_degrees += len(adj_lists[i])
        # else: trường hợp này không nên xảy ra nếu adj_lists hợp lệ và len(adj_lists) == num_vertices
    
    # Theo định lý bắt tay, tổng các bậc bằng hai lần số cạnh (2*E)
    # Vì vậy, tổng các bậc phải là một số chẵn.
    if sum_of_degrees % 2 != 0:
        # Điều này chỉ ra một vấn đề với cấu trúc đồ thị (ví dụ: không phải đồ thị đơn giản)
        # hoặc lỗi trong danh sách kề. Một đồ thị đơn giản luôn có tổng bậc chẵn.
        return False 
    
    num_edges = sum_of_degrees // 2
    
    return num_edges == num_vertices - 1

def isComplete(num_vertices, adj_lists, is_connected_status):
    """
    Kiểm tra xem đồ thị có phải là đồ thị đầy đủ không.
    Một đồ thị đầy đủ (V > 0) có mỗi đỉnh bậc V-1.
    Đồ thị đầy đủ với V > 1 đỉnh thì luôn liên thông.

    Args:
        num_vertices (int): Tổng số đỉnh trong đồ thị.
        adj_lists (list of list of int): Danh sách kề của đồ thị.
        is_connected_status (bool): Kết quả từ việc kiểm tra tính liên thông.
                                     (Không thực sự cần thiết cho logic chính
                                     của đồ thị đầy đủ nếu V > 1, nhưng vẫn nhận vào
                                     để nhất quán với yêu cầu).

    Returns:
        bool: True nếu đồ thị đầy đủ, False nếu không.
    """
    if num_vertices == 0:
        # Đồ thị rỗng có thể coi là đầy đủ (không có cặp đỉnh nào để không có cạnh)
        # hoặc không đầy đủ. Theo nhiều định nghĩa, K_0 là đầy đủ.
        return True 
    if num_vertices == 1:
        # Đồ thị 1 đỉnh (K_1) luôn đầy đủ (bậc 0, V-1 = 1-1 = 0)
        return True

    # Đối với đồ thị đầy đủ có V > 1 đỉnh, nó phải liên thông.
    # Nếu bạn muốn ràng buộc chặt chẽ rằng hàm chỉ được gọi khi liên thông:
    # if not is_connected_status and num_vertices > 1:
    #     return False # Hoặc xử lý theo cách khác nếu logic của bạn yêu cầu

    # Kiểm tra bậc của mỗi đỉnh
    # Mỗi đỉnh trong đồ thị đầy đủ V đỉnh phải có bậc là V-1.
    expected_degree = num_vertices - 1
    for i in range(num_vertices):
        if i < len(adj_lists):
            # Kiểm tra xem danh sách kề có chứa đỉnh lặp lại hoặc khuyên không
            # Đồ thị đầy đủ là đồ thị đơn.
            # len(set(adj_lists[i])) đảm bảo các đỉnh kề là duy nhất.
            # i not in adj_lists[i] đảm bảo không có khuyên (self-loop).
            if i in adj_lists[i]: # Có khuyên
                return False
            if len(set(adj_lists[i])) != len(adj_lists[i]): # Có cạnh lặp
                 return False
            
            if len(adj_lists[i]) != expected_degree:
                return False
        else:
            # Lỗi: danh sách kề không đủ thông tin cho tất cả các đỉnh
            return False 
            
    return True

def complete_set(vertex_balances, is_complete_status):
    """
    Trả về danh sách trọng số đỉnh nếu đồ thị được xác định là đầy đủ.

    Args:
        vertex_balances (list): Danh sách các trọng số (balance) của đỉnh.
        is_complete_status (bool): Kết quả từ hàm isComplete (True nếu đầy đủ).

    Returns:
        list: Danh sách vertex_balances nếu is_complete_status là True.
              Trả về một list rỗng ([]) nếu is_complete_status là False.
    """
    if is_complete_status:
        return vertex_balances
    else:
        return [] # Trả về list rỗng nếu không phải là đồ thị đầy đủ

def _find_grid_dimensions_and_validate(num_vertices, adj_lists):
    """
    Hàm phụ trợ: Tìm kích thước lưới (m, n) và xác thực cấu trúc cơ bản.
    Trả về (isValid, m, n) hoặc (False, None, None).
    isValid là True nếu tìm thấy một cấu trúc lưới tiềm năng.
    """
    if num_vertices == 0: # Đồ thị rỗng không phải lưới hợp lệ để có kích thước
        return False, None, None
    if num_vertices == 1: # Lưới 1x1
        # Một đỉnh đơn lẻ không có cạnh (khuyên) là lưới 1x1.
        if adj_lists and adj_lists[0] and (0 in adj_lists[0] or len(adj_lists[0]) > 0) :
             return False, None, None # Có khuyên hoặc cạnh
        return True, 1, 1

    degrees = [0] * num_vertices
    sum_of_degrees = 0
    for i in range(num_vertices):
        if i < len(adj_lists):
            degree_i = len(adj_lists[i])
            degrees[i] = degree_i
            sum_of_degrees += degree_i
            # Trong đồ thị lưới có nhiều hơn 1 đỉnh, không có đỉnh cô lập (bậc 0)
            if degree_i == 0 and num_vertices > 1 : return False, None, None 
            if degree_i > 4: return False, None, None # Bậc tối đa là 4 trong lưới 2D
            # Kiểm tra đồ thị đơn
            if i in adj_lists[i]: return False, None, None # Có khuyên
            if len(set(adj_lists[i])) != degree_i: return False, None, None # Có cạnh lặp
        else: # Lỗi dữ liệu adj_lists
            return False, None, None 

    if sum_of_degrees % 2 != 0: # Tổng bậc phải chẵn
        return False, None, None 
    num_edges = sum_of_degrees // 2

    # Thử tìm các kích thước M, N của lưới
    for m_cand in range(1, int(math.sqrt(num_vertices)) + 1):
        if num_vertices % m_cand == 0:
            n_cand = num_vertices // m_cand
            
            expected_edges = 0
            if m_cand > 0 and n_cand > 0: # Đảm bảo cả hai chiều dương
                expected_edges = (m_cand - 1) * n_cand + m_cand * (n_cand - 1)
            
            if num_edges == expected_edges:
                # Kiểm tra phân bố bậc (heuristic)
                deg_counts = {0:0, 1:0, 2:0, 3:0, 4:0}
                for d_val in degrees:
                    if d_val in deg_counts: 
                        deg_counts[d_val] += 1
                    # Các bậc > 4 đã bị loại ở trên

                if m_cand == 1 and n_cand == 1: # Trường hợp 1x1 (đã xử lý ở đầu hàm này)
                    if deg_counts[0] == 1 and sum(deg_counts[d] for d in [1,2,3,4]) == 0 :
                         return True, m_cand, n_cand # (1,1)
                elif m_cand == 1 or n_cand == 1: # Là một đường thẳng (path graph) với V > 1
                    if num_vertices > 1 and deg_counts[1] == 2 and deg_counts[2] == (num_vertices - 2) and \
                       deg_counts[3] == 0 and deg_counts[4] == 0:
                        # Ưu tiên trả về hàng < cột nếu là đường thẳng
                        return True, min(m_cand,n_cand), max(m_cand,n_cand) 
                else: # Lưới M_x_N với M,N > 1
                    corners = 4
                    edges_non_corner = 2 * (m_cand - 2) + 2 * (n_cand - 2)
                    internal = (m_cand - 2) * (n_cand - 2)
                    if deg_counts[2] == corners and \
                       deg_counts[3] == edges_non_corner and \
                       deg_counts[4] == internal:
                        # Ưu tiên trả về hàng < cột
                        return True, min(m_cand,n_cand), max(m_cand,n_cand) 
            
    return False, None, None # Không tìm thấy kích thước lưới phù hợp

def isGrid(num_vertices, adj_lists, is_connected_status):
    """
    Kiểm tra xem đồ thị có phải là đồ thị lưới chữ nhật 2D không.
    Trả về True (1) nếu là lưới, False (0) nếu không.
    """
    if not is_connected_status:
        # Trường hợp đặc biệt: 1 đỉnh, 0 cạnh vẫn được coi là lưới (1x1) và liên thông.
        # _find_grid_dimensions_and_validate sẽ xử lý trường hợp num_vertices = 1.
        if num_vertices == 1:
            is_valid_form, _, _ = _find_grid_dimensions_and_validate(num_vertices, adj_lists)
            return is_valid_form
        return False # Nếu không liên thông và có nhiều hơn 1 đỉnh, không phải lưới

    # Nếu liên thông (hoặc là trường hợp 1 đỉnh), gọi hàm phụ trợ để kiểm tra cấu trúc
    is_valid_form, _, _ = _find_grid_dimensions_and_validate(num_vertices, adj_lists)
    return is_valid_form

def grid_set(num_vertices, adj_lists, vertex_balances, is_connected_status):
    """
    Nếu đồ thị là lưới (theo kiểm tra của isGrid), 
    hàm này sẽ tìm lại kích thước và trả về số hàng (c), số cột (n), và ma trận trọng số (grid_matrix).
    Nếu không phải lưới (isGrid trả về False), hàm này trả về -1.

    Args:
        num_vertices (int): Tổng số đỉnh.
        adj_lists (list of list of int): Danh sách kề.
        vertex_balances (list): Danh sách trọng số của các đỉnh.
        is_connected_status (bool): Trạng thái liên thông của đồ thị.

    Returns:
        tuple: (c, n, grid_matrix) nếu là lưới.
        int: -1 nếu không phải là lưới hoặc có lỗi.
    """
    is_graph_a_grid = isGrid(num_vertices, adj_lists, is_connected_status)

    if not is_graph_a_grid:
        return -1

    # Nếu isGrid trả về True, chúng ta cần tìm lại kích thước c (rows) và n (cols)
    # bằng cách gọi lại hàm phụ trợ.
    # (Lưu ý: Việc gọi lại _find_grid_dimensions_and_validate ở đây có nghĩa là
    # logic kiểm tra lưới được thực hiện hai lần nếu đồ thị đúng là lưới.
    # Đây là hệ quả của việc isGrid chỉ trả về boolean.)
    
    is_valid_form_again, c, n = _find_grid_dimensions_and_validate(num_vertices, adj_lists)

    if not is_valid_form_again or c is None or n is None:
        # Trường hợp này không nên xảy ra nếu isGrid trả về True và logic nhất quán.
        # Đây là một kiểm tra an toàn.
        return -1 

    # Kiểm tra vertex_balances
    if not vertex_balances or len(vertex_balances) != num_vertices:
        # Thiếu thông tin trọng số hoặc số lượng trọng số không khớp số đỉnh
        return -1 

    # Tạo grid_matrix
    grid_matrix = []
    try:
        for i in range(c): # c là số hàng
            row_data = vertex_balances[i * n : (i + 1) * n] # n là số cột
            if len(row_data) != n: # Đảm bảo lấy đủ phần tử cho một hàng
                                   # (cần thiết nếu num_vertices không phải là tích của c và n tìm được)
                return -1 # Lỗi logic hoặc dữ liệu không nhất quán
            grid_matrix.append(row_data)
    except IndexError: # Xảy ra nếu vertex_balances quá ngắn so với c*n
        return -1
        
    return c, n, grid_matrix

