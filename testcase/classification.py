import testcase.QSstarlightTestCase as QSStarlight
import testcase.iRoomTestCase as iRoom
import testcase.QSA50TestCase as QSA50
import testcase.QSDokiTestCase as QSDoki

## 加入离开房间
def joinandleaveroom(driver,roomid,devicenameinfo,package):
    if package == 'QSStarlight':
        QSStarlight.joinandleaveroom(driver,roomid,devicenameinfo,package)
    elif package == 'iRoom':
        iRoom.joinandleaveroom(driver,roomid,devicenameinfo,package)
    elif package == 'QSA50':
        QSA50.joinandleaveroom(driver,roomid,devicenameinfo,package)
    elif package == 'QSDoki':
        QSDoki.joinandleaveroom(driver,roomid,devicenameinfo,package)



def backapp(driver,roomid,devicenameinfo,package):
    if package == 'QSStarlight':
        QSStarlight.backapp(driver,roomid,devicenameinfo,package)
    elif package == 'iRoom':
        iRoom.backapp(driver,roomid,devicenameinfo,package)
    elif package == 'QSDoki':
        QSDoki.backapp(driver,roomid,devicenameinfo,package)

def lockscreen(driver,roomid,devicenameinfo,package):
    if package == 'QSStarlight':
        QSStarlight.lockscreen(driver,roomid,devicenameinfo,package)
    elif package == 'iRoom':
        iRoom.lockscreen(driver,roomid,devicenameinfo,package)
    elif package == 'QSA50':
        QSA50.lockscreen(driver,roomid,devicenameinfo,package)
    elif package == 'QSDoki':
        QSDoki.lockscreen(driver,roomid,devicenameinfo,package)

def changerole(driver,roomid,devicenameinfo,package):
    if package == 'iRoom':
        iRoom.changerole(driver,roomid,devicenameinfo,package)


def recordhoinandleave(driver,roomid,devicenameinfo,package):
    if package == 'iRoom':
        iRoom.recordhoinandleave(driver,roomid,devicenameinfo,package)

def creatroom(driver,devicenameinfo,package):
    if package == 'iRoom':
        iRoom.creatroom(driver,devicenameinfo,package)
