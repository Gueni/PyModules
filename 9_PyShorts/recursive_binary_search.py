#Recursive Binary Search 
def recursive_binary_search(data_set,target,low,high):
    if low > high:
        return False
    else:
        mid = (low+high)//2
        if target == data_set[mid]:
            return True
        elif target < data_set[mid]:
            return recursive_binary_search(data_set,target,low,mid-1)
        else:
            return recursive_binary_search(data_set,target,mid+1,high)

data_set    =   [1,5,6,7,9,10,15]
target      =   9
print(recursive_binary_search(data_set,target,0,len(data_set)-1))