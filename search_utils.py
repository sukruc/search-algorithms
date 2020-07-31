from operator import gt, lt


def _get_left_index(k):
    return 2*k+1


def _get_right_index(k):
    return 2*k+2


def _minheaporder(arr, k, size):
    left = 2*k + 1
    right = 2*k + 2

    cursor = k

    if left < size and arr[left] < arr[cursor]:
        cursor = left
    if right < size and arr[right] < arr[cursor]:
        cursor = right
    if cursor != k:
        arr[cursor], arr[k] = arr[k], arr[cursor]
        _minheaporder(arr, cursor, size)


def _maxheaporder(arr, k, size):
    left = 2*k + 1
    right = 2*k + 2

    cursor = k

    if left < size and arr[left] > arr[cursor]:
        cursor = left
    if right < size and arr[right] > arr[cursor]:
        cursor = right
    if cursor != k:
        arr[cursor], arr[k] = arr[k], arr[cursor]
        _maxheaporder(arr, cursor, size)


def _heaporder(arr, k, size, reverse=False):
    if reverse:
        op = lt
    else:
        op = gt

    left = _get_left_index(k)
    right = _get_right_index(k)

    cursor = k
    if left < size and op(arr[cursor], arr[left]):
        cursor = left
    if right < size and op(arr[cursor], arr[right]):
        cursor = right
    if cursor != k:
        arr[cursor], arr[k] = arr[k], arr[cursor]
        _heaporder(arr, cursor, size, reverse=reverse)



def _check_min_heap(arr):
    n = len(arr)
    for i in range(n):
        left = _get_left_index(i)
        right = _get_right_index(i)
        if left < n and arr[i] > arr[left]:
            return False
        if right < n and arr[i] > arr[right]:
            return False
    return True


def _check_max_heap(arr):
    n = len(arr)
    for i in range(n):
        left = _get_left_index(i)
        right = _get_right_index(i)
        if left < n and arr[i] < arr[left]:
            return False
        if right < n and arr[i] < arr[right]:
            return False
    return True


def _get_parent_index(k):
    return (k - 1) // 2


def heapify(arr, reverse=False):
    size = len(arr)
    first_parent_index = _get_parent_index(size - 1)
    for k in range(first_parent_index, -1, -1):
        _heaporder(arr, k, size, reverse=reverse)


def heappop(arr):
    n = len(arr)
    arr[0], arr[-1] = arr[-1], arr[0]
    obj = arr.pop()
    _minheaporder(arr, 0, n - 1)
    return obj


def heappush(arr, obj):
    arr.append(obj)
    size = len(arr)
    child = size - 1
    parent = _get_parent_index(child)
    while parent >= 0:
        print('parent:', arr[parent])
        print('child:', arr[child])
        if arr[parent] > arr[child]:
            arr[child], arr[parent] = arr[parent], arr[child]
            # _heaporder(arr, parent, size)
            child, parent = parent, _get_parent_index(parent)
        else:
            break


def heapsort(arr):
    heapify(arr, reverse=True)
    size = len(arr)
    for i in range(size-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        _maxheaporder(arr, 0, i)


if __name__ == '__main__':
    A = [5,4,3,2,1]

    heapsort(A)

    A

    A

    A = [1,2,3,4564,5745,13,423,543,7,53,542,637,5621,3463,75,46,24,3,7635,735,74,86,468,567,45,74,7856,82,54235345,34,367,534,764,574,74,56,36,36,435,643,56]

    heapsort(A)

    A
    _check_max_heap(A)
