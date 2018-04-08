# -*- coding:utf-8 -*-
import os
import time
import sys
import cv2
import copy
from PyQt4 import QtCore
from PyQt4 import QtGui


class DemoShow(QtGui.QWidget):
    def __init__(self,parent=None):
        super(DemoShow,self).__init__(parent)
        self.setWindowTitle(u"人眼视线追踪标注工具")
        self.label_image = QtGui.QLabel()
        Layout_main = QtGui.QGridLayout(self)
        Layout_main.setSpacing(0)
        Layout_main.addWidget(self.label_image,0,0)
        self.device = cv2.VideoCapture(0)
        if self.device.isOpened is False:
            print("The Camera opened fail.")
            exit(-1)
        self.image_height = int(self.device.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
        self.image_width = int(self.device.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
        
        self.path = self.mkdir("save")
        self.frame = None
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.UpdataImage)
        
        self.timer.start(1000 / 30)
    
    


    def UpdataImage(self):
        ret, self.frame = self.device.read()
        self.label_image.setFixedSize(self.image_width,self.image_height)
        tmp_frame = copy.deepcopy(self.frame)
        self.GridLines(tmp_frame, 30)
        image= QtGui.QImage(tmp_frame, self.image_width, self.image_height,QtGui.QImage.Format_RGB888)
        self.label_image.setPixmap(QtGui.QPixmap.fromImage(image))
    
    def GridLines(self, frame, n):
        for i in range(0, self.image_width, int(n)):
            cv2.line(frame,(i, 0),(i, self.image_height),[255, 255, 255],1)
        for j in range(0, self.image_height, int(n)):
            cv2.line(frame,(0, j),(self.image_width, j),[255, 255, 255],1)
            
        
    
    def mousePressEvent(self,e):
         if self.timer.isActive():
            self.timer.stop()
            # TODO sava image
            image_path = self.path + '/' + self.getTimeStr() + "_x_" + str(e.x()) + "_y_" + str(e.y()) + ".jpg"
            self.save_image(image_path)
            # TODO save json
            self.timer.start(1000 / 30)
    
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
        cv2.imwrite(path_name,self.frame)
        

if __name__ == "__main__":
    print "hello again."
    app = QtGui.QApplication(sys.argv)
    obj = DemoShow()
    obj.show()
    app.exec_()
