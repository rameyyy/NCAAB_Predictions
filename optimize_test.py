import concurrent.futures
import time

start_time = time.time()

def long_func(i,j,k):
    time.sleep(.1)
    return i,j,k

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [
        executor.submit(long_func, i, j, k)
        for i in range(0, 50)
        for j in range(0, 40)
        for k in range(0, 100)
    ]
    
    for future in concurrent.futures.as_completed(futures):
        print(future.result())

end_time = time.time() - start_time
print(end_time)