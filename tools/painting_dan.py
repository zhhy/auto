# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import math as math
import re
import time

now = time.strftime('%Y-%m-%d-%H-%M-%S')

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
    curr_videobr, databr= [], []

    f = open(filename)
    lines = f.readlines()
    for line in lines:
        line_index = line.find('CheckTrans -- delay')
        s_index = line.find('changeto')
        if line_index > 0 and s_index == -1:
            # print(line)
            st = re.split(r'\W+',line)
            # print(s_index)
            #delayms.append(int(st[st.index('delay')+1]))
            #databr.append(int(st[st.index('databr')+1]))
            #netbr.append(int(st[st.index('netbr')+1]))
            curr_videobr.append(int(st[st.index('curbr') + 1]))
            #socketbuf.append(int(st[st.index('sock') + 1]))
    print(line_index)
    info={'curr_videobr':curr_videobr}
    return info
	
def get_info1(filename):
    delay, throughput, socketbuf= [], [], []

    f = open(filename)
    lines = f.readlines()
    for line in lines:
        line_index = line.find('CheckTransStatus -- stat')
        if line_index > 0 :
            # print(line)
            st = re.split(r'\W+',line)
            # print(s_index)
            delay.append(int(st[st.index('stat')+1]))
            throughput.append(int(st[st.index('stat')+2]))
            socketbuf.append(int(st[st.index('stat')+3]))
            #socketbuf.append(int(st[st.index('sock') + 1]))
    #print(socketbuf)
    info={'delay': delay,'throughput':throughput,'socketbuf':socketbuf}
    #print(info)
    return info
	


def paint(info1,info2,name):
    painting_infos = [f"rc=1 {name}:", max(info1[name]), min(info1[name]),
           round(average(info1[name]), 2), round(var(info1[name], average(info1[name])), 2)]

    painting_infos1 = [f"rc=2 {name}:", max(info2[name]), min(info2[name]),
                      round(average(info2[name]), 2), round(var(info2[name], average(info2[name])), 2)]

    #print(info1[name])
    #设置纵横坐标
   
    y = max(max(info1[name]), max(info2[name]))




    plt.ylim(0, y*1.1)


    #
    #plt.text(45, y*1.1+y/20, painting_infos, fontsize=10, color='black')
    plt.text(45, y*1.1+y/20*2, painting_infos1, fontsize=10, color='black')

    #示例
    #plt.plot(info1[name], color='red', linewidth=0.3, linestyle="-", label=f"rc=1 {name}")
    plt.plot(info2[name], color='green', linewidth=0.3, linestyle="-", label=f"rc=2 {name}")
    plt.legend(loc='upper left', frameon=False)

    plt.savefig(f'f://logs/iroom/painting_{name}.png')
    plt.close()
    
    
def paint1(info,name):
    painting_infos1 = [f"rc=2 {name}:", max(info[name]), min(info[name]),
                      round(average(info[name]), 2), round(var(info[name], average(info[name])), 2)]

    #print(info1[name])
    #设置纵横坐标
   
    y = max(max(info[name]), max(info[name]))




    plt.ylim(0, y*1.1)


    #
    #plt.text(45, y*1.1+y/20, painting_infos, fontsize=10, color='black')
    plt.text(45, y*1.1+y/20*2, painting_infos1, fontsize=10, color='black')

    #示例
    #plt.plot(info1[name], color='red', linewidth=0.3, linestyle="-", label=f"rc=1 {name}")
    plt.plot(info[name], color='green', linewidth=0.3, linestyle="-", label=f"rc=2 {name}")
    plt.legend(loc='upper left', frameon=False)

    plt.savefig(f'f://logs/iroom/{now}_{name}.png')
    plt.close()

file_info=get_info("f://logs/iroom/pslstreaming_log.txt")
#file_info1=get_info("f://logs/iroom/pslstreaming_log1.txt")
#file_info2=get_info1("e://log/pslstreaming_log.txt")
#file_info3=get_info1("e://log/pslstreaming_log1.txt")


#paint(file_info2,file_info3,'delay')
#paint(file_info,file_info1,'databr')
#paint(file_info2,file_info3,'throughput')
#paint(file_info,file_info1,'curr_videobr')
paint1(file_info,'curr_videobr')
#paint(file_info2,file_info3,'socketbuf')