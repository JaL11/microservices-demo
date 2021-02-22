'''

Author: Ming Yeh Oliver Cheung

Copyright (c) 2021 Wise CSE Group 1
'''

import matplotlib.pyplot as plt
plt.style.use('ggplot')
import numpy as np
import psutil
from threading import Thread
import time
import tracemalloc
import prometheus_client

class Monitor(Thread):
    """ Monitors a process, by cpu usage, ram usage
        and can also measure request time. Results are opened on a prometheus
        client where it can be scrapped to a server on port 9999
    Args:
        Thread ([type]): [description]
    """
    def __init__(self, delay):
        super(Monitor, self).__init__()
        self.system_usage = prometheus_client.Gauge('system_usage',
                            'Hold current system resource usage',
                            ['resource_type'])
        prometheus_client.start_http_server(9999)
        self.stopped = False
        self.started_request = False
        self.request_time = 0.0
        self.all_request_time = 0.0
        self.requests = 0
        self.stopped = False
        self.delay = delay # Time between calls to GPUtil
        tracemalloc.start()
        self.start_time = None
        self.start()

    def run(self):
        """ updates and measures system information every delay 
        """
        while not self.stopped:
            current_ram, ath_ram = tracemalloc.get_traced_memory()
            self.system_usage.labels('CPU').set(psutil.cpu_percent())
            self.system_usage.labels("Process_Memory").set(current_ram/ 10**6)
            self.system_usage.labels("Peak_Memory").set(ath_ram/ 10**6)
            if self.started_request:
                request_average = self.all_request_time/self.requests
                self.system_usage.labels("Average Request Time").set(request_average)
                self.system_usage.labels("Latest Request Time").set(self.request_time)
            time.sleep(self.delay)

    def stop(self):
        """ stops tracing ram when application stops
        """
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        self.stopped = True

    def start_request(self):
        """ starts timer for a request
        """
        self.start_time = time.perf_counter()

    def stop_request(self):
        """stop timer for a request and handles 
        time measurement
        """
        self.stop_time = time.perf_counter() - self.start_time
        self.set_request_time(self.stop_time)

    def set_request_time(self, time):
        """ updates newest request time and amount of requests timed

        Args:
            time (int): time of a request
        """
        self.request_time = time
        self.all_request_time += time
        self.requests += 1
        self.started_request = True

if __name__ == "__main__":
    mon = Monitor(1)
    mon.start_request()
    mon.stop_request()