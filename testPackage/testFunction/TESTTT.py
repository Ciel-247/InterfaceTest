# _*_ coding:utf-8 _*_
__author__ = 'gjj14453'
import logging
import os
import common.myDate as myDate

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p))
pics = []
picpath = []


##################################
#  日志
# 0: debug
# 1：info
# 2：warning
# -1：error
###################################
def mylogger(msg, flag=1):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='mylog.log',
                        filemode='w')


    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    if flag == 0:
        logging.debug(msg)
    elif flag == 1:
        logging.info(msg)
    elif flag == 2:
        logging.warning(msg)
        screenshot()
    elif flag == -1:
        logging.error(msg)
        screenshot()
    logging.getLogger('').removeHandler(console)


#  截屏
def screenshot():
    dirname = PATH('D:\\MyConfiguration\\gjj14453\\PycharmProjects\\untitled\\list_out' + "/screenshot")


os.popen("adb wait-for-device")
os.popen("adb shell screencap -p /data/local/tmp/tmp.png")
if not os.path.isdir(dirname):
    os.makedirs(dirname)
pic = myDate.timestampname() + ".png"
path = dirname + "/" + pic
os.popen("adb pull /data/local/tmp/tmp.png " + PATH(path))
os.popen("adb shell rm /data/local/tmp/tmp.png")
mylogger("截图为：" + pic)
pics.append(pic)
picpath.append(path)


def creathtml(path, pic):
    html = ''


if range(len(path)) > 0:
    for i in range(len(path)):
        if i == 0:
            html = '<a href=' + path[i] + ' target="_blank">' + pic[i] + '</a>'
else:
    html = html + '<br /><a href=' + path[i] + ' target="_blank">' + pic[i] + '</a>'
else:
html = ''
htmls = 'htmlbegin<td>' + html + '</td>htmlend'
