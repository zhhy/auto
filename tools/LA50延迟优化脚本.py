# -*- coding:utf-8 -*-

import matplotlib.pyplot as plt
import sys
import os


def painting(info, label_info, paint_img_dir):

    plt.text(len(info)*0.6, max(info), f"max: {max(info)}\nmin: {min(info)}\navg:{sum(info)/len(info)}", fontsize=10,
             color='black')

    # 示例
    plt.plot(info, color='red', linewidth=0.3, linestyle="-", label=label_info)
    plt.legend(loc='upper left', frameon=False)

    # plt.show()
    plt.savefig(f"{paint_img_dir}/{label_info}.png")
    plt.close()


def parse_log(filepath):
    cbuff_info, pzvt_info, freeze_time_info = [], [], []
    stream_id = None

    with open(filepath) as f:
        lines = f.readlines()

    for line in lines:
        if 'psdemux_probe' in line:
            streaminfo = line.split(" ")
            if len(streaminfo) > streaminfo.index('psdemux_probe') + 2:
                stream_id = streaminfo[streaminfo.index('psdemux_probe') + 1]
                stream_url = streaminfo[streaminfo.index('psdemux_probe') + 2]
                print(stream_url)

        if f"psdemux({stream_id}) pstream(0) delay" in line:
            lineinfo = line.split(' ')
            cbuff_info.append(int(lineinfo[lineinfo.index('delay') + 1]))
            pzvt = lineinfo[lineinfo.index('playavg') + 1]
            pzvt_info.append(int(pzvt.split('(')[0]))

        if f"psdemux({stream_id}) pstream(0) setplay" in line:
            lineinfo = line.split(' ')
            freeze_time_info.append(int(lineinfo[lineinfo.index('dura') + 1]))

    paint_img_dir = os.path.dirname(filepath)
    painting(cbuff_info, 'delay', paint_img_dir)    # delay 就是cbuffer
    painting(pzvt_info, 'playavg', paint_img_dir)
    freeze_time = sum(freeze_time_info)
    freeze_count = len(freeze_time_info)
    print(f"freeze次数:{freeze_count}, 总时长:{freeze_time}ms，平均时长：{freeze_time/freeze_count}ms")


if __name__ == '__main__':
    filepath = r"E:\log\psdemux_log.txt"
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    parse_log(filepath)