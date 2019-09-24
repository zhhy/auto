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
    delay1, delay2, curbr,time = [], [], [],[]

    f = open(filename,encoding='utf-8')
    lines = f.readlines()
    for line in lines:
        line_index = line.find('TransPacket_Packer -- Adjust -- delay')
        s_index = line.find('-->')
        if line_index > 0 and s_index == -1:
            #print(line)
            st = re.split(r'\W+',line)
            time.append(re.findall('\d+:\d+:\d+',line))
            #print(time)
            # print(s_index)
            #print(st[st.index('curbr')+1])
            delay1.append(int(st[st.index('delay')+1]))
            delay2.append(int(st[st.index('delay')+3]))
            curbr.append(int(st[st.index('curbr')+1]))


    info={'delay1': delay1,'delay2':delay2,'curbr':curbr,'time':time}
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
    ax.plot(info['delay1'], color='green', linewidth=1, linestyle="-", label=f"delay1")
    ax.plot(info['delay2'], color='red', linewidth=1, linestyle="-", label=f"delay2")
    ax.plot(info['curbr'], color='black', linewidth=1, linestyle="-", label=f"curbr")

    # set ticks and tick labels
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels, rotation=15)
    print(xticks)
    plt.legend(loc='upper left', frameon=False)

    plt.savefig(f'd://log/delay.png')
    plt.close()


    # show the figure
    #plt.show()
    '''
    painting_infos = [f"delay1:", max(info['delay1']), min(info['delay1']),
                      round(average(info['delay1']), 2), round(var(info['delay1'], average(info['delay1'])), 2)]
    painting_infos1 = [f"delay2:", max(info['delay2']), min(info['delay2']),
                      round(average(info['delay2']), 2), round(var(info['delay2'], average(info['delay2'])), 2)]
    painting_infos2 = [f"curbr:", max(info['curbr']), min(info['curbr']),
                      round(average(info['curbr']), 2), round(var(info['curbr'], average(info['curbr'])), 2)]

    # trick to get the axes
    fig, ax = plt.subplots()

    # make ticks and tick labels
    xticks = range(0, len(info['time']), 2)
    xticklabels = info['time']



    #print(x)
    #plt.plot(x, 1: 24)
    #print(max(info['curbr']))
    #x = len(info['delay1'])
    y = max(info['delay1'])

# plot data
    ax.plot(x, y)

# set ticks and tick labels
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels, rotation=15)
    plt.text(45, y*1.1+y/20, painting_infos, fontsize=10, color='black')
    plt.text(45, y*1.1+y/20*2, painting_infos1, fontsize=10, color='black')
    plt.text(1000, y * 1.1 + y/20 * 2, painting_infos2, fontsize=10, color='black')


    #plt.ylim(0, y * 1.1)
    #plt.xlim(0, x * 1.1)

    #plt.plot(info['delay1'], color='green', linewidth=1, linestyle="-", label=f"delay1")
    #plt.plot(info['delay2'], color='red', linewidth=1, linestyle="-", label=f"delay2")
    #plt.plot(info['curbr'], color='black', linewidth=1, linestyle="-", label=f"curbr")
    plt.legend(loc='upper left', frameon=False)

    plt.savefig(f'e://log/delay.png')
    plt.close()
'''

file_info=get_info("d://log/pslstreaming_log.txt")
paint(file_info)