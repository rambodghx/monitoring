from io import TextIOWrapper
import psutil
import gpustat
import time 
from time import sleep

def print_device_inf():
    print("-------------Device Info [CPU]-------------")
    print(get_cpu_info())
    print("-------------Device Info [RAM]-------------")
    print(get_ram_info())
    print("-------------Device Info [DISK]-------------")
    print(get_disk_info())
    print("-------------Device Info [GPU]-------------")
    print(get_gpu_info())

def get_cpu_info() -> str:
    freq = psutil.cpu_freq(percpu=True)
    cpuFreqs = ""
    for id,fr in enumerate(freq):
        cpuFreqs += "[{}] {} MHz \n".format(id,fr.max)
    return cpuFreqs

def get_ram_info() -> str:
    memInfo = psutil.virtual_memory()
    totalMem = memInfo.total/(1024*1024*1024)
    return "Total RAM : "+"{:.2f}".format(totalMem)+" Gb"

def get_disk_info() -> str:
    totalDisk = psutil.disk_usage("/").total/(1024*1024*1024)
    return "Total DISK : {:.2f} Gb".format(totalDisk)


def get_gpu_info() -> str:
    gpus = gpustat.GPUStatCollection[0].new_query().jsonify().get("gpus")
    res = ""
    for gp in gpus:
        res += "[{}] {} {} Mb".format(gp["index"],gp["name"],gp["memory.total"])
    return res


def get_cpu_load() -> str:
    percs = psutil.cpu_percent(percpu=True)
    res = "CPU Util : "
    for (i,p) in enumerate(percs):
        res += "[CORE({}) {}%]\t".format(i,p)
    temps = psutil.sensors_temperatures()["coretemp"]
    res += "\nCPU Temps : "
    for (i,t) in enumerate(temps):
        res += "[UNIT({}) {}C]\t".format(i,t.current)
    return res

def get_available_ram() -> str:
    memInfo = psutil.virtual_memory()
    availInGb = memInfo.available/(1024*1024*1024)
    res = "{:.2f} Gb - {}%".format(availInGb,memInfo.percent)
    return res

def get_gpu_loads() -> str:
    info = gpustat.GPUStatCollection[0].new_query().jsonify()["gpus"]
    res = ""
    for gpu in info:
        res += "{} : {}Mb - {}% - {}C".format(gpu["name"],gpu["memory.used"],gpu["utilization.gpu"],gpu["temperature.gpu"])
    return res



def create_open_file(file) -> TextIOWrapper:
    unix = time.time()
    rfile = open("{}/{}.csv".format(file,unix),mode="w")
    rfile.write("timestamp,unit,detail\n")
    return rfile

def write(file:TextIOWrapper):
    cpu = get_cpu_load()
    ram = get_available_ram()
    gpu =get_gpu_loads()
    date = time.time()
    file.write("{},{},{}\n".format(date,"cpu",cpu))
    file.write("{},{},{}\n".format(date,"gpu",gpu))
    file.write("{},{},{}\n".format(date,"ram",ram))

print_device_inf()

update_interval = -1
while True:
    try:
        update_interval = int(input("Please enter updating interval in seconds [1-5] : "))
    except:
        print("--> Enter Valid Number!")
        continue;   
    if not(0 <= update_interval <= 5):
        print("--> please enter between 1-5")
        continue
    break

print("--> Interval has been set on "+str(update_interval)+"s")

file = None
while True:
    try:
        fileName = input("Enter export file folder : ")
        file = create_open_file(fileName)
    except:
        print("--> Folder not found or permission denied!!!")
        continue;  
    break;

while True:
    sleep(update_interval)
    print("\033c", end="")
    print(get_cpu_load())
    print(get_available_ram())
    print(get_gpu_loads())
    write(file)
