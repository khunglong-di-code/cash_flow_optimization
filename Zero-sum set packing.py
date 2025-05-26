def is_valid_subset(subset):
    total = 0
    for i in range(len(subset)):
        total += subset[i]
    return total == 0

def remove_elements(arr, used_indices):
    new_arr = []
    for i in range(len(arr)):
        if not used_indices[i]:
            new_arr.append(arr[i])
    return new_arr

def count_set_bits(x):
    count = 0
    while x > 0:
        if x & 1 == 1:
            count += 1
        x = x >> 1
    return count

def BestPartition(subset):
    n = len(subset)
    if n == 0:
        return []
    max_length = 0
    best_solution = []
    total_masks = 1 << n
    for mask in range(1, total_masks):
        count = count_set_bits(mask)
        if count < 3 or count > (n // 2):
            continue
        current_subset = []
        for j in range(n):
            if (mask & (1 << j)) != 0:
                current_subset.append(subset[j])
        if is_valid_subset(current_subset):
            used_indices = []
            for j in range(n):
                if (mask & (1 << j)) != 0:
                    used_indices.append(True)
                else:
                    used_indices.append(False)
            remaining = remove_elements(subset, used_indices)
            partial_part = BestPartition(remaining)
            candidate_solution = []
            candidate_solution.append(current_subset)
            for part in partial_part:
                candidate_solution.append(part)
            total_elems = 0
            for t in candidate_solution:
                total_elems += len(t)
            if total_elems > max_length:
                max_length = total_elems
                best_solution = candidate_solution
    return best_solution

def zero_sum_set_packing(arr):
    n = len(arr)
    used = []
    for _ in range(n):
        used.append(False)
    result = []

    for i in range(n):
        if not used[i] and arr[i] == 0:
            result.append([arr[i]])
            used[i] = True

    for i in range(n):
        if used[i]:
            continue
        for j in range(i + 1, n):
            if used[j]:
                continue
            if arr[i] + arr[j] == 0:
                result.append([arr[i], arr[j]])
                used[i] = True
                used[j] = True
                break

    remaining = []
    for i in range(n):
        if not used[i]:
            remaining.append(arr[i])

    partitions = BestPartition(remaining)
    for part in partitions:
        result.append(part)

    return result

def read_data_from_file(filename):
    arr = []
    file = open(filename, 'r')
    for line in file:
        line = line.strip()
        if line != '':
            num = 0
            negative = False
            start_index = 0
            if line[0] == '-':
                negative = True
                start_index = 1
            for i in range(start_index, len(line)):
                num = num * 10 + (ord(line[i]) - ord('0'))
            if negative:
                num = -num
            arr.append(num)
    file.close()
    return arr

def main():
    filename = 'data.txt'
    arr = read_data_from_file(filename)
    subsets = zero_sum_set_packing(arr)
    print("Các tập con rời nhau có tổng bằng 0 (số phần tử tối đa):")
    for subset in subsets:
        print(subset)

if __name__ == "__main__":
    main()
