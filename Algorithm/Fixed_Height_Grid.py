def solve_debt_on_grid(c, n, grid):  
    dp_memo = {}
    pattern_memo = {}
    
    def is_valid_pattern(pattern, debts):
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

    def apply_pattern(pattern, debts, col):
        next_debts = [0] * c
        for i in range(c):
            next_debts[i] = debts[i]

        for i in range(len(pattern)):
            d = pattern[i]
            if d == 'R':
                if col < n - 1:
                    grid[i][col + 1] += debts[i]
                next_debts[i] = 0
            elif d == 'U':
                next_debts[i - 1] += debts[i]
                next_debts[i] = 0
            elif d == 'D':
                next_debts[i + 1] += debts[i]
                next_debts[i] = 0

        return next_debts

    def num_transactions(pattern):
        count = 0
        for d in pattern:
            if d != 'N':
                count += 1
        return count

    def generate_valid_patterns(c):
        DIRECTIONS = ['U', 'D', 'R', 'N']
        patterns = []
        total_patterns = 4 ** c

        for p in range(total_patterns):
            pattern = []
            temp = p
            for i in range(c):
                pattern.append(DIRECTIONS[temp % 4]) 
                temp //= 4

            valid = True
            for i in range(c - 1):
                if pattern[i] == 'D' and pattern[i + 1] == 'U':
                    valid = False
                    break
            if valid:
                patterns.append(pattern)

        return patterns

    valid_patterns = generate_valid_patterns(c)

    def DP(k, debts_tuple):
        if (k, debts_tuple) in dp_memo:
            return dp_memo[(k, debts_tuple)]

        debts = [0] * c
        for i in range(c):
            debts[i] = debts_tuple[i]

        if k == n + 1:
            return 0

        min_cost = float('inf')
        best_pattern = None

        for pattern in valid_patterns:
            if k == n and 'R' in pattern:
                continue
            if is_valid_pattern(pattern, debts):
                next_debts = apply_pattern(pattern, debts, k - 1)
                    
                cost = num_transactions(pattern) + DP(k + 1, tuple(next_debts))
                if cost < min_cost:
                    min_cost = cost
                    best_pattern = pattern

        dp_memo[(k, debts_tuple)] = min_cost
        pattern_memo[(k, debts_tuple)] = best_pattern 
        return min_cost

    def reconstruct_solution():
        k = 1
        debts_tuple = [0] * c 
        for i in range(c):
            debts_tuple[i] = grid[i][0]
        transactions = []

        while k <= n:
            pattern = pattern_memo.get((k, tuple(debts_tuple)))
            if pattern is None:
                break
            transactions.append(pattern)
            debts_tuple = apply_pattern(pattern, debts_tuple, k - 1)
            k += 1

        return transactions

    first_col_debts = [0] * c
    for i in range(c):
        first_col_debts[i] = grid[i][0]
    
    min_transactions = DP(1, tuple(first_col_debts))
    transaction_sequence = reconstruct_solution()
    return min_transactions, transaction_sequence

