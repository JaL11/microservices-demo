'''

Author: Ming Yeh Oliver Cheung

Copyright (c) 2021 Wise CSE Group 1
'''
import psutil
from threading import Thread
import time
import tracemalloc
import prometheus_client

class Monitor(Thread):
    def __init__(self, delay):
        super(Monitor, self).__init__()
        self.system_usage = prometheus_client.Gauge('system_usage',
                            'Hold current system resource usage',
                            ['resource_type'])
        prometheus_client.start_http_server(9999)
        self.stopped = False
        self.delay = delay # Time between calls to GPUtil
        tracemalloc.start()
        self.start_time = None
        self.start()

    def run(self):
        while not self.stopped:
            current_ram, ath_ram = tracemalloc.get_traced_memory()
            current_ram = current_ram / 10**6
            self.system_usage.labels('CPU').set(psutil.cpu_percent())
            self.system_usage.labels("Process_Memory").set(current_ram)
            self.system_usage.labels("Peak_Memory").set(ath_ram/ 10**6)
            time.sleep(self.delay)

    def stop(self):
        current, peak = tracemalloc.get_traced_memory()
        logging.info(f"Peak memory usage was {peak / 10**6}MB")
        tracemalloc.stop()
        self.stopped = True


if __name__ == "__main__":
    mon = Monitor(1)