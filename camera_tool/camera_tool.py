# -*- coding:utf-8 -*-
import os
import time
import sys
import cv2
import copy
from PyQt4 import QtCore
from PyQt4 import QtGui


class DemoShow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(DemoShow, self).__init__(parent)
        self.save_image_width = 1280
        self.save_image_height = 720
        self.show_image_width = 1920
        self.show_image_height = 1080
        self.frame_rate = 1000 / 30
        self.setWindowTitle(u"gaze tracking")
        self.label_image = QtGui.QLabel()
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
        tmp_frame = copy.deepcopy(self.frame)
        self.GridLines(tmp_frame, 6, 6)
        image= QtGui.QImage(tmp_frame, self.show_image_width, self.show_image_height, QtGui.QImage.Format_RGB888)
        self.label_image.setPixmap(QtGui.QPixmap.fromImage(image))

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
         if self.timer.isActive():
            self.timer.stop()
            image_path = self.path + '/' + self.getTimeStr() + "_x_" + str(e.x()) + "_y_" + str(e.y()) + ".jpg"
            self.save_image(image_path)
            self.timer.start(self.frame_rate)

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


if __name__ == "__main__":
    print "hello again."
    app = QtGui.QApplication(sys.argv)
    obj = DemoShow()
    obj.show()
    app.exec_()
