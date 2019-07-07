from concurrent import futures
import  time

def create_ont(tnum):
    time.sleep(1)
    a = time.time()
    print(a)
    return a


with futures.ThreadPoolExecutor(max_workers=20 ) as executor:
    g = executor.map(create_ont,[1,2,2,3,3,1])
    # print(a)

print(list(g))