import re
import matplotlib.pyplot as plt

filename1 = r"E:/log/psdemux_log.txt"

def loadfile(filename):
    video = []
    with open(filename) as f:
        lines = f.readlines()
    for line in lines:
        if line.find('video decode frame time') > 0:
            deltainfo = line.split(" ")

            video.append(int(deltainfo[deltainfo.index('time') + 1]))
    return video

def getout(video):
    m = []
    n = []
    for i in video:
        if i< 10000:
            m.append(i)
    print(min(m))
    print(max(m))
    print(sum(m)/len(m))

v = loadfile(filename1)
getout(v)




