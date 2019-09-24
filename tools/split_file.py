# -*- coding:utf-8 -*-
from datetime import datetime


def splitfile():
    source_file = '/Users/liminglei/Desktop/log/meizu.txt'
    target_dir = '/Users/liminglei/Desktop/log/'

    # 计数器
    flag = 0

    # 文件名
    name = 1

    # 存放数据
    dataList = []

    print("开始。。。。。")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    with open(source_file, 'rb') as f_source:
        for line in f_source:
            flag += 1
            dataList.append(line)
            if flag == 2000000:
                with open(target_dir + "split_list_" + str(name) + ".txt", 'wb+') as f_target:
                    for data in dataList:
                        f_target.write(data)
                name += 1
                flag = 0
                dataList = []

    # 处理最后一批行数少于200万行的
    with open(target_dir + "split_list_" + str(name) + ".txt", 'wb+') as f_target:
        for data in dataList:
            f_target.write(data)

    print("完成。。。。。")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == "__main__":
    splitfile()

