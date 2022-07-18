import sys
import os
import urllib.request
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from panoramic360 import panoramic360
import json

form_class = uic.loadUiType("SVS_Viewer.ui")[0]

class WindowClass(QMainWindow, form_class) :
    count_load_image = 131
    count_save_image = 0
    directory_path = "/Users/leehoseop/Desktop/img_data/360_image/"
    file_name = "DJI_"
    ext = ".JPG"

    def initUI(self):
        self.setWindowTitle("Sky Viewer Solution Data Creator" + " Vesion Beta")
        self.show()

    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(1920,1080)                        #창크기 고정

        # self.setCursor(QtCore.Qt.CrossCursor)
        # # keep a reference of the original image
        # self.source = QPixmap(self.directory_path + self.file_name + str(self.count_load_image).zfill(4) + self.ext)
        # self.pano = QPixmap(self.source.width() * 3, self.source.height())
        # self.center = self.pano.rect().center()
        # # use a QPointF for precision
        # self.delta = QtCore.QPointF()
        # self.deltaTimer = QtCore.QTimer(interval=25, timeout=self.moveCenter)
        # self.sourceRect = QtCore.QRect()
        # # create a pixmap with three copies of the source;
        # # this could be avoided by smart repainting and translation of the source
        # # but since paintEvent automatically clips the painting, it should be
        # # faster then computing the new rectangle each paint cycle, at the cost
        # # of a few megabytes of memory.
        # self.setMaximumSize(self.source.size())
        # qp = QtGui.QPainter(self.pano)
        # qp.drawPixmap(0, 0, self.source)
        # qp.drawPixmap(self.source.width(), 0, self.source)
        # qp.drawPixmap(self.source.width() * 2, 0, self.source)
        # qp.end()

        self.btn_loadFromFile.clicked.connect(self.File_Dialog)
        self.btn_Delete_List.clicked.connect(self.Clear_File_List)
        self.listWidget.itemSelectionChanged.connect(self.File_list_itemSelectionChange)
        self.btn_SVS.clicked.connect(self.loadImageFromFile)
        self.btn_Forward.clicked.connect(self.ForwardImageFromFile)
        self.btn_Backward.clicked.connect(self.BackwardImageFromFile)
        self.btn_Left.clicked.connect(self.LeftImageFromFile)
        self.btn_Right.clicked.connect(self.RightImageFromFile)



    def File_Dialog(self):
        path = QFileDialog.getExistingDirectory(self, 'Open File')
        file_list = os.listdir(path)
        file_list_py = [file for file in file_list if file.endswith('.jpg')]  ## 파일명 끝이 .jpg인 경우

        for file in sorted(file_list_py):
            self.listWidget.addItem(file)

    def Clear_File_List(self):
        self.listWidget.clear()
        self.File_list_itemSelectionChange()


    def File_list_itemSelectionChange(self):
        item = self.listWidget.currentItem()
        if (item == None):
            self.file_name_label.setText("Undifined")
        else:
            self.file_name_label.setText(item.text())

    def loadImageFromFile(self) :
        #QPixmap 객체 생성 후 이미지 파일을 이용하여 QPixmap에 사진 데이터 Load하고, Label을 이용하여 화면에 표시
        # self.qPixmapFileVar = QPixmap()
        # self.qPixmapFileVar.load(self.directory_path+self.file_name+str(self.count_load_image).zfill(4)+self.ext)
        # self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(1500)
        # self.image_Label.setPixmap(self.qPixmapFileVar)
        self.hide()
        self.panoramic360 = panoramic360(self.directory_path+self.file_name+str(self.count_load_image).zfill(4)+self.ext)  # 두번째창 생성
        self.panoramic360.exec()  # 두번째창 닫을때까지 기다림

    def ForwardImageFromFile(self) :
        self.count_load_image += 1
        #QPixmap 객체 생성 후 이미지 파일을 이용하여 QPixmap에 사진 데이터 Load하고, Label을 이용하여 화면에 표시
        self.qPixmapFileVar = QPixmap()
        self.qPixmapFileVar.load(self.directory_path+self.file_name+str(self.count_load_image).zfill(4)+self.ext)
        self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(1500)
        self.image_Label.setPixmap(self.qPixmapFileVar)
    def BackwardImageFromFile(self) :
        self.count_load_image -= 1
        #QPixmap 객체 생성 후 이미지 파일을 이용하여 QPixmap에 사진 데이터 Load하고, Label을 이용하여 화면에 표시
        self.qPixmapFileVar = QPixmap()
        self.qPixmapFileVar.load(self.directory_path+self.file_name+str(self.count_load_image).zfill(4)+self.ext)
        self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(1500)
        self.image_Label.setPixmap(self.qPixmapFileVar)
    def LeftImageFromFile(self) :
        #QPixmap 객체 생성 후 이미지 파일을 이용하여 QPixmap에 사진 데이터 Load하고, Label을 이용하여 화면에 표시
        self.qPixmapFileVar = QPixmap()
        self.qPixmapFileVar.load(self.directory_path+self.file_name+str(self.count_load_image).zfill(4)+self.ext)
        self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(1500)
        self.image_Label.setPixmap(self.qPixmapFileVar)
    def RightImageFromFile(self) :
        #QPixmap 객체 생성 후 이미지 파일을 이용하여 QPixmap에 사진 데이터 Load하고, Label을 이용하여 화면에 표시
        self.qPixmapFileVar = QPixmap()
        self.qPixmapFileVar.load(self.directory_path+self.file_name+str(self.count_load_image).zfill(4)+self.ext)
        self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(1500)
        self.image_Label.setPixmap(self.qPixmapFileVar)

    # class Panoramic(QtWidgets.QWidget):
    #     def __init__(self, imagePath):
    #         QtWidgets.QWidget.__init__(self)
    #         self.setCursor(QtCore.Qt.CrossCursor)
    #         # keep a reference of the original image
    #         self.source = QtGui.QPixmap(imagePath)
    #         self.pano = QtGui.QPixmap(self.source.width() * 3, self.source.height())
    #         self.center = self.pano.rect().center()
    #         # use a QPointF for precision
    #         self.delta = QtCore.QPointF()
    #         self.deltaTimer = QtCore.QTimer(interval=25, timeout=self.moveCenter)
    #         self.sourceRect = QtCore.QRect()
    #         # create a pixmap with three copies of the source;
    #         # this could be avoided by smart repainting and translation of the source
    #         # but since paintEvent automatically clips the painting, it should be
    #         # faster then computing the new rectangle each paint cycle, at the cost
    #         # of a few megabytes of memory.
    #         self.setMaximumSize(self.source.size())
    #         qp = QtGui.QPainter(self.pano)
    #         qp.drawPixmap(0, 0, self.source)
    #         qp.drawPixmap(self.source.width(), 0, self.source)
    #         qp.drawPixmap(self.source.width() * 2, 0, self.source)
    #         qp.end()

    # def loadImageFromWeb(self) :
    #
    #     #Web에서 Image 정보 로드
    #     urlString = "https://avatars1.githubusercontent.com/u/44885477?s=460&v=4"
    #     imageFromWeb = urllib.request.urlopen(urlString).read()
    #
    #     #웹에서 Load한 Image를 이용하여 QPixmap에 사진데이터를 Load하고, Label을 이용하여 화면에 표시
    #     self.qPixmapWebVar = QPixmap()
    #     self.qPixmapWebVar.loadFromData(imageFromWeb)
    #     self.qPixmapWebVar = self.qPixmapWebVar.scaledToWidth(600)
    #     self.lbl_picture.setPixmap(self.qPixmapWebVar)
    #
    # def saveImageFromWeb(self) :
    #     #Label에서 표시하고 있는 사진 데이터를 QPixmap객체의 형태로 반환받은 후, save함수를 이용해 사진 저장
    #     self.qPixmapSaveVar = self.lbl_picture.pixmap()
    #     self.qPixmapSaveVar.save("SavedImage.jpg")

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()