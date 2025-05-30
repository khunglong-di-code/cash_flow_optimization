class Vertex:
    def __init__(self, numeric_id: int, name: str, balance: float):
        self.numeric_id: int = numeric_id
        self.name: str = name
        self.balance: float = balance

    def get_id(self) -> int:
        return self.numeric_id

    def get_name(self) -> str:
        return self.name

    def get_balance(self) -> float:
        return self.balance

    def update_balance(self, amount_change: float) -> None:
        self.balance += amount_change

    def set_balance(self, new_balance: float) -> None:
        self.balance = new_balance

    def __str__(self) -> str:
        return f"Vertex(ID: {self.numeric_id}, Tên: '{self.name}', Số dư: {self.balance})"

    def __repr__(self) -> str:
        return self.__str__()