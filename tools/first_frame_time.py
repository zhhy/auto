# -*- coding:utf-8 -*-

import re
filename = r"E:\log\psdemux_log.txt"

pstreams = {}

with open(filename) as f:
    lines = f.readlines()

for line in lines:

    if 'psdemux_probe' in line:
        streaminfo = line.split(" ")
        stream_id = streaminfo[streaminfo.index('psdemux_probe') + 1]
        stream_url = streaminfo[streaminfo.index('psdemux_probe') + 2]
        pstreams[stream_id] = stream_url.rstrip()




first_frame = []
demuxinit=[]
pzb=[]
conn=[]
open=[]
probe=[]
buffering=[]
start=[]


for line in lines:
    if "first_frame_time" in line:
        lineinfo = line.split(' ')
        first_frame.append(re.findall('^\d*\w*',lineinfo[lineinfo.index('first_frame_time') + 1]))

        #f3.append(lineinfo[lineinfo.index('first_frame_time') + 1])

for line in lines:
    if "setplay time:" in line:
        lineinfo = re.split(r'\W+',line)
        demuxinit.append(lineinfo[lineinfo.index('init')+1])
        pzb.append(lineinfo[lineinfo.index('pzb')+1])
        conn.append(lineinfo[lineinfo.index('conn')+1])
        open.append(lineinfo[lineinfo.index('open')+1])
        probe.append(lineinfo[lineinfo.index('probe') + 1])
        start.append(int(lineinfo[lineinfo.index('start')+2])-int(lineinfo[lineinfo.index('start')+1]))
        buffering.append(lineinfo[lineinfo.index('buffering') + 1])






i=0
while i<len(first_frame):
    print(f'秒开时间：{first_frame[i]},demuxinit时间:{demuxinit[i]},连接pzb server时间:{pzb[i]},http建立连接到server回应时间：{conn[i]},下发数据时间：{open[i]},收到meta信息时间：{probe[i]},近似等于音频设备打开时间：{start[i]},缓冲时间：{buffering[i]}')
    i=i+1
