import threading
import subprocess
import time
import re
from queue import Queue

WORD_THREAD = 50

IP_QUEUE = Queue()
for i in range(9,18):
    IP_QUEUE.put('192.168.50.'+str(i))
def ping_ip():
    while not IP_QUEUE.empty():
        ip = IP_QUEUE.get()
        res = subprocess.Popen('ping -c 2 -w 5 %s' % ip, stdout=subprocess.PIPE, shell=True)

        out = res.stdout.read().decode('utf-8')
        out_array=out.split('\n')
        out_array=[x for x in out_array if x!='']

        rttStr=out_array[-1]
        pattern = re.compile(r'(-?\d+\.\d+)', re.I)
        m = pattern.findall(rttStr)
        f = open("ping_all.prom", "a")
        print(
                '# TYPE', ip+'_ms', 'gauge\n',
                ip+'_ms', m[1], file = f
                )
        f.close()
if __name__ == '__main__':
    ip = IP_QUEUE.get()
    f = open("ping_all.prom", "w")
    f.close()
    threads = []
    start_time = time.time()
    for i in range(WORD_THREAD):
        thread = threading.Thread(target=ping_ip)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print('time：%s' % (time.time() - start_time))
