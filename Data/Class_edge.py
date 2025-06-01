class Edge:
    def __init__(self, u_numeric_id: int, v_numeric_id: int):
        if u_numeric_id < v_numeric_id:
            self.vertex1_id: int = u_numeric_id
            self.vertex2_id: int = v_numeric_id
        else:
            self.vertex1_id: int = v_numeric_id
            self.vertex2_id: int = u_numeric_id
    '''Theo em - Anh Tú, em vẫn cho các phương thức này vào ADT edge, ví dụ như get_endpoints (Xác định đỉnh) dù đồ thị là vô hướng, 
    hay tương tự 2 phương thức tiếp theo, mục tiêu là tương tác riêng biệt từng cạnh, còn class DebtGraph sẽ có các thao tác của tập hợp cạnh ạ'''
    def get_endpoints(self) -> list[int]: 
        return [self.vertex1_id, self.vertex2_id]

    def connects_vertex(self, numeric_id: int) -> bool:
        return self.vertex1_id == numeric_id or self.vertex2_id == numeric_id

    def get_other_vertex_id(self, numeric_id: int) -> int | None:
        if self.vertex1_id == numeric_id:
            return self.vertex2_id
        elif self.vertex2_id == numeric_id:
            return self.vertex1_id
        return None

    def __str__(self) -> str:
        return f"Edge({self.vertex1_id} - {self.vertex2_id})"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if not isinstance(other, Edge):
            return False
        return (self.vertex1_id == other.vertex1_id and 
                self.vertex2_id == other.vertex2_id)
        
    def __hash__(self) -> int:
        return hash(f"{self.vertex1_id}-{self.vertex2_id}")
