def binary_search_closest(arr, target):
    left, right = 0, len(arr) - 1
    closest = None

    while left <= right:
        mid = (left + right) // 2

        if closest is None or abs(arr[mid] - target) < abs(closest - target):
            closest = arr[mid]

        if arr[mid] < target:
            left = mid + 1
        elif arr[mid] > target:
            right = mid - 1
        else:
            return arr[mid]

    return closest


arr = [1, 3, 5, 7, 9]
target = 6
print(binary_search_closest(arr, target))  # Output: 5
