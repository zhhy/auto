import re
import matplotlib.pyplot as plt


filename1 = r"D:/logs/2.txt"

def loadfile(filename):
    reslt = []
    time = []
    with open(filename) as f:
        lines = f.readlines()
    for line in lines:
        if line.find('TarBuf') >0:
            deltainfo = line.split(" ")

            tarbuf = deltainfo[deltainfo.index('TarBuf')+1]
            if len(tarbuf)>4:
                reslt.append(line)
                time.append(deltainfo[deltainfo.index('May')+2])
    print(filename)
    for i in reslt:
        print(i)
    return reslt

def getinfo(filename):
    tarbuf=[]
    time = []
    with open(filename) as f:
        lines = f.readlines()
    for line in lines:
        if line.find('TarBuf')>0:
            deltainfo = line.split(" ")
            tarbuf.append(int(deltainfo[deltainfo.index("TarBuf")+1]))
            time.append(re.findall('\d+:\d+:\d+', line))
    info={"tarbuf":tarbuf,'time':time}
    return info

def paint(info3,name):

    #m =max(max(info1[name]),max(info2[name]),max(info3[name]))
    #n = min(min(info1[name]),min(info2[name]),min(info3[name]))
    m = max(info3[name])
    n = min(info3[name])
    if m>1000:
        y1 = m
    else:
        y1 = 800
    if n<1000:
        y2 = n
    else:
        y2 = 1600
    x = info3['time'][:]

    fig, ax = plt.subplots()

    # make ticks and tick labels
    xticks = range(0, len(x), 30)
    xticklabels = [x[i] for i in range(0,len(x),30)]
    plt.ylim(y2, y1)
    ax.plot(info3['tarbuf'], color='red', linewidth=1, linestyle="-", label=f"tarbuf")
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels, rotation=15)
    print(xticks)
    plt.legend(loc='upper left', frameon=False)

    plt.savefig(f'd://logs/painting_{name}.png')
    plt.close()

    plt.ylim(y2, y1)

info1 = getinfo(filename1)

paint(info1,'tarbuf')