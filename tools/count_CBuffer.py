# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import pandas as pd
import math as math
import datetime
import re

def var(list, avg):
    var1 = 0
    for i in list:
        var1 += float((i - avg) ** 2 * 1.0)
    var2 = (math.sqrt(var1 / (len(list) - 1) * 1.0))
    return var2


def average(list):
    avg = sum(list) / float(len(list) * 1.0)
    return avg

def get_info(filename):
    cbuffer1, cbuffer2, tbuffer,time = [], [], [],[]

    f = open(filename)
    lines = f.readlines()
    for line in lines:
        line_index = line.find('CBuffer')
        s_index = line.find('-->')
        if line_index > 0 and s_index == -1:
            #print(line)
            st = re.split(r'\W+',line)
            time.append(re.findall('\d+:\d+:\d+',line))
            #print(time)
            # print(s_index)
            #print(st[st.index('curbr')+1])
            cbuffer1.append(int(st[st.index('CBuffer')+1]))
            cbuffer2.append(int(st[st.index('CBuffer')+2]))
            tbuffer.append(int(st[st.index('CBuffer')+3]))


    info={'client_cbuffer': cbuffer1,'server_cbuffer':cbuffer2,'tbuffer':tbuffer,'time':time}
    #print(info)
    return info
def paint(info):

    x = info['time'][:]
    # trick to get the axes
    fig, ax = plt.subplots()

    # make ticks and tick labels
    xticks = range(0, len(x), 250)
    xticklabels = [x[i] for i in range(0,len(x),250)]

    # plot data
    ax.plot(info['client_cbuffer'], color='green', linewidth=1, linestyle="-", label=f"client_cbuffer")
    ax.plot(info['server_cbuffer'], color='red', linewidth=1, linestyle="-", label=f"server_cbuffer")
    ax.plot(info['tbuffer'], color='black', linewidth=1, linestyle="-", label=f"tbuffer")

    # set ticks and tick labels
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels, rotation=15)
    print(xticks)
    plt.legend(loc='upper left', frameon=False)

    plt.savefig(f'd://logs/CBuffer.png')
    plt.close()

file_info=get_info("d://logs/2.txt")
paint(file_info)