# -*- coding:utf-8 -*-
import time

filename = r"e:\log\psdemux_log.txt"

# filename = r"/Users/liminglei/Desktop/log/psdemux_log.txt"

pstreams = {}

with open(filename) as f:
    lines = f.readlines()

now = time.strftime('%Y-%m-%d-%H-%M-%S')
print(now)
for line in lines:

    if 'global_psdemux_getinstance' in line and 'arrayindex' in line:
        streaminfo = line.split(" ")
        print(streaminfo)
        stream_id = streaminfo[streaminfo.index('global_psdemux_getinstance') + 1]
        stream_url = streaminfo[streaminfo.index('global_psdemux_getinstance') + 2]
        pstreams[stream_id] = stream_url.rstrip()

for stream in pstreams.keys():

    f3 = []
    for line in lines:
        if f"psdemux({stream}) pstream(0) setplay" in line:
            lineinfo = line.split(' ')
            f3.append(int(lineinfo[lineinfo.index('dura') + 1]))
    print(f3, stream)
    if len(f3) > 0:
        print(sum(f3) - f3[0])
        总计 = sum(f3)
        平均 = 总计 / 5
        print(f'流id:{stream}')
        print(f'url:{pstreams[stream]}')
        print(f'卡顿时长：{f3}\n共计:{len(f3)}次\n总计:{总计}\n平均时长:{平均}')