in_str1 =   "ab efquybzepfiBEZIBCg"
in_str2 =   "JFfn do685ZCF&&""ÉLQRJNVMORZÀÇÈÀÇÉ!:;ZCzdD"
vowels  =   "aieou"

def iterative_count(in_str):
    count = 0
    for i in range(len(in_str)):
        if in_str[i].lower() not in vowels and in_str[i].isalpha():
            count +=1
    return count 

def recursive_count(in_str):
    if in_str == '':
        return 0
    if in_str[0].lower() not in vowels and in_str[0].isalpha():
        return 1+ recursive_count(in_str[1:])
    else :
        return recursive_count(in_str[1:])

print("iterative count in_str1: " + str(iterative_count(in_str1)))
print("recursive count in_str1: " + str(recursive_count(in_str1)))    
print("iterative count in_str2: " + str(iterative_count(in_str2)))
print("recursive count in_str2: " + str(recursive_count(in_str2)))        
