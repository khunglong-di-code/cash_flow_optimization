print ("Khởi động chương trình ! \n ")
menu = """Lựa chọn chức năng:
1/ Đọc file csv đã cài đặt
2/ Sinh file csv ngẫu nhiên
3/ 
4
5
6
7
8
9
10
0/ Thoát
"""
while (True):
    print (menu)
    try:
        choice = int(input("Nhập lựa chọn: "))
    except ValueError:
        print("Vui lòng nhập số nguyên từ 0 đến 10.")
        continue
    
    match choice: 
        case 1: 
            csv_file = "cash_flow_optimization_dataset.csv"
            print("File cash_flow_optimization_dataset.csv mẫu đã được đọc !")
            break           
        case 2: 
            print("Case 1:")
        case _:
            print("Nothing")
        case 0:
            print("kết thúc chương trình")
    