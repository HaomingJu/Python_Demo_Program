# -*- coding:utf-8 -*-
import os
import time
import sys
import cv2
import copy
import threading
# import pyautogui as pag

from PyQt4 import QtCore
from PyQt4 import QtGui

kframe = None

class VideoRecorderThread(threading.Thread):
    def __init__(self, time):
        threading.Thread.__init__(self)
        self.can_next = False
        self.lock = threading.Lock()

    def run(self):
        self.can_next = True
        # TODO 编码器初始化
        while True:
            self.lock.acquire()
            if self.can_next is False:
                self.lock.release()
                break
            self.lock.release()
            print "write...."
        print "stop..."


    def stop(self):
        self.lock.acquire()
        self.can_next = False
        self.lock.release()





class DemoShow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(DemoShow, self).__init__(parent)
        self.save_image_width = 1280
        self.save_image_height = 720
        self.show_image_width = 1920
        self.show_image_height = 1080
        self.frame_rate = 1000 / 30
        self.col_line_num = 6
        self.row_line_num = 6
        self.recorde_video = False
        self.cap = None
        self.setWindowTitle(u"gaze tracking")
        self.label_image = QtGui.QLabel()
        self.label_image.setCursor(QtCore.Qt.CrossCursor)
        Layout_main = QtGui.QGridLayout(self)
        Layout_main.setSpacing(0)
        Layout_main.addWidget(self.label_image, 0, 0)
        self.device = cv2.VideoCapture(0)
        self.device.set(cv2.CAP_PROP_FRAME_WIDTH,self.show_image_width)
        self.device.set(cv2.CAP_PROP_FRAME_HEIGHT,self.show_image_height)
        if self.device.isOpened is False:
          print("The Camera opened fail.")
          exit(-1)
        self.image_height = int(self.device.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.image_width = int(self.device.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.path = self.mkdir("save")
        self.frame = None
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.UpdataImage)

        self.timer.start(self.frame_rate)     # 控制帧率
        self.resize(self.show_image_width, self.show_image_height)

    def UpdataImage(self):
        ret, self.frame = self.device.read()
        self.frame = cv2.resize(self.frame, (self.show_image_width, self.show_image_height))
        save_frame = cv2.resize(self.frame, (self.save_image_width, self.save_image_height))

        tmp_frame = copy.deepcopy(self.frame)
        self.GridLines(tmp_frame,self.col_line_num, self.row_line_num)
        image= QtGui.QImage(tmp_frame, self.show_image_width, self.show_image_height, QtGui.QImage.Format_RGB888)
        self.label_image.setPixmap(QtGui.QPixmap.fromImage(image))

        if self.recorde_video is True:
            if self.cap is None:
                mp4_path_name = self.path + '/' + self.getTimeStr() + ".avi"
                print mp4_path_name
                self.cap = cv2.VideoWriter(mp4_path_name, cv2.VideoWriter_fourcc('I', '4', '2', '0'), 25, (self.save_image_width, self.save_image_height))
            else:
                self.cap.write(save_frame)
        else:
            if self.cap is None:
                self.cap.release()
                self.cap = None




    def GridLines(self, frame, n, m ):
        col_num = self.show_image_width / n
        row_num = self.show_image_height / m
        for i in range(0, self.show_image_width + 1, col_num):
            cv2.line(frame,(i, 0),(i, self.show_image_height),[255, 255, 255],1)
        for j in range(0, self.show_image_height + 1, row_num):
            cv2.line(frame,(0, j),(self.show_image_width, j),[255, 255, 255],1)
        for m in range(0, self.show_image_width + 1, col_num):
            for n in range(0, self.show_image_height + 1, row_num):
                cv2.circle(frame,(m,n),5,(255,0,0),3)

    def keyPressEvent(self, e):
        if e.key() ==  QtCore.Qt.Key_D:
            print ('delete the previous image: ')
            print (self.path)
            print (os.listdir(self.path)[-1])
            os.remove(self.path + '\\' + os.listdir(self.path)[-1]) 

    def mousePressEvent(self,e):
        if e.button() == QtCore.Qt.LeftButton:
            if self.timer.isActive():
                self.timer.stop()
                image_path = self.path + '/' + self.getTimeStr() + "_x_" + str(e.x()) + "_y_" + str(e.y()) + ".jpg"
                self.save_image(image_path)
                self.timer.start(self.frame_rate)
        elif e.button() == QtCore.Qt.RightButton:
            self.recorde_video = True
        else:
            pass

    def mouseReleaseEvent(self,e):
        if e.button() == QtCore.Qt.RightButton:
            self.recorde_video = False
            pass

    # def mouseMoveEvent(self, e):
        # print "123132"

    def mkdir(self, path_):
        [scriptDir,scriptName]  = os.path.split(os.path.abspath(__file__))
        path = scriptDir + "/" + str(path_)
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    def getTimeStr(self):
        timestamp = time.time()
        nowTime = (int(round(timestamp * 1000)))
        return str(nowTime)

    def save_image(self, path_name):
        self.frame= cv2.resize(self.frame, (self.save_image_width, self.save_image_height))
        cv2.imwrite(path_name,self.frame)


    # 事件过滤
    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseMove:
             if event.buttons() == QtCore.Qt.NoButton:
                 pos = event.pos()
                 gpos = event.globalPos()
                 # print self.label_image.mapFromGlobal(QtCore.QPoint(gpos.x(), gpos.y()))
                 # print "%d %d %d %d" % (pos.x(), pos.y(), gpos.x(), gpos.y())
                 if pos.x() < 100 and pos.y() < 100:
                     self.label_image.setToolTip(u"狗算法,CNM要求真多")
                 else:
                     self.label_image.setToolTip(u"")

             else:
                 pass
        return QtGui.QMainWindow.eventFilter(self, source, event)


if __name__ == "__main__":
    print "hello again."
    app = QtGui.QApplication(sys.argv)
    obj = DemoShow()
    obj.show()
    app.installEventFilter(obj)
    app.exec_()
