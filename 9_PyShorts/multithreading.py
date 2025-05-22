import time
import threading

list    =   []
tt1 ,tt2    =   0.2 , 0.2
#count function to be passed as first thread.
def count_1(n):
    for i in range(1,n+1):
       list.append(i)
       time.sleep(tt1) 
#count function to be passed as second thread.
def count_2(n):
    for i in range(1,n+1):
       list.append(i)
       time.sleep(tt2) 
#declaring the first thread associated to count_1 & passing n = 5
thread_1 = threading.Thread(target=count_1,args=(5,))
#start first thread
thread_1.start()
#declaring the first thread associated to count_2 & passing n = 5
thread_2=threading.Thread(target=count_2,args=(5,))
#start second thread
thread_2.start()
#print number of active threads 
print(threading.active_count())
# do not jump to line 30 and so on before thread 1 and 2 are done executing.
thread_1.join()     
thread_2.join()
print(threading.active_count())
print(list)
print("threading is over")