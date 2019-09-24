import re
import matplotlib.pyplot as plt

filename1 = r"d:/log/1.txt"
#filename2 = r"E:/log/iRzsrmp1-1.txt"
#filename3 = r"E:/log/iRzsrnmp-1.txt"

def loadfile(filename):
    reslt = []
    time = []
    with open(filename) as f:
        lines = f.readlines()
    for line in lines:
        if line.find('Delta') >0:
            deltainfo = line.split(" ")

            video = deltainfo[deltainfo.index('Delta')+1]
            if len(video)>4:
                reslt.append(line)
                time.append(deltainfo[deltainfo.index('May')+2])
    print(filename)
    for i in reslt:
        print(i)
    return reslt

def getinfo(filename):
    videodelta=[]
    audiodelta=[]
    time = []
    with open(filename) as f:
        lines = f.readlines()
    for line in lines:
        if line.find('Delta')>0:
            deltainfo = line.split(" ")
            videodelta.append(int(deltainfo[deltainfo.index("Delta")+1]))
            audiodelta.append(int(deltainfo[deltainfo.index("Delta")+2]))
            time.append(re.findall('\d+:\d+:\d+', line))
    info={"videodelta":videodelta,"audiodelta":audiodelta,'time':time}
    return info

def paint(info3,name):

    #m =max(max(info1[name]),max(info2[name]),max(info3[name]))
    #n = min(min(info1[name]),min(info2[name]),min(info3[name]))
    m = max(info3[name])
    n = min(info3[name])
    if m>500:
        y1 = m
    else:
        y1 = 1000
    if n<-2000:
        y2 = n
    else:
        y2 = -2000
    x = info3['time'][:]

    fig, ax = plt.subplots()

    # make ticks and tick labels
    xticks = range(0, len(x), 30)
    xticklabels = [x[i] for i in range(0,len(x),30)]
    plt.ylim(y2, y1)
    ax.plot(info3[name], color='green', linewidth=1, linestyle="-", label=f"delta")
    ax.plot(info3['videodelta'], color='red', linewidth=1, linestyle="-", label=f"videodelta")

    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels, rotation=15)
    print(xticks)
    plt.legend(loc='upper left', frameon=False)

    plt.savefig(f'd://log/painting_{name}.png')
    plt.close()

    plt.ylim(y2, y1)
    #plt.plot(info3[name], color='green', linewidth=1, linestyle="-", label=f"wifi{name}")
    #plt.plot(info2[name], color='black', linewidth=1, linestyle="-", label=f"mulpath without 4G{name}")
    #plt.plot(info1[name], color='red', linewidth=1, linestyle="-", label=f"mulpath{name}")
    #plt.legend(loc='upper left', frameon=False)

    #plt.savefig(f'e:/log/painting_{name}.png')
    #plt.close()

info1 = getinfo(filename1)
#info2 = getinfo(filename2)
#info3 = getinfo(filename3)

paint(info1,'audiodelta')