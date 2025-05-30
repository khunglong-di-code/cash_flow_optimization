class Edge:
    def __init__(self, u_numeric_id: int, v_numeric_id: int):
        # đây là phần khởi tạo, Thoa nhớ giúp bạn kiểm tra lại phần vô hướng nhé
        if u_numeric_id < v_numeric_id:
            self.vertex1_id: int = u_numeric_id
            self.vertex2_id: int = v_numeric_id
        else:
            self.vertex1_id: int = v_numeric_id
            self.vertex2_id: int = u_numeric_id 