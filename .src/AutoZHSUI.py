# -*- coding: utf-8 -*-
from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QIcon
import AutoLesson
from threading import Thread
import sys, os
def resource_path(relative_path):
    '''返回资源绝对路径。'''
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller会创建临时文件夹temp
        # 并把路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)

class ZHSUI():
    def __init__(self):
        file = QFile(resource_path('ZHSUI.ui'))
        self.window = QUiLoader().load(file)
        self.window.pushButton.clicked.connect(self.threadStart)

    def start(self):
        user = self.window.userEdit.text()
        passwd = self.window.passwdEdit.text()
        class_name = self.window.classEdit.text()
        Auto = AutoLesson.AutoLessons()
        Auto.auto(user, passwd, class_name)

    def threadStart(self):
        t = Thread(target=self.start)
        t.start()
app = QApplication([])
#加载Icon
app.setWindowIcon(QIcon(resource_path('logo.png')))
UI = ZHSUI()
UI.window.show()
app.exec_()

'''
cmd打包代码：pyinstaller -w -F AutoZHSUI.py -p AutoLesson.py -p CrackSlider.py --add-data="ZHSUI.ui;." --add-data="logo.png;." -i "logo.ico" --upx-dir="D:\CodeSoftware\GUI\upx-3.96-win64"
'''