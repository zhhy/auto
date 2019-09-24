# -*- coding:utf-8 -*-

import os
import sys
import re
import matplotlib.pyplot as plt


def find_log(loginfo, findstr):
    res = []
    for log in loginfo:
        if findstr in log:
            res.append(log)
    return res


def parse_demux_log(loginfo, logfilepath):
    f = open(os.path.join(logfilepath, 'res_log.txt'), 'w')
    ffp = None
    res_infos = {}
    miaokai_infos = {}
    for log in loginfo:
        if re.findall('ffp.+ffp_create', log):
            f.write('##########')
            ffp = log.strip().split(' ')[7]
            f.write(log)
            res_infos[ffp] = []
            res_infos[ffp].append(log)
            miaokai_infos[ffp] = {}

        re_str = ['\) mode \d$', 'changemode \d cur \d', 'video_rendering_start$']
        for i in re_str:
            if re.findall(i, log):
                f.write(log)
                res_infos[ffp].append(log)

        find_str = ['psdemux_init opaque', ' ver[', 'is->name', 'filename ','Conn_Init dns time', 'OpenRequest Start',
                    'http_code[200]', 'devinfo', 'probe_trans video',
                    'first_audio_rendering_start', 'changemode return', f'{ffp} ijkmp_shutdown ', 'buffer error']
        for i in find_str:
            if i in log:
                f.write(log)
                res_infos[ffp].append(log)

        if 'time:' in log:
            info = log.strip().split(' ')
            miaokai_infos[ffp]['time']=int(info[info.index('time:')+1])
        if 'SDL_AoutPauseAudio' in log:
            miaokai_infos[ffp]['SDL_AoutPauseAudio'] = log
        if re.findall('audio_open \d+', log):
            miaokai_infos[ffp]['audio_open'] = log
    f.close()
    return res_infos, miaokai_infos


def print_total_result(res_infos, miaokai_infos, logfilepath):
    f = open(os.path.join(logfilepath, 'res_total.txt'), 'w')
    for key in res_infos.keys():
        f.write(f'{key} 整体测试情况：\n')
        err_list = []
        for info in res_infos[key]:
            if 'OpenRequest Start ' in info:
                request_start_index = res_infos[key].index(info)
                is_httpcode = 'http_code[200]' in res_infos[key][request_start_index + 1]
                if not is_httpcode:
                    f.write(f'收流失败，没有http_code[200],{info}\n')
                    err_list.append(is_httpcode)

        infos = '\n'.join(res_infos[key])
        # 判断是否下发视频、音频信息,是否有第一帧音频、视频数据
        search_infos ={'下发音视频数据':'probe_trans video', '第一帧视频数据':'video_rendering_start',
                       '第一帧音频数据': 'first_audio_rendering_start'}
        for search_key in search_infos.keys():
            sea_info = re.findall(search_infos[search_key], infos)
            if len(sea_info) == 0:
                f.write(f'收流失败，没有{sea_info}\n')
                err_list.append(sea_info)
        # 判断ijk是否关闭
        is_ijk_close = re.findall('ffp.+ ijkmp_shutdown', infos)[0].split()[0] == key
        if not is_ijk_close:
            f.write(f'{key} ijk 没有关闭\n')
            err_list.append(is_ijk_close)

        # 判断秒开时间
        miaokai_time = miaokai_infos[key]['time']
        if miaokai_time > 1000:
            f.write(f'秒开时间大于1s,为{miaokai_time}\n')
            f.write(miaokai_infos[key]['SDL_AoutPauseAudio'])
            f.write(miaokai_infos[key]['audio_open'])
            err_list.append(miaokai_infos[key]['time'])

        if len(err_list) == 0:
            f.write('测试正常\n')
    f.close()


def sum_array(array1, array2):
    res_array = []
    for i in range(len(array1)):
        res_array.append(array1[i]+array2[i])
    return res_array


def painting_miaokai(loginfo, logfilepath):
    prepare_list = locals()
    res = {'time:': [], 'init': [], 'pzb': [], 'conn': [], 'open': [],
           'probe': [], 'start': [], 'buffering': []}
    # print(re.findall('time: \d+','\n'.join(loginfo)))
    for log in loginfo:
        if 'time:' in log:
            info = log.strip().split(' ')
            for i in res.keys():
                if i == 'start':
                    result = int(info[info.index(i)+1]) + int(info[info.index(i)+2][:-1])
                    res[i].append(result)
                else:
                    result = info[info.index(i)+1]
                    if ',' in result:
                        result = result[0:-1]
                    res[i].append(int(result))

    x = list(range(1,len(res['pzb'])+1))
    x_1 = [ i+0.2 for i in x]
    y_list = list(res.keys())
    plt.bar(x, res['time:'], color='y', label='time', width=0.2)
    for i in range(len(x)):
        plt.text(x[i], res['time:'][i]/2, res['time:'][i], ha='center', va='baseline')
    list1 = ['init', 'pzb', 'conn', 'open', 'probe', 'start', 'buffering']
    color_list = ['red', 'green', 'lightgrey', 'orange', 'gray', 'cyan', 'pink']
    res_bottom = [0 for i in res['init']]
    for key in list1:
        index = list1.index(key)
        plt.bar(x_1, res[key], label=key, color=color_list[index], width=0.2, bottom=res_bottom)
        for i in range(len(x)):
            if res[key][i] == 0:
                continue
            plt.text(x_1[i], res_bottom[i] + res[key][i]/2, res[key][i], ha='center', va='baseline')
        # plt.text(x_1, res[key], res[key], ha='center', va='bottom')
        res_bottom = sum_array(res[key], res_bottom)
    plt.legend()
    plt.savefig(os.path.join(logfilepath, f'paint_miaokai.png'))
    plt.close('all')


def painting_video_freeze(loginfo, logfilepath):
    res = {}
    for log in loginfo:
        if 'bufstat' in log:
            info = log.strip().split(' ')
            bufstat_index = info.index('bufstat')
            if info[7] not in res.keys():
                res[info[7]] = {'pause': [], 'vq': [], 'aq': [], 'pq': [], 'sq': [],
                                'clk_v': [], 'clk_a': [], 'clk_vrenderd': [], 'clk_vdispalyed': [], 'clk_arender': []}
            res[info[7]]['pause'].append(int(re.findall('\d+', info[bufstat_index + 1])[0]))
            res[info[7]]['vq'].append(int(re.findall('\d+', info[bufstat_index + 2])[0]))
            res[info[7]]['aq'].append(int(re.findall('\d+', info[bufstat_index + 3])[0]))
            res[info[7]]['pq'].append(int(re.findall('\d+', info[bufstat_index + 4])[0]))
            res[info[7]]['sq'].append(int(re.findall('\d+', info[bufstat_index + 5])[0]))
            if 'nan' in info[bufstat_index + 6]:
                res[info[7]]['clk_v'].append(0)
            elif re.findall('\d+.\d+', info[bufstat_index + 6]):
                res[info[7]]['clk_v'].append(float(re.findall('\d+.\d+', info[bufstat_index + 6])[0]))
            if 'nan' in info[bufstat_index + 7]:
                res[info[7]]['clk_a'].append(0)
            elif re.findall('\d+.\d+', info[bufstat_index + 7]):
                res[info[7]]['clk_a'].append(float(re.findall('\d+.\d+', info[bufstat_index + 7])[0]))
            res[info[7]]['clk_vrenderd'].append(int(re.findall('\d+', info[bufstat_index + 8])[0]))
            res[info[7]]['clk_vdispalyed'].append(int(re.findall('\d+', info[bufstat_index + 9])[0]))
            res[info[7]]['clk_arender'].append(int(re.findall('\d+', info[bufstat_index + 10])[0]))

    for i in res:
        x = list(range(len(res[i]['pause'])))
        y_list = list(res[i].keys())
        for key in y_list:
            plt.figure(i + key)
            plt.xlim(0, len(x))
            plt.plot(x, res[i][key], 'o-', color='red', label=key, markersize=1, linewidth=0.5)
            plt.legend()
            plt.savefig(os.path.join(logfilepath, f'paint_video_freeze_{i}_{key}.png'))
            plt.close()


def painting_delay_infos(loginfo, logfilepath):
    res = {}
    for log in loginfo:
        if 'pstream(0) delay' in log:
            info = log.strip().split(' ')
            if info[7] not in res.keys():
                res[info[7]] = {'delay': [], 'bps': [], 'freeze': [], 'reada': [], 'pause': [], 'filter':[]}
            res[info[7]]['delay'].append(int(re.findall('\d+', info[info.index('delay') + 1])[0]))
            res[info[7]]['bps'].append(int(re.findall('\d+', info[info.index('bps') + 1])[0]))
            res[info[7]]['freeze'].append(int(re.findall('\d+', info[info.index('freeze') + 1])[0]))
            res[info[7]]['reada'].append(int(re.findall('\d+', info[info.index('reada') + 1])[0]))
            res[info[7]]['pause'].append(int(re.findall('\d+', info[info.index('pause') + 1])[0]))
            res[info[7]]['filter'].append(int(re.findall('\d+', info[info.index('filter') + 1])[0]))
    # painting
    for i in res:
        x = list(range(len(res[i]['delay'])))
        y_list = list(res[i].keys())
        plt.figure(i)
        for key in y_list:
            plt.subplot(321+y_list.index(key))
            plt.xlim(0, len(x))
            plt.plot(x, res[i][key], 'go-', label=key, markersize=1, linewidth=0.5)
            plt.legend()
        plt.savefig(os.path.join(logfilepath, f'paint_delayinfo_{i}.png'))
        plt.close()


if __name__ == '__main__':
    # python3 A50_push_rec.py /Users/liminglei/Desktop/log/2018-12-02_19-41-56__iLiveA50/pslstreaming_log.txt False
    # logfile = sys.argv[1]
    logfile = '/Users/liminglei/Desktop/log/vivo/psdemux_log.txt'
    if len(sys.argv) > 1:
        logfile = sys.argv[1]
    logfilepath = os.path.dirname(logfile)
    streamfile = []
    demuxfile = []

    for f in os.listdir(logfilepath):
        if 'pslstreaming_log' in f:
            streamfile.append(f)
        elif 'psdemux_log' in f:
            demuxfile.append(f)
    for f in demuxfile:
        path = os.path.join(logfilepath, f)
        loginfo = []
        with open(path, 'r') as f:
            for line in f:
                loginfo.append(line)
        res_infos, miaokai_infos = parse_demux_log(loginfo, logfilepath)
        print_total_result(res_infos, miaokai_infos, logfilepath)
        painting_miaokai(loginfo, logfilepath)
        painting_video_freeze(loginfo, logfilepath)
        painting_delay_infos(loginfo, logfilepath)