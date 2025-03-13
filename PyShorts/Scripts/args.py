args = [1,2,3]
kwargs = {'a':1,'b':2,'c':3}

def func(a,b,c):
    print(a,b,c)

func(*args)     # output: 1 2 3 
func(**kwargs)  # output: 1 2 3 
    