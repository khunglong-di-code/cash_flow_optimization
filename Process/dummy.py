# Constants
DIRECTIONS = ['U', 'D', 'R', 'N']

# Sample grid dimensions
c = 3  # height (rows)
n = 4  # number of columns
grid = [
    [2,  3,  4,  -1],
    [1,  5, -4,  -7],
    [-3, 2,  5,   3]
]

dp_memo = {}
pattern_memo = {}

def is_valid_pattern(pattern, debts):
    """Kiểm tra xem pattern có hợp lệ với trạng thái nợ không"""
    new_debts = [0] * c
    for i in range(c):
        new_debts[i] = debts[i]

    for i in range(len(pattern)):
        d = pattern[i]
        if d == 'U':
            if i == 0 or new_debts[i] == 0:
                return False
            new_debts[i] += new_debts[i - 1]
            new_debts[i - 1] = 0
        elif d == 'D':
            if i == len(pattern) - 1 or new_debts[i] == 0:
                return False
            new_debts[i] += new_debts[i + 1]
            new_debts[i + 1] = 0

    for x in new_debts:
        if x != 0:
            return False
    return True

def apply_pattern(pattern, debts):
    """Áp dụng pattern và trả về trạng thái nợ mới"""
    next_debts = [0] * c
    for i in range(c):
        next_debts[i] = debts[i]

    for i in range(len(pattern)):
        d = pattern[i]
        if d == 'R':
            next_debts[i] += debts[i]
        elif d == 'U':
            next_debts[i - 1] += debts[i]
            next_debts[i] = 0
        elif d == 'D':
            next_debts[i + 1] += debts[i]
            next_debts[i] = 0

    return next_debts

def num_transactions(pattern):
    """Đếm số giao dịch trong pattern (bỏ qua 'N')"""
    count = 0
    for d in pattern:
        if d != 'N':
            count += 1
    return count

def generate_valid_patterns():
    """Tạo tất cả pattern hợp lệ"""
    patterns = []
    total_patterns = 1
    for i in range(c):
        total_patterns *= len(DIRECTIONS)

    for p in range(total_patterns):
        pattern = []
        temp = p
        for i in range(c):
            pattern.append(DIRECTIONS[temp % len(DIRECTIONS)])
            temp //= len(DIRECTIONS)

        # Kiểm tra ràng buộc: không có 'D' theo sau 'U' liền kề
        valid = True
        for i in range(c - 1):
            if pattern[i] == 'D' and pattern[i + 1] == 'U':
                valid = False
                break
        if valid:
            patterns.append(pattern)

    return patterns

valid_patterns = generate_valid_patterns()

def DP(k, debts_tuple):
    """Phiên bản theo tài liệu - base case ở k = n"""
    if (k, debts_tuple) in dp_memo:
        return dp_memo[(k, debts_tuple)]

    debts = list(debts_tuple)
    
    # BASE CASE: Cột cuối cùng (k = n)
    if k == n:
        min_cost = float('inf')
        best_pattern = None
        
        for pattern in valid_patterns:
            # Ràng buộc quan trọng: KHÔNG được dùng 'R' ở cột cuối
            if 'R' in pattern:
                continue
                
            if is_valid_pattern(pattern, debts):
                cost = num_transactions(pattern)
                if cost < min_cost:
                    min_cost = cost
                    best_pattern = pattern
        
        dp_memo[(k, debts_tuple)] = min_cost
        pattern_memo[(k, debts_tuple)] = best_pattern
        return min_cost
    
    # RECURSIVE CASE: Các cột từ 1 đến n-1
    min_cost = float('inf')
    best_pattern = None

    for pattern in valid_patterns:
        if is_valid_pattern(pattern, debts):
            next_debts = apply_pattern(pattern, debts)
            cost = num_transactions(pattern) + DP(k + 1, tuple(next_debts))
            if cost < min_cost:
                min_cost = cost
                best_pattern = pattern

    dp_memo[(k, debts_tuple)] = min_cost
    pattern_memo[(k, debts_tuple)] = best_pattern
    return min_cost

def solve_debt_on_grid():
    """Giải bài toán theo phương pháp tài liệu"""
    first_col_debts = [grid[i][0] for i in range(c)]
    return DP(1, tuple(first_col_debts))

def reconstruct_solution():
    """Tái tạo chuỗi pattern đã sử dụng"""
    k = 1
    debts_tuple = tuple([grid[i][0] for i in range(c)])
    transactions = []

    while k <= n:
        pattern = pattern_memo.get((k, debts_tuple))
        if pattern is None:
            break
        transactions.append(pattern)
        debts_tuple = tuple(apply_pattern(pattern, list(debts_tuple)))
        k += 1

    return transactions

# Chạy thuật toán
result = solve_debt_on_grid()
print("Minimum number of transactions:", result)

# Tái tạo và in chuỗi giao dịch
transaction_sequence = reconstruct_solution()
print("Transaction patterns used:")
for i, pattern in enumerate(transaction_sequence, 1):
    print(f"Cột {i}: {pattern}")