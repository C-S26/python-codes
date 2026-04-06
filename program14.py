#program to check process CPU usage  
import psutil

for proc in psutil.process_iter(['pid','name','cpu_percent']):
    if proc.info['cpu_percent'] > 4:
        print("High CPU usage:", proc.info)
    else:
        print("its low CPU usage:", proc.info)
