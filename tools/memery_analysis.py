# -*- coding:utf-8 -*-
import os
import matplotlib.pyplot as plt


def count_log(file):
    log_dir = os.path.dirname(file)
    push_files = []
    for logfile in os.listdir(log_dir):
        if 'pslstreaming' in logfile:
            print(logfile)
            push_files.append(os.path.abspath(logfile))
    res_push_file = os.path.join(log_dir)
    for i in reversed(push_files):

        print(i)
    # print(push_files.reverse())


def parse_log(file):
    meminfo = []
    with open(file, 'r') as f:
        lines = f.read().split('\n')
        for line in lines:
            if 'getMemInfo' in line:
                index = lines.index(line)
                meminfo.append(lines[index:index+5])
                # print(lines[index+2])
    res_total_mem = []
    for info in meminfo:
        mem = info[-1].split(": ")[1]
        res_total_mem.append(int(mem))
    print(res_total_mem)
    print(sum(res_total_mem)/len(res_total_mem))
    print(max(res_total_mem), min(res_total_mem))

    x = range(len(res_total_mem))
    y = max(res_total_mem)

    plt.xlim(0, len(x))
    plt.ylim(0, y*1.1)

    plt.text(10, y, f'totalUseMem: \nMax:{max(res_total_mem)},\nMin:{min(res_total_mem)},\nAvg:{sum(res_total_mem)/len(res_total_mem)}')
    plt.plot(res_total_mem, color='red', markersize=1, linewidth=0.5, linestyle="-", label="totalUseMem")
    # plt.legend(loc='upper left', frameon=False)
    plt.legend()

    plt.show()


logfile = '/Users/liminglei/Desktop/log/1/pslstreaming_log.txt'
# count_log(logfile)
parse_log(logfile)
