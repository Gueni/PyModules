string_var  =   "bcizbpuvbksdblhrzbir"

#using built in python len method
print(len(string_var))

#using iterative approche 
def iterative_len(string):
    c=0
    for i in range(len(string)):
        c+=1
    return c

print(iterative_len(string_var))

#using recursive approche
def recursive_len(string):
    if string=="":
        return 0
    return 1+ recursive_len(string[1:])

print(recursive_len(string_var))