import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
from scipy.interpolate import make_interp_spline, BSpline
from multiprocessing import Process
import speedtest
import datetime
import time
import os.path
from os import path
#need to add way to handle the test.csv being empty/low in amount

s = speedtest.Speedtest()
def testspeed():
    while True:
        print("testing speed")
        if path.exists('test.csv'):
            with open('test.csv', mode='a', newline='') as speedcsv:
                csv_writer = csv.DictWriter(speedcsv, fieldnames=['time', 'downspeed', 'upspeed'])
            speedcsv = open('test.csv',mode='a',newline='')
            csv_writer = csv.DictWriter(speedcsv, fieldnames=['time', 'downspeed', 'upspeed'])
            time_now = datetime.datetime.now().strftime("%H:%M:%S")
            downspeed = round((round(s.download()) / 1048576), 2)
            upspeed = round((round(s.upload()) / 1048576), 2)
            csv_writer.writerow({
                'time': time_now,
                'downspeed': downspeed,
                "upspeed": upspeed
            })
            #csv_writer.writerow(time_now,downspeed,upspeed)
            print("added row",time_now)
            # 60 seconds sleep
            speedcsv.close()
            time.sleep(20)
        else:
            with open('test.csv',mode='w',newline='') as speedcsv:
                csv_writer = csv.DictWriter(speedcsv, fieldnames=['time', 'downspeed', 'upspeed'])

times = []
download = []
upload = []

style.use('seaborn-ticks')
fig = plt.figure()
ax1 = fig.add_subplot(1,2,1)
ax2 = fig.add_subplot(1,2,2)
lists = []

def animate(i):
    if path.exists('test.csv'):
            with open('test.csv', 'r') as csvfile:
                times = []
                download = []
                upload = []
                plots = csv.reader(csvfile, delimiter=',')
                #print(list(plots))
                lists = list(plots)[-100:]
                for x,row in enumerate(lists):
                    #print(x,row)
                    times.append(int(x))
                    download.append(float(row[1]))
                    upload.append(float(row[2]))
                if len(times) > 5:
                    times = np.array(times)
                    xnew = np.linspace(times.min(),times.max(),300)

                    spl = make_interp_spline(times, download, k=3)
                    downloadsmooth = spl(xnew)
                    downloadaverage = sum(download) / len(download)
                    uploadaverage = sum(upload) / len(upload)
                    spl2 = make_interp_spline(times,upload,k=3)
                    uploadsmooth = spl2(xnew)
                    ax1.clear()
                    ax2.clear()
                    #print(times, "\n", download, "\n", upload)
                    ax1.plot(xnew, downloadsmooth, label='download', color='#b52871')
                        ##F5B14C')
                    ax1.axhline(y=downloadaverage,color = 'pink',linestyle = 'dashed')
                    ax1.annotate(f'Average Download Rate = {round(downloadaverage,2)} Mb/s',xy=(80,downloadaverage*.9),xycoords = 'data')
                    ax2.axhline(y=uploadaverage,color = 'pink',linestyle = 'dashed')
                    ax2.annotate(f'Average Download Rate = {round(uploadaverage,2)} Mb/s',xy=(80,uploadaverage),xytext = (0,-20), textcoords='offset points',xycoords = 'data',arrowprops=dict(arrowstyle="->"))
                    ax2.plot(xnew, uploadsmooth, label='upload', color='#2CBDFE')
                    #ax1.plot(times,download)
                    #ax1.plot(times,upload)
                    ax1.set_xlabel('Time')
                    ax1.set_ylabel('Speed in Mb/s')
                    ax2.set_xlabel('Time')
                    ax2.set_ylabel('Speed in Mb/s')
                    ax1.set_title("Internet Download Speed")
                    ax2.set_title("Internet Upload Speed")
                else:
                    ax1.clear()
                    ax2.clear()
                    #print(times, "\n", download, "\n", upload)
                    ax1.plot(times, download, label='download', color='#b52871')
                        ##F5B14C')
                    ax2.plot(times, upload, label='upload', color='#2CBDFE')
                    #ax1.plot(times,download)
                    #ax1.plot(times,upload)
                    ax1.set_xlabel('Time')
                    ax1.set_ylabel('Speed in Mb/s')
                    ax2.set_xlabel('Time')
                    ax2.set_ylabel('Speed in Mb/s')
                    ax1.set_title("Internet Download Speed")
                    ax2.set_title("Internet Upload Speed")
def animator():
    ani = animation.FuncAnimation(fig, animate,interval = 2000)
    plt.show()

if __name__ == '__main__':
    print("Program will take about 5 min to gain intitial datapoints")
    p1 = Process(target = testspeed)
    p1.start()
    p2 = Process(target = animator)
    p2.start()