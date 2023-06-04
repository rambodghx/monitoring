#-- Attention from RambodGh : Main code was in https://qxf2.com/blog/generate-cpu-load/ 

import time
import math 
import sys 
import multiprocessing

 

interval = 0
while True:
    try:
        interval = int(input("Please enter interval in seconds : "))
    except:
        print("Please enter valid value ")
        continue
    if interval < 1 :
        print("Please enter number more than 0")
        continue
    break

load = 0
while True:
    try:
        load = int(input("Please enter overall load [0-70]% :"))
    except:
        print("Please enter valid number")
        continue
    if not(0 < load < 70) :
        print("Please enter number more than 0 and less than 70 (for your safety :) )")
        continue
    break

def generate_cpu_load(interval=interval,utilization=load):
    start_time = time.time()
    for i in range(0,int(interval)):
        while time.time()-start_time < utilization/100.0:
            a = math.sqrt(64*64*64*64*64)
        time.sleep(1-utilization/100.0)
        start_time += 1

print("Generating {}% load for {}s started now you can check you load...".format(load,interval))
print("** For force shutdown please Ctrl + c ")
processes = []
for _ in range (multiprocessing.cpu_count()):
    p = multiprocessing.Process(target = generate_cpu_load)
    p.start()
    processes.append(p)
for process in processes:
    process.join()
print("Load completed ;) ")
