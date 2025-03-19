import glob
from importlib.resources import path
import os

mylist  = []
path    =   ""

for file in glob.glob(path): 
    filename = os.path.basename(file)
    mylist.append(filename)
    
with open("musicList.txt", 'w') as file:
        for row in mylist:
            s = " ".join(map(str, row))
            file.write(s+'\n')