# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")
import math


def solution1(T, R):
    # write your code in Python 3.6

    if not T or not R:
        return 0

    if len(T) != len(R):
        raise ValueError("Both array should have same length")

    test_cases = {}
    numbers = {str(i) for i in range(10)}
    for (x, y) in zip(T, R):
        if {x[-1]} & numbers:
            test_cases[x] = [True if y == "OK" else False]
        else:
            group_name = x[:-1]
            if group_name not in test_cases:
                test_cases[group_name] = [True if y == "OK" else False]
            else:
                test_cases[group_name] += [True if y == "OK" else False]

    total_groups = len(test_cases)
    passed_groups = 0
    for k, v in test_cases.items():
        if all(v):
            passed_groups += 1
    return math.floor((passed_groups * 100) / total_groups)


def solution(A):
    i = 0
    j = 0
    n = len(A)
    e_map = dict()
    n_distinct_element = len(set(A))
    result = float("inf")

    while i < n:
        if A[i] in e_map:
            e_map[A[i]] += 1
        else:
            e_map[A[i]] = 1

        if len(e_map) == n_distinct_element:
            result = min(result, i - j)

        while len(e_map) == n_distinct_element and j <= i:
            e_map[A[j]] -= 1
            if e_map[A[j]] == 0:
                del e_map[A[j]]
                j += 1
            if len(e_map) < n_distinct_element:
                break
            result = min(result, i - j)

            if result == n_distinct_element:
                return result
            j += 1
        i += 1
    return result


# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

def solution(A, S):
    # write your code in Python 3.6
    if not A:
        return 0

    result = 0
    cur_sum = 0
    freq = {}
    n = len(A)
    MAX_RESULT = 1000000000
    for i in range(0, n):
        cur_sum += (A[i] - S)
        if (cur_sum == 0):
            result += 1
        if cur_sum in freq:
            result += freq[cur_sum]

        if cur_sum in freq:
            freq[cur_sum] += 1
        else:
            freq[cur_sum] = 1

    return result if result <= MAX_RESULT else MAX_RESULT



