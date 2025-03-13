
def linear_search(data_set,target):
    for i in range(len(data_set)):
        if data_set[i]== target:
            return True
    return False


data_set    = [1,2,5,66,94,52,36,55,8,9,63,0]
target      = 36

print(linear_search(data_set,target))