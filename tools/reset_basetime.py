# -*- coding:utf-8 -*-
import sys

def get_new_log(logs):

    toggleMulitefalseindex = [logs.index(log) for log in logs if "toggleMute false" in log]
    toggleMulitetrueindex = [logs.index(log) for log in logs if "toggleMute true" in log]

    filedir = "/Users/liminglei/Downloads/"
    file_toogle = open(filedir+"tmpfile.txt",'w+')


    for togglefalse in toggleMulitefalseindex:
        for toggletrue in toggleMulitetrueindex:
            if toggletrue > togglefalse:
                print(toggletrue,togglefalse)
                # print(logs[togglefalse:toggletrue+1])
                for line in logs[togglefalse:toggletrue+1]:
                    file_toogle.write(line)
                break

    file_toogle.close()


def get_res_log():
    filedir = "/Users/liminglei/Downloads/"
    res = open(filedir + "res.txt", 'w+')

    with open(filedir + "tmpfile.txt", 'r+') as f:
        lines = f.readlines()

        for line in lines:
            if 'basetime' in line:
                print(True)
                res.write(line)
    res.close()





if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        logs = f.readlines()
    get_new_log(logs)
    get_res_log()