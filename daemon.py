import time
import json
import io
import psutil

#to run it
#nohup python -u daemon.py &

while True:
    time.sleep(1)
    try:
        for p in psutil.process_iter():
            if p.memory_percent() > 5 or p.cpu_percent(0.1) > 5:
                f = open('log.json',mode='a') 
                print(p.cpu_percent(0.1))
                f.write(json.dumps(p.as_dict(), default=str)+'\n')  
            
    #f.write(json.dumps(str(i)+'\n') )
    #f.flush()
                f.close()
    except:
        continue        