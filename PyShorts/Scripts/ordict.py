
from collections import OrderedDict
keys  = ['a','b','c']
vals = [1,2,3]
od = OrderedDict()
g =   {'a':1,'b':2,'c':3}
for key in keys:
    for val in vals:
        od[key]=val

print(dict(od))
print(g)

my_list = [1, 2, 3, 4, 5]
one, two, three, four, five = my_list

print(one)