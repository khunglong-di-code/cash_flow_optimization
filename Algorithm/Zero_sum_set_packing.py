def BEST_PARTITION(debts, subset):
    subset = subset[:]
    solutions = []
    
    # Xử lý các phần tử có giá trị 0
    i = 0
    while i < len(subset):
        if debts[subset[i]] == 0:
            # Tạo partition chỉ có 1 nhóm duy nhất
            remaining = subset[:i] + subset[i+1:]
            if remaining:
                partition, _ = BEST_PARTITION(debts, remaining)
                solutions.append(partition + [[subset[i]]])
            else:
                solutions.append([[subset[i]]])
            subset.remove(subset[i])
        else:
            i += 1
    
    subset_copy = subset[:]
    for i in subset_copy:
        if i not in subset:
            continue
        for j in subset_copy:
            if j not in subset:
                continue
            if i < j and debts[i] + debts[j] == 0:
                remaining = [x for x in subset if x != i and x != j]
                if remaining:
                    partition, _ = BEST_PARTITION(debts, remaining)
                    solutions.append(partition + [[i, j]])
                else:
                    solutions.append([[i, j]])
                subset.remove(i)
                subset.remove(j)
                break
    
    # Tìm partition cho các subset lớn hơn
    max_size = len(subset) // 2
    if len(subset) >= 3:
        for size in range(3, max_size + 1):
            for s in generate_subsets(subset, size):
                # Tính tổng không dùng sum()
                sum_s = 0
                for idx in s:
                    sum_s += debts[idx]
                if sum_s == 0:
                    remaining = [x for x in subset if x not in s]
                    if remaining:
                        partition, _ = BEST_PARTITION(debts, remaining)
                        solutions.append(partition + [s])
                    else:
                        solutions.append([s])
    
    if not solutions:
        return [], 0
    
    best = solutions[0]
    for partition in solutions:
        if len(partition) > len(best):
            best = partition
    
    k = len(best)
    return best, k

def generate_subsets(arr, size):
    if size == 0:
        yield []
        return
    if len(arr) < size:
        return
    first, rest = arr[0], arr[1:]
    for subset in generate_subsets(rest, size - 1):
        yield [first] + subset
    for subset in generate_subsets(rest, size):
        yield subset

def print_partition(debts, partition):
    result = []
    for group in partition:
        group_values = []
        for i in group:
            group_values.append(debts[i])
        result.append(group_values)
    print("Partition:", result)

if __name__ == "__main__":
    debts1 = [0, 5, -5, 3, -3]
    subset1 = [0, 1, 2, 3, 4]
    partition, k = BEST_PARTITION(debts1, subset1)
    print_partition(debts1, partition)
    print("k =", k)
