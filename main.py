#!/usr/bin/env python3
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QObject, Qt
import re
from secondwindow import secondwindow
import json
# import beep
# import shutil
# from collections import OrderedDict

form_class = uic.loadUiType("SVS_Viewer.ui")[0]

class Handler(QObject):
    def __init__(self, *args, **kwargs):
        super(Handler, self).__init__(*args, **kwargs)

class WebEnginePage(QWebEnginePage):
    point = []
    def __init__(self, *args, **kwargs):
        super(WebEnginePage, self).__init__(*args, **kwargs)

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceId):
        point = re.sub('|"|x|y|z|:|{|}', '', message)  #message 출력부 불필요한 문자열 제거
        point = point.split(',')
        self.point.clear()                              #리스트 초기화
        self.point.append(point)                        #출력되는 좌표값 리스트에 추가
        print(point)


class WindowClass(QMainWindow, form_class) :
    count_load_image = 0
    count_save_image = 0
    image_directory_path = "/Users/leehoseop/PycharmProjects/pano_dataset/sejong_gumgang_bridge/"
    file_name = "DJI_"
    ext = ".JPG"
    images_path = []
    background_picture = "/Users/leehoseop/PycharmProjects/SVS_Data_Creator/images/SVS_background2.png"
    widget_List = []
    url = QtCore.QUrl().fromLocalFile(os.path.split(os.path.abspath(__file__))[0] + r'/2.html')



    def initUI(self):
        self.show()


    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(1600,900)                        #창크기 고정
        self.setWindowTitle("Sky Viewer Solution Data Creator" + " Vesion Beta")
        self.setWindowIcon(QIcon("/Users/leehoseop/PycharmProjects/SVS_Data_Creator/images/icon.png"))
        self.image_Label.setStyleSheet("background-image : url(%s)" %self.background_picture)
        self.image_Label.setAutoFillBackground(True)

        # Set up backend communication via web channel
        self.handler = Handler()
        self.channel = QWebChannel()

        # Make the handler object available, naming it "backend"
        self.channel.registerObject("backend", self.handler)

        # Use a custom page that prints console messages to make debugging easier
        self.page = WebEnginePage()
        self.page.setWebChannel(self.channel)

        # Use a webengine view
        self.webview = QtWebEngineWidgets.QWebEngineView()
        self.webview.setPage(self.page)
        self.webview.setWindowFlags(Qt.WindowStaysOnTopHint)  #| Qt.FramelessWindowHint
        self.webview.setGeometry(15, 12, 1200, 675)
        self.webview.load(self.url)
        self.webview_layout.addWidget(self.webview)

        self.btn_loadFromFile.clicked.connect(self.File_Dialog)
        # self.pushbutton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_Delete_List.clicked.connect(self.Clear_File_List)
        self.listWidget.itemSelectionChanged.connect(self.File_list_itemSelectionChange)
        self.btn_svs.clicked.connect(self.loadImageFromFile)
        self.btn_Next.clicked.connect(self.NextImageFromFile)
        self.btn_Previous.clicked.connect(self.PreviousImageFromFile)
        self.btn_Image_Data_Generator.clicked.connect(self.Image_Labling)
        self.save_btn.clicked.connect(self.save_json_file)
        self.listWidget.itemClicked.connect(self.Clicked_list_item)

    def File_Dialog(self):
        exts = ('.jpg', 'png', '.JPG', '.PNG')

        images_path = QFileDialog.getExistingDirectory(self, 'Open File')
        self.images_path.append(images_path)
        file_list = os.listdir(images_path)
        print(images_path)
        file_list_py = [file for file in file_list if file.endswith(exts)]  ## 파일명 끝이 .jpg인 경우

        for file in sorted(file_list_py):
            self.listWidget.addItem(file)

    def Clear_File_List(self):
        self.listWidget.clear()         #파일리스트 삭제
        self.File_list_itemSelectionChange()
        self.file_path_label.setText("Undifined")
        self.images_path.clear()        #imagesPath 초기화
        self.qPixmapFileVar = QPixmap()
        self.qPixmapFileVar.load(str(self.background_picture))
        self.image_Label.setPixmap(self.qPixmapFileVar)


    def File_list_itemSelectionChange(self):
        item = self.listWidget.currentItem()
        path = self.images_path
        if (item == None):
            self.file_name_label.setText("Undifined")
        else:
            self.file_name_label.setText(item.text())
            self.file_path_label.setText(str(path[0]) + "/" + item.text())

    def loadImageFromFile(self) :
        clicked_points = WebEnginePage.point
        self.point_x_label.setText(clicked_points[0][0])
        self.point_y_label.setText(clicked_points[0][1])
        self.point_z_label.setText(clicked_points[0][2])

    #클릭한 아이템을 라벨에 보여주도록 함
    def Clicked_list_item(self, item):
        self.qPixmapFileVar = QPixmap()
        self.qPixmapFileVar.load(str(self.images_path[0]) + "/" + str(item.text()))
        self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(1200)
        self.image_Label.setPixmap(self.qPixmapFileVar)

    def NextImageFromFile(self) :
        item = self.listWidget.currentItem() #파일 이름
        value = self.listWidget.count() #리스트내 파일_전체 계수
        row = self.listWidget.currentRow() #현재 행
        self.row += row
        print(value)
        print(row)
        if self.row < value:
            self.listWidget.setCurrentRow(row+1)
            self.qPixmapFileVar = QPixmap()
            self.qPixmapFileVar.load(str(self.images_path[0]) + "/" + str(item.text()))
            self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(1200)
            self.image_Label.setPixmap(self.qPixmapFileVar)
        else :
            self.listWidget.setCurrentRow(0)

    def PreviousImageFromFile(self) :
        item = self.listWidget.currentItem()
        value = self.listWidget.count()
        row = self.listWidget.currentRow() #현재 행
        self.row -= row
        print(value)
        print(row)
        if row < value:
            self.listWidget.setCurrentRow(row-1)
            self.qPixmapFileVar = QPixmap()
            self.qPixmapFileVar.load(str(self.images_path[0]) + "/" + str(item.text()))
            self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(1200)
            self.image_Label.setPixmap(self.qPixmapFileVar)
        else :
            self.listWidget.setCurrentRow(0)

    def dragEnterEvent(self, event):            #드래그 앤 드랍을 구현
            if event.mimeData().hasUrls():
                event.accept()
            else:
                event.ignore()

    def dropEvent(self, event):
            files = [u.toLocalFile() for u in event.mimeData().urls()]
            for f in files:
                print(f)

    def Image_Labling(self):            #파일의 경로를 받아올 수 있도록 함
        global i
        global imag_path_dir
        global file_list
        imag_path_dir = QFileDialog.getExistingDirectory(self, 'Open File')
        file_list = os.listdir(imag_path_dir)
        file_list.sort()

        if not file_list:
            print("img_load_fail")
            sys.exit()

        i = 1
        while i < len(file_list):
            img_name = imag_path_dir + '/' + file_list[i]
            print(file_list[i])
            print(img_name)
            if i > len(file_list):
                msg = QMessageBox()
                msg.setWindowTitle('Message')
                msg.setText("No more Images, Press OK")
                break

            self.second = secondwindow()    #두번째창 생성
            self.second.exec()          #두번째창 닫을때까지 기다림
            # self.show()  # 두번쨰창 닫으면 다시 메인윈도우


    def save_json_file(self):
        global i
        global imag_path_dir
        global file_list

        clicked_points = WebEnginePage.point
        # image_name =
        selected_object = self.second.second_text_item
        object_number = self.second.second_text_index
        web_url = self.second.second_text_url
        web_vurl = self.second.second_text_vurl
        production = "skyviewersolution"

        # json파일에 정보를 넣어준다.
        # file_data = OrderedDict()
        file_data = {}
        file_data['point'] = []
        file_data['version'] = "1.0.0"
        file_data['filename'] = "%s" % file_list[i]
        file_data['production_company'] = "%s" %production
        file_data["point"].append({
            "item": selected_object,            #오브젝트
            "index": object_number,             #인덱싱넘버
            "url": web_url,                     #웹페이지 주소
            "vurl":web_vurl,                    #유투브 소스
            "point_x": clicked_points[0][0],    #x좌표
            "point_y": clicked_points[0][1],    #y좌표
            "point_z": clicked_points[0][2]     #z좌표
        })


        print(json.dumps(file_data, ensure_ascii=False, indent="\t"))

        with open(imag_path_dir + file_list[i] + '.json', 'w', encoding="utf-8") as make_file:
            json.dump(file_data, make_file, ensure_ascii=False, indent="\t")
        # shutil.copy(img_name, Labeled_data_path)
        i += 1
        #
        # def home(self):
        #     self.show()             #두번째창 닫으면 다시 첫 번째 창 보여 짐



    # def Clicked_list_item(self, current):
    #     currentItem = self.listWidget(current)
    #     print(currentItem)
    #     pixmap = currentItem.getPixmap()
    #     imagePath = currentItem.getImagePath()
    #     lblTxt = currentItem.getText()
    #
    #     self.qPixmapFileVar = QPixmap()
    #     self.qPixmapFileVar.load(self.images_path + currentItem)
    #     self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(1500)
    #     self.image_Label.setPixmap(self.qPixmapFileVar)

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
    # Make the handler object available, naming it "backend"
    myWindow.show()
    app.exec_()