def BEST_PARTITION(debts, subset):
    subset_copy = []
    for i in range(len(subset)):
        subset_copy.append(subset[i])

    solutions = []

    # Xử lý phần tử bằng 0
    i = 0
    while i < len(subset_copy):
        if debts[subset_copy[i]] == 0:
            remaining = []
            for x in subset_copy:
                if x != subset_copy[i]:
                    remaining.append(x)

            if len(remaining) > 0:
                partition, _ = BEST_PARTITION(debts, remaining)
                temp = []
                for p in partition:
                    temp.append(p)
                temp.append([subset_copy[i]])
                solutions.append(temp)
            else:
                solutions.append([[subset_copy[i]]])
            subset_copy.pop(i)
        else:
            i = i + 1

    # Xử lý cặp có tổng bằng 0
    i = 0
    while i < len(subset_copy):
        j = i + 1
        found = False
        while j < len(subset_copy):
            if debts[subset_copy[i]] + debts[subset_copy[j]] == 0:
                remaining = []
                for x in subset_copy:
                    if x != subset_copy[i] and x != subset_copy[j]:
                        remaining.append(x)

                if len(remaining) > 0:
                    partition, _ = BEST_PARTITION(debts, remaining)
                    temp = []
                    for p in partition:
                        temp.append(p)
                    temp.append([subset_copy[i], subset_copy[j]])
                    solutions.append(temp)
                else:
                    solutions.append([[subset_copy[i], subset_copy[j]]])
                subset_copy.pop(j)
                subset_copy.pop(i)
                found = True
                break
            else:
                j = j + 1
        if not found:
            i = i + 1

    # Xét nhóm từ 3 đến n (không giới hạn n//2 nữa)
    n = len(subset_copy)
    size = 3

    while size <= n:
        subsets = generate_subsets(subset_copy, size)
        for s in subsets:
            sum_s = 0
            for idx in s:
                sum_s = sum_s + debts[idx]

            if sum_s == 0:
                remaining = []
                for x in subset_copy:
                    in_s = False
                    for y in s:
                        if x == y:
                            in_s = True
                    if not in_s:
                        remaining.append(x)

                if len(remaining) > 0:
                    partition, _ = BEST_PARTITION(debts, remaining)
                    temp = []
                    for p in partition:
                        temp.append(p)
                    temp.append(s)
                    solutions.append(temp)
                else:
                    solutions.append([s])
        size = size + 1

    if len(solutions) == 0:
        return [], 0

    best = solutions[0]
    for part in solutions:
        if len(part) > len(best):
            best = part

    k = len(best)
    return best, k


def generate_subsets(arr, size):
    result = []

    def backtrack(start, path):
        if len(path) == size:
            temp = []
            for x in path:
                temp.append(x)
            result.append(temp)
            return

        i = start
        while i < len(arr):
            path.append(arr[i])
            backtrack(i + 1, path)
            path.pop()
            i = i + 1

    backtrack(0, [])
    return result


def print_partition(debts, partition):
    result = []
    for group in partition:
        group_values = []
        for i in group:
            group_values.append(debts[i])
        result.append(group_values)
    print("Partition:", result)


if __name__ == "__main__":
    debts1 = [-3, 3, -4, 4, -1, 2, -1, 0]
    subset1 = [0,1,2,3,4,5,6,7]
    for i in range(len(debts1)):
        subset1.append(i)

    partition, k = BEST_PARTITION(debts1, subset1)
    print_partition(debts1, partition)
    print("k =", k)
