from Algorithm import *

from Data import *

import csv
import os

print ("Khởi động chương trình ! \n ")

menu = """Lựa chọn chức năng:
1/ Đọc và xử lí file csv đã cài đặt.
2/ Kiểm tra điều kiện liên thông của đồ thị nợ.
3/ Kiểm tra tính chất đồ thị nợ.
4/ Sử dụng phương pháp tổng quát cho đồ thị
5/ Sử dụng phương pháp cho đồ thị đầy đủ
6/ Sử dụng phương pháp cho đồ thị lưới
7/ Sử dụng phương pháp Min edge Max flow
0/ Thoát

"""
Control = True
Sample = []
csv_file = None
flag1 = False

while (Control == True):
    print (menu)
    try:
        choice = int(input("Nhập lựa chọn: "))
    except ValueError:
        print("Vui lòng nhập số nguyên từ 0 đến 10. \n")
        continue
    
    match choice: 
        case 1: 
            csv_file = "cash_flow_optimization_dataset.csv"

            SHOULD_ENSURE_INTEGER_BALANCES = True 
            names_map, balances, _ = preprocess_to_lists(
            csv_file,
            ensure_integer_balances=SHOULD_ENSURE_INTEGER_BALANCES,
            assume_complete_graph=False,
            predefined_connections_str=None)
            
            if not names_map:
                print("Không xử lý được dữ liệu từ CSV. Kết thúc. \n")
                flag1 = False
                continue
            else:

                num_people = get_nodes_count(names_map)
                # Alg1: Đồ thị đầy đủ
                adj_alg1 = create_complete_adj_list(num_people)
                write_graph_to_txt_minimal("Data/output_alg1_complete.txt", balances, adj_alg1, SHOULD_ENSURE_INTEGER_BALANCES)
                Sample.append("Data/output_alg1_complete.txt")

                # Alg2 & Alg6: Đồ thị tổng quát liên thông
                adj_alg2_6 = create_general_connected_adj_list(num_people, extra_edges_factor=0.25)
                write_graph_to_txt_minimal("Data/output_alg2_6_general.txt", balances, adj_alg2_6, SHOULD_ENSURE_INTEGER_BALANCES)
                Sample.append("Data/output_alg2_6_general.txt")

                # Alg3: Tree
                adj_alg3_path = create_tree_adj_list(num_people, tree_type="path")
                write_graph_to_txt_minimal("Data/output_alg3_tree_path.txt", balances, adj_alg3_path, SHOULD_ENSURE_INTEGER_BALANCES)
                Sample.append("Data/output_alg3_tree_path.txt")
    
                adj_alg3_star = create_tree_adj_list(num_people, tree_type="star")
                write_graph_to_txt_minimal("Data/output_alg3_tree_star.txt", balances, adj_alg3_star, SHOULD_ENSURE_INTEGER_BALANCES)
                Sample.append("Data/output_alg3_tree_star.txt")

                # Alg4: Grid
                if num_people > 0:
                    potential_rows, potential_cols = 0, 0
                    for r_test in range(1, int(num_people**0.5) + 2):
                        if r_test == 0: continue
                        if num_people % r_test == 0:
                            potential_rows = r_test
                            potential_cols = num_people // r_test

                    if potential_rows * potential_cols == num_people and potential_rows > 0:
                        filename = f"output_alg4_grid_{potential_rows}x{potential_cols}.txt"
                        adj_alg4 = create_grid_adj_list(potential_rows, potential_cols)
                        write_graph_to_txt_minimal(filename, balances, adj_alg4, SHOULD_ENSURE_INTEGER_BALANCES)
                        Sample.append(filename)
                    elif num_people == 1:
                        filename = "output_alg4_grid_1x1.txt"
                        adj_alg4_single = create_grid_adj_list(1,1)
                        write_graph_to_txt_minimal(filename, balances, adj_alg4_single, SHOULD_ENSURE_INTEGER_BALANCES)
                        Sample.append(filename)
                    elif num_people > 1 : 
                        filename = f"output_alg4_grid_1x{num_people}.txt"
                        adj_alg4_path = create_grid_adj_list(1, num_people)
                        write_graph_to_txt_minimal(filename, balances, adj_alg4_path, SHOULD_ENSURE_INTEGER_BALANCES)
                        Sample.append(filename)

                print("File cash_flow_optimization_dataset.csv mẫu đã được đọc và xử lí! \n")

                flag1 = True
                
            continue    

        case 2: 
            print("Kết quả kiểm tra tính liên thông: \n")
            if not Sample:
                print("Chưa có dữ liệu đồ thị. Vui lòng chạy chức năng 1 trước.")
                continue
            if flag1:
                for filename in Sample:
                    if not os.path.exists(filename):
                        print(f"File {filename} không tồn tại.")
                        continue
                    a, b = readGraph(filename)
                    if isConnect(a, b): 
                        print(f"{filename} là liên thông \n")
                    else: 
                        print(f"{filename} ko là liên thông \n")
                    a, b = None, None
            else: 
                print("Không thể thực thi do lỗi \n")
                continue

        case 3: 
            print("Kết quả kiểm tra tính chất đồ thị: \n")
            if not Sample:
                print("Chưa có dữ liệu đồ thị. Vui lòng chạy chức năng 1 trước.")
                continue
            if flag1:
                for filename in Sample:
                    if not os.path.exists(filename):
                        print(f"File {filename} không tồn tại.")
                        continue
                    a, b = readGraph(filename)
                    if isConnect(a, b):
                        print (f"{filename} là liên thông ")
                        if isTree(a, b): 
                            print (f"{filename} và Cây \n")
                        if isComplete(a, b): 
                            print (f"{filename} và đồ thị đầy đủ \n")
                        if isGrid(a, b): 
                            print (f"{filename} và đồ thị lưới \n")
                    a, b = None, None
            else: 
                print("Không thể thực thi do lỗi \n")
                continue

        case 4:
            print("Chức năng 4: Tìm giao dịch tối ưu trên đồ thị tổng quát.")
            if not Sample:
                print("Chưa có dữ liệu đồ thị. Vui lòng chạy chức năng 1 trước.")
                continue
            print("Danh sách file đồ thị có thể chọn:")
            for idx, filename in enumerate(Sample):
                print(f"{idx+1} - {filename}")
            try:
                idx = int(input("Chọn Sample để thực hiện (ví dụ: 1): ")) - 1
                if idx < 0 or idx >= len(Sample):
                    print("Lựa chọn không hợp lệ.")
                    continue
            except ValueError:
                print("Vui lòng nhập số hợp lệ.")
                continue

            filename = Sample[idx]
            if not os.path.exists(filename):
                print(f"File {filename} không tồn tại.")
                continue

            V, T = readGraph(filename)
            transactions = FIND_TRANSACTIONS(vertex_data, edge_data):
            print("Các giao dịch tối ưu:")
            for tr in transactions:
                print(tr)

        case 5:
            print("Chức năng 5: Tìm giao dịch tối ưu trên đồ thị đầy đủ.")
            if not Sample:
                print("Chưa có dữ liệu đồ thị. Vui lòng chạy chức năng 1 trước.")
                continue
            print("Danh sách file đồ thị có thể chọn:")
            for idx, filename in enumerate(Sample):
                print(f"{idx+1} - {filename}")
            try:
                idx = int(input("Chọn Sample để thực hiện (ví dụ: 1): ")) - 1
                if idx < 0 or idx >= len(Sample):
                    print("Lựa chọn không hợp lệ.")
                    continue
            except ValueError:
                print("Vui lòng nhập số hợp lệ.")
                continue

            filename = Sample[idx]
            if not os.path.exists(filename):
                print(f"File {filename} không tồn tại.")
                continue

            V, T = readGraph(filename)
            if not isComplete(V, T):
                print("File này không phải là đồ thị đầy đủ. Vui lòng chọn lại.")
                continue

            transactions = FIND_TRANSACTIONS(vertex_data, edge_data)
            print("Các giao dịch tối ưu:")
            for tr in transactions:
                print(tr)

        case 6:
            print("Chức năng 6: Tìm giao dịch tối ưu trên đồ thị lưới.")
            if not Sample:
                print("Chưa có dữ liệu đồ thị. Vui lòng chạy chức năng 1 trước.")
                continue
            print("Danh sách file đồ thị có thể chọn:")
            for idx, filename in enumerate(Sample):
                print(f"{idx+1} - {filename}")
            try:
                idx = int(input("Chọn Sample để thực hiện (ví dụ: 1): ")) - 1
                if idx < 0 or idx >= len(Sample):
                    print("Lựa chọn không hợp lệ.")
                    continue
            except ValueError:
                print("Vui lòng nhập số hợp lệ.")
                continue

            filename = Sample[idx]
            if not os.path.exists(filename):
                print(f"File {filename} không tồn tại.")
                continue

            from Algorithm.Check_Graph import readGraph, isGrid, grid_set
            from Algorithm.Fixed_Height_Grid import solve_debt_on_grid

            vertex_data, edge_data = readGraph(filename)
            if not isGrid(vertex_data, edge_data):
                print("Đồ thị không phải dạng lưới.")
                continue

            r, c, grid = grid_set(vertex_data)
            min_transactions, transaction_sequence = solve_debt_on_grid(r, c, grid)
            print("Số giao dịch tối thiểu:", min_transactions)
            print("Chuỗi giao dịch:")
            for idx, pattern in enumerate(transaction_sequence):
                print(f"Cột {idx+1}: {pattern}")
        case 7:
            print("Chức năng 7: Tìm giao dịch tối ưu bằng Min Cost Max Flow.")
            if not Sample:
                print("Chưa có dữ liệu đồ thị. Vui lòng chạy chức năng 1 trước.")
                continue
            print("Danh sách file đồ thị có thể chọn:")
            for idx, filename in enumerate(Sample):
                print(f"{idx+1} - {filename}")
            try:
                idx = int(input("Chọn Sample để thực hiện (ví dụ: 1): ")) - 1
                if idx < 0 or idx >= len(Sample):
                    print("Lựa chọn không hợp lệ.")
                    continue
            except ValueError:
                print("Vui lòng nhập số hợp lệ.")
                continue

            filename = Sample[idx]
            if not os.path.exists(filename):
                print(f"File {filename} không tồn tại.")
                continue

            V, T = readGraph(filename)
            if not isConnect(V, T):
                print("File này không phải là đồ thị liên thông. Vui lòng chọn lại.")
                continue

            transactions = solve_debt_MCMF(V,T)
            for transaction in transactions:
                from_node, to_node, amount = transaction
                print(f"{from_node} -> {to_node}: {amount}")

            print("Số giao dịch tối thiểu: ", len(transactions))
          
        case 0:
            print("kết thúc chương trình")
            Control = False

    
