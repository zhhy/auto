import datetime


def loadfile(file):
    res_infos = {}
    begin_flag = False
    num = 0
    with open(file,'r') as f:
        lines =f.readlines()
        for line in lines:
            if 'icmp_seq=0' in line:
                begin_flag = True
                res_infos[num] = []
            if 'now canceling' in line:
                begin_flag = False
                num += 1
            if begin_flag == True:
                res_infos[num].append(line)
    #print(res_infos.keys())
    return res_infos

def parse_log(infos):
    rtt_res = {}
    time_res = {}
    for key in infos.keys():
        rtt_res[key] = []
        time_res[key] = []
        print('---------')
        for line in infos[key]:
            if 'icmp_seq=' in line:
                rtt_res[key].append(float(line.split('delay=')[-1].split(' ')[0]))
                log_time = ' '.join(line.split(' ')[0:2]).strip()
                dt = datetime.datetime.strptime(log_time, '%Y-%m-%d %H:%M:%S.%f')
                time_res[key].append(dt.timestamp())

            if 'timeout' in line:
                rtt = 0
                rtt_res[key].append(rtt)
                log_time = ' '.join(line.split(' ')[0:2]).strip()
                dt = datetime.datetime.strptime(log_time, '%Y-%m-%d %H:%M:%S.%f')
                time_res[key].append(dt.timestamp())
    return rtt_res,time_res



def output(rtt_res,time_res):
    rtttrace={}
    lossrate={}
    rtt = [[] for i in range(1000)]
    base = 0
    n = 0
    num = 0


    for key in time_res.keys():

        rtttrace[key] = []
        lossrate[key]= []
        for i in range(len(time_res[key])):
            if time_res[key][i] - time_res[key][base]<0.1:
                #print(rtt)
                rtt[n].append(rtt_res[key][i])
                i +=1
            else:
                base = i
                n +=1
        for i in range(len(rtt)):
            if len(rtt[i]) != 0:
                #print(max(rtt[i]))
                rtttrace[key].append(max(rtt[i]))
                #print(rtt[i])
                for j in rtt[i]:
                   if j == 0:
                        num +=1
                lossrate[key].append(num/len(rtt[i])*100)
                num = 0

        print(lossrate[key])
        print(rtttrace[key])

        with open(f'd:\wjl\_lossrate{key}.txt', "w", ) as f:
            for i in range(len(lossrate[key])):
                f.write(str(lossrate[key][i]))
                f.write('\n')
        f.close()
        with open(f'd:\wjl\_rtttrace{key}.txt', "w", ) as f:
            for i in range(len(rtttrace[key])):
                f.write(str(rtttrace[key][i]))
                f.write('\n')
        f.close()




res_info = loadfile('d://log/pi_ping.txt')
rtt,time = parse_log(res_info)
#print(len(res_info))
file_path1 = 'D:\wjl\_lossrate.txt'
file_path2 = 'D:\wjl\_rtttrace.txt'
output(rtt,time)
