
import sys 
#using the classical for loop iteration
var = [i*2 for i in range(10000)]
#defining the generator method
def Gen(n):
    for i in range(n):
        yield i*2       #only yielding the present value and pausing afterward
gen = Gen(10000)

print(var)
print("-----------------------------------")
for i in gen:
    print(i)
print("-----------------------------------")
print("Occupied memory (var): {} Bytes".format(sys.getsizeof(var)))
print("Occupied memory (gen): {} Bytes".format(sys.getsizeof(gen)))
print("-----------------------------------")