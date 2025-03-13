
data_set  = [1,2,3,5,6,8]
target    = 2
def iterartive_binary_search(data_set,target):
    low  = 0
    high = len(data_set)-1
    while (low <= high):
        mid = (low+high)//2
        if target== data_set[mid]:
            return True
        elif target < data_set[mid]:
            high = mid -1
        elif target > data_set[mid]:
            low  = mid +1
    return False

print(iterartive_binary_search(data_set,target))