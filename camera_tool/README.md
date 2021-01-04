# 人眼视线追踪标注工具

应用PyQt4模块, 编写可视化窗口工具用以辅助算法人员进行标注.<p>

## 1. 环境配置
```
sudo apt-get install libqt4-dev
sudo apt-get install python-qt4
sudo pip install xlib
sudo pip install PyAutoGUI
```


## 2. 思路说明
1. 使用cv2模块`cap = cv2.VideoCapture(0)`打开PC摄像头, 并`ret, frame = cap.read()`读取数据.
2. 使用Qt.Core.QTimer()进行不断触发`cap.read()`来更新显示, 以此达到更新界面的目的.
3. 重定义鼠标点击事件`mousePressEvent`, 每点击一次,停止更新界面并将frame数据保存为图片. 图片名称为 "time_x_y.jpg". 名称中含有鼠标点击瞬间的坐标.
4. 最后在Python脚本所在目录下会有一个名为"save"的文件夹用以保存图片.最后算法人员取得含有(x,y)数据的图片用以训练.
