# -*- coding:utf-8 -*-

import os
import datetime
import sys


def find_log(info, res, findlog, res_index=1):
    if findlog in info:
        parse_info = info.split(' ')
        if isinstance(res_index, int):
            locate_str = findlog.strip().split(' ')[-1]
            drop_seq = parse_info[parse_info.index(locate_str) + res_index]
            res.append(int(drop_seq))

        else:
            res.append(info)
        # print(f"the {findlog} is {drop_seq}")
    return res


def print_log(res_list, findlog, index):
    if len(res_list) > 0:
        if isinstance(index, int):
            if 'dura' in findlog:
                # print(res_list)
                res = sum(res_list)
                print(f"the result of {findlog} is {res}")
                return
            res = len(res_list)
            print(f"the result of {findlog} is {res}")
        else:
            print(f"the result of {findlog} is")
            res_info = []
            for info in res_list:
                audio_num = info.strip().split(' ')[10]
                res_info.append(audio_num)

            for n in set(res_info):
                count = 0
                for i in res_info:
                    if i == n:
                        count +=1
                print(f'{n} : {count}')
    else:
        print(f'the result of {findlog} is 0')



# {findstr:index}
def parse_log(loginfo, find_part):
    num = 1
    log_time = loginfo[0].strip().split('#')[1].strip().split('(')[0]
    dt = datetime.datetime.strptime(log_time, '%Y %b %d %H:%M:%S.%f')
    start_time = dt.timestamp()
    prepare_list = locals()
    print(f'第{num}分钟,{dt}日志：')
    for key in find_part:
        key_valu = '_'.join(key.strip().split(' '))
        prepare_list['res'+key_valu] =[]
    for log in loginfo:
        if '(' not in log:
            continue
        log_time = log.strip().split('#')[1].strip().split('(')[0]
        log_dt = datetime.datetime.strptime(log_time, '%Y %b %d %H:%M:%S.%f')
        floattime = log_dt.timestamp()
        if floattime - start_time < num * 60:
            for key in find_part:
                key_valu = '_'.join(key.strip().split(' '))
                res_key = prepare_list['res'+ key_valu]
                res_key = find_log(log, res_key, key, find_part[key])
                # print(f"drop seq is {drop_seq}")
        else:
            num += 1
            for key in find_part:
                key_valu = '_'.join(key.strip().split(' '))
                res_key = prepare_list['res' + key_valu]
                print_log(res_key, key, find_part[key])
            # print_log(drop_seqs, 'drop seq')
            print(f'第{num}分钟,{log_dt}日志：')
            for key in find_part:
                key_valu = '_'.join(key.strip().split(' '))
                prepare_list['res' + key_valu] = []
                res_key = prepare_list['res'+ key_valu]
                res_key = find_log(log, res_key, key, find_part[key])
                # print(f"drop seq is {drop_seq}")
    for key in find_part:
        key_valu = '_'.join(key.strip().split(' '))
        res_key = prepare_list['res' + key_valu]
        print_log(res_key, key, find_part[key])


def parse_demux_log(loginfo):
    num = 1
    log_time = loginfo[0].strip().split('#')[1].strip().split('(')[0]
    dt = datetime.datetime.strptime(log_time, '%Y %b %d %H:%M:%S.%f')
    start_time = dt.timestamp()
    prepare_list = locals()
    res_setplay = []
    res_dura = []
    res_freeze = []
    print(f'第{num}分钟,{dt}日志：')
    for log in loginfo:
        if '(' not in log:
            continue
        log_time = log.strip().split('#')[1].strip().split('(')[0]
        log_dt = datetime.datetime.strptime(log_time, '%Y %b %d %H:%M:%S.%f')
        floattime = log_dt.timestamp()
        if floattime - start_time < num * 60:
            res_setplay = find_log(log, res_setplay, '(0) setplay', 1)
            res_dura = find_log(log, res_dura, ' dura ', 1)
            res_freeze = find_log(log, res_freeze, ') setfreeze', 1)
        else:
            num += 1
            print_log(res_setplay, 'setplay', 1)
            print_log(res_setplay, 'dura', 1)
            print_log(res_setplay, 'setfreeze', 1)
            # print_log(drop_seqs, 'drop seq')
            print(f'第{num}分钟,{log_dt}日志：')
            res_setplay = []
            res_dura = []
            res_freeze = []
            res_setplay = find_log(log, res_setplay, '(0) setplay', 1)
            res_dura = find_log(log, res_dura, ' dura ', 1)
            res_freeze = find_log(log, res_freeze, ') setfreeze', 1)
    print_log(res_setplay, 'setplay', 1)
    print_log(res_setplay, 'dura', 1)
    print_log(res_setplay, 'setfreeze', 1)


def split_file(logfile, splitstr='connect='):
    loginfo = []
    with open(logfile, 'r') as f:
        for line in f:
            loginfo.append(line)
    connect_time = []
    for log in loginfo:
        if splitstr in log:
            # print(log)
            connect_time.append(loginfo.index(log))
    loginfo_res = []
    for ct in connect_time:
        index = connect_time.index(ct)

        if index == 0:
            loginfo_res.append(loginfo[0:ct])
        else:
            begin_index = connect_time[index - 1]
            loginfo_res.append(loginfo[begin_index:ct])
    loginfo_res.append(loginfo[connect_time[-1]::])
    print(len(loginfo_res))
    return loginfo_res


def merge_log(merge_log_dir, log_files):
    if os.path.exists(merge_log_dir):
        return
    with open(merge_log_dir, 'w') as f1:
        for file in log_files:
            with open(file, 'r', encoding='utf-8') as f2:
                for line in f2:
                    f1.write(line)


if __name__ == '__main__':
    filepath = sys.argv[1]
    # filepath = '/Users/liminglei/Desktop/log/2018-12-07_11-09-46__iLiveA50/psdemux_log.txt '
    log_dir = os.path.dirname(filepath)
    psdemux = []
    pslstreaming = []
    for logfile in os.listdir(log_dir):
        if 'psdemux' in logfile:
            psdemux.append(os.path.join(log_dir, logfile))
        elif 'stream' in logfile:
            pslstreaming.append(os.path.join(log_dir, logfile))

    push_file_path = os.path.join(log_dir, 'push.txt')
    rec_file_path = os.path.join(log_dir, 'rec.txt')

    merge_log(push_file_path, reversed(pslstreaming))
    merge_log(rec_file_path, reversed(psdemux))

    print('推流日志分析')
    for loginfo in split_file(push_file_path):
        find_part = {' drop seq':1, 'dup seq':1, 'reset ts':'整行', 'audio_compensate_on_recorded':'整行'}
        parse_log(loginfo, find_part)

    print('收流日志分析')
    for loginfo in split_file(rec_file_path, ') ffp_create'):
        parse_demux_log(loginfo)


