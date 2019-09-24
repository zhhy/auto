# -*-coding:utf-8 -*-
import sys

log_info_base = {
    '初始化获取uid': 'PIiRoomPeer # new PIiRoomPeer',
    '开始加入房间': 'PIiRoomPeer # changeBehavior start',
    '收流url': 'PeerPlayer # setVideoPath',
    '收流视频成功': 'PIiRoomPeer # onReceivePeerVideoSuccess',
    '收流音频成功': 'PIiRoomPeer # onReceivePeerAudioSuccess',
    '离开房间': 'iRoomDemo # onLeftAlliRoom',
    '调用forceshutdown': '# PIiRoomPeer # forceShutdown',
    '打点码': 'whoop',
    '推流成功200ok': 'httpcode=200',
}

log_info_plus = {
    '发送长连接消息': 'PIiRoomPeer # onMessageOutput',
    '收到长连接消息': 'PIiRoomPeer # onMessageInput',
    '加入房间结束': 'PIiRoomPeer # changeBehavior finish',
    '发起RS请求': 'RoomServer # /rooms/memberships/change/ request',
    'RS请求响应': 'RoomServer # /rooms/memberships/change/ response',
    '创建播放器': 'PeerPlayer # new PeerPlayer',
    '开始移除播放器': 'PIiRoomPeer # removePlay start',
    '移除播放器结束': 'PIiRoomPeer # removePlay finish',
    '释放播放器窗口': 'UserWindowManager # releaseWindow',
    # 'ios开始停止摄像头': 'Transcoder -- AVCapture --  stop session',
    # 'ios结束停止摄像头': 'Transcoder -- AVCapture -- mAVCapSession release completed',
    '切后台': 'PIiRoomPeer # onPause',
    '切前台': 'PIiRoomPeer # onResume',
    '开始建立连接': 'HttpPostWriter -- SetupConn -- before connect',
    '发送http-request请求': 'HttpPostWriter -- Run -- send request',
    '推流结束': 'HttpPostWriter --  Stop -- close socket',
    '离开房间清理': 'PIiRoomPeer # cleanUp',
}


def parse_log(filepath_list, verbose=1):
    for file in filepath_list:
        with open(file, 'r') as f:
            logs = f.readlines()

        for line in logs:
            if verbose == 1:
                for key in log_info_base.keys():
                    if log_info_base[key] in line:
                        print(key)
                        print(line)
            else:
                for key in log_info_plus.keys():
                    if log_info_plus[key] in line:
                        print(key)
                        print(line)


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) > 1:
        filepath_list = sys.argv[1::]
    else:
        filepath_list = ['/Users/liminglei/Desktop/log/2/pslstreaming_log.txt']
    print(filepath_list)
    parse_log(filepath_list)