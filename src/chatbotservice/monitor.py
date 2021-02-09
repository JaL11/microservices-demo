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

class Monitor(Thread):
    def __init__(self, delay):
        super(Monitor, self).__init__()
        self.stopped = False
        self.delay = delay # Time between calls to GPUtil
        self.ram = []
        self.current_ram = None
        tracemalloc.start()
        self.start_time = None
        self.p = LivePlot()
        self.x_vec = np.linspace(0,1,101)[0:-1]
        self.y_vec = np.zeros(len(self.x_vec))
        self.line1 = []
        self.start()

    def run(self):

        while not self.stopped:
            self.current_ram, _ = tracemalloc.get_traced_memory()
            self.current_ram = self.current_ram / 10**6
            self.ram.append(self.current_ram)

            self.y_vec[-1] = self.current_ram
            self.line1 = self.p.live_plotter(self.x_vec,self.y_vec,self.line1)
            self.y_vec = np.append(self.y_vec[1:],0.0)
            time.sleep(self.delay)

    def stop(self):
        current, peak = tracemalloc.get_traced_memory()
        print(f"Peak memory usage was {peak / 10**6}MB")
        tracemalloc.stop()
        self.stopped = True

class LivePlot:

    def __init__(self):
        super().__init__()
    
    def live_plotter(self, x_vec,y1_data,line1,identifier='',pause_time=0.1):
        if line1==[]:
            # this is the call to matplotlib that allows dynamic plotting
            plt.ion()
            fig = plt.figure(figsize=(13,6))
            ax = fig.add_subplot(111)
            # create a variable for the line so we can later update it
            line1, = ax.plot(x_vec,y1_data,'-o',alpha=0.8)        
            #update plot label/title
            plt.ylabel("RAM in MB")
            plt.title("Ram Usage")
            plt.savefig("Test")
        
        # after the figure, axis, and line are created, we only need to update the y-data
        line1.set_ydata(y1_data)
        # adjust limits if new data goes beyond bounds
        if np.min(y1_data)<=line1.axes.get_ylim()[0] or np.max(y1_data)>=line1.axes.get_ylim()[1]:
            plt.ylim([np.min(y1_data)-np.std(y1_data),np.max(y1_data)+np.std(y1_data)])
        # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
        plt.pause(pause_time)
        
        # return line so we can update it again in the next iteration
        return line1

if __name__ == "__main__":
    mon = Monitor(1)