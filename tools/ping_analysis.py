# -*- coding:utf-8 -*-
import os
import datetime
import matplotlib.pyplot as plt
import numpy as np


def parse_log(file):
    res_infos = {}
    begin_flag = False
    num = 0
    res_total_info = {}
    with open(file, 'r') as f:
        info = f.read().split('\n')
        for line in info:
            if '56 data bytes' in line:
                begin_flag = True
                res_infos[num] = []
            if 'packets received' in line and 'packet loss' in line:
                begin_flag = False
                res_total_info[num] = []
                # print(line, '\n')
                # print(info[info.index(line)+1], '\n')
                res_total_info[num].append(f"{' '.join(line.split(' ')[0:2]).strip()}")
                # res_total_info[num].append(f"{info[info.index(line)+1]}")
                num += 1
            if begin_flag:
                res_infos[num].append(line)
                # print(line)
    return res_infos, res_total_info


def analysis(infos, res_total_info):
    rtt_res = {}
    time_res = {}
    for key in infos.keys():
        rtt_res[key] = []
        time_res[key] = []
        print('---------')
        for line in infos[key]:
            if 'time=' in line:
                # print(' '.join(line.split(' ')[0:2]))
                rtt = line.split('time=')[-1]
                rtt = float(rtt.split(' ')[0])
                rtt_res[key].append(rtt)
                # if rtt > 15:
                #     print(line)
                log_time = ' '.join(line.split(' ')[0:2]).strip()
                # time_res = line.split(' ')[0:2]
                # log_time = loginfo[0].strip().split('#')[1].strip().split('(')[0]
                dt = datetime.datetime.strptime(log_time, '%Y-%m-%d %H:%M:%S.%f')
                time_res[key].append(dt.timestamp())
            elif 'timeout' in line:
                rtt = 0
                # print(line)
                rtt_res[key].append(rtt)

        plt.figure(key)

        min_time = int(min(time_res[key]))
        # print(int(min(time_res[key])))
        parse_time = [i - min_time for i in time_res[key]]
        # print(max(rtt_res[key]))
        plt.ylim(0, max(rtt_res[key]))
        # plt.xlim(0, max(parse_time)+5)
        if max(rtt_res[key]) < 120:
            plt.yticks(np.arange(0, max(rtt_res[key]), 5))

        # plt.xticks(np.arange(0, parse_time[-1], 10))
        plt.text(10 , max(rtt_res[key]), f"{res_total_info[key]}")
        plt.plot(rtt_res[key], color='red', markersize=1, linewidth=0.5, linestyle="-", label="rtt")

        plt.legend()
        plt.savefig(os.path.join('/Users/liminglei/Desktop/log/2', f'ping_{key}.png'))
        plt.close()
        # plt.show()
    # print(rtt_res)
    # print(time_res)


logfile = '/Users/liminglei/Desktop/log/pi_ping 2.txt'
infos, res_total_info = parse_log(logfile)
analysis(infos, res_total_info)