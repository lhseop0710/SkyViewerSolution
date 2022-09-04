#!/usr/bin/env python3
import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5 import QtCore, QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QObject, Qt
from panoramic360 import panoramic360
from secondwindow import secondwindow
import json
import cv2
import beep
import shutil
from collections import OrderedDict

form_class = uic.loadUiType("SVS_Viewer.ui")[0]

class Handler(QObject):
    def __init__(self, *args, **kwargs):
        super(Handler, self).__init__(*args, **kwargs)

class WebEnginePage(QWebEnginePage):
    def __init__(self, *args, **kwargs):
        super(WebEnginePage, self).__init__(*args, **kwargs)

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceId):
        l = message.split(",")
        self.obj = l
        print ('JS: %s line %d: %s' % (sourceId, lineNumber, message))
        print("WebEnginePage Console: %s" %message)
        return message

class WindowClass(QMainWindow, form_class) :
    count_load_image = 0
    count_save_image = 0
    directory_path = "/Users/leehoseop/Desktop/img_data/360_image/"
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

        # self.setCentralWidget(self.central_widget)
        # self.vertical.addWidget(QTextEdit())
        # self.vertical.addWidget(QTextEdit())




        ##
        # self.widget_pano = QtWidgets.QWidget(self.centralwidget)
        # self.widget_List.append(self.widget_pano)
        # self.widget_pano.setObjectName("widget_youtube")

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
        # self.setCentralWidget(self.webview)
        self.webview.setWindowFlags(Qt.WindowStaysOnTopHint)  #| Qt.FramelessWindowHint
        self.webview.setGeometry(15, 12, 1200, 675)
        self.webview.setFixedSize(1200, 675)
        self.webview.load(self.url)
        self.webview_layout.addWidget(self.webview)
        # self.horizontal.addLayout(self.vertical)
        # self.webview.show()
        ##

        self.btn_loadFromFile.clicked.connect(self.File_Dialog)
        # self.pushbutton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_Delete_List.clicked.connect(self.Clear_File_List)
        self.listWidget.itemSelectionChanged.connect(self.File_list_itemSelectionChange)
        self.btn_SVS.clicked.connect(self.loadImageFromFile)
        self.btn_Next.clicked.connect(self.NextImageFromFile)
        self.btn_Previous.clicked.connect(self.PreviousImageFromFile)
        self.btn_Image_Data_Generator.clicked.connect(self.Image_Labling)  #OpenCV창으로 넘어가도록 함
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
        # self.hide()             #메인윈도우 숨김
        self.second = panoramic360(self.directory_path+self.file_name+str(self.count_load_image).zfill(4)+self.ext)  # 두번째창 생성
        self.second.exec()  # 두번째창 닫을때까지 기다림
        self.show()

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


        # self.count_load_image -= 1
        # #QPixmap 객체 생성 후 이미지 파일을 이용하여 QPixmap에 사진 데이터 Load하고, Label을 이용하여 화면에 표시
        # self.qPixmapFileVar = QPixmap()
        # self.qPixmapFileVar.load(self.directory_path+self.file_name+str(self.count_load_image).zfill(4)+self.ext)
        # self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(1200)
        # self.image_Label.setPixmap(self.qPixmapFileVar)


    def dragEnterEvent(self, event):            #드래그 앤 드랍을 구현
            if event.mimeData().hasUrls():
                event.accept()
            else:
                event.ignore()

    def dropEvent(self, event):
            files = [u.toLocalFile() for u in event.mimeData().urls()]
            for f in files:
                print(f)

    clicked_points = []
    blue, red = (255, 0, 0), (0, 0, 255)  # 색상 값

    def onMouse(self, event, x, y, flags, param):  # 마우스 이벤트 핸들 함수  ---①
        global isDragging, x0, y0, img  # 전역변수 참조
        global x_point, y_point, w_point, h_point
        global img_draw
        if event == cv2.EVENT_LBUTTONDOWN:  # 왼쪽 마우스 버튼 다운, 드래그 시작 ---②
            self.clicked_points.append((x,y))
        elif event == cv2.EVENT_LBUTTONUP:  # 왼쪽 마우스 버튼 업 ---④
            img_draw = img.copy()  # 선택 영역에 사각형 그림을 표시할 이미지 복제
            for point in self.clicked_points:
            # 선택 영역에 빨간 사각형 표시
                cv2.circle(img_draw, (point[0], point[1]), 2, self.red, thickness = -1)
                cv2.imshow('img_draw', img_draw)  # 빨간 사각형 그려진 이미지 화면 출력
                # if self.w > 0 and self.h > 0:  # 폭과 높이가 양수이면 드래그 방향이 옳음 ---⑤
                #     img_draw = img.copy()  # 선택 영역에 사각형 그림을 표시할 이미지 복제
                #     # 선택 영역에 빨간 사각형 표시
                #     cv2.circle(img_draw, (self.clicked_points[0], 3, self.red, 2)
                #     cv2.imshow('img_draw', img_draw)  # 빨간 사각형 그려진 이미지 화면 출력
                # else:
                #     #cv2.imshow('img', img)  # 드래그 방향이 잘못된 경우 사각형 그림ㅇㅣ 없는 원본 이미지 출력
                #     print("좌측 상단에서 우측 하단으로 영역을 드래그 하세요.")
        # elif event == cv2.EVENT_RBUTTONDOWN:        #cv2.EVENT_RBUTTONDBCKL은 macOS Montrey, openCV4.5 python3.7에서 지원되지 않음
        #     print("destroyWindow")
        #     cv2.destroyWindow('img_draw')

    def Image_Labling(self):            #파일의 경로를 받아올 수 있도록 함
        global img  #전역변수 참조
        global clicked_points #전역변수 참조
        global img_draw
        Labeled_data_path = self.directory_path #라벨링한 이미지의 경로를 지정
        path_dir = QFileDialog.getExistingDirectory(self, 'Open File')
        file_list = os.listdir(path_dir)
        file_list.sort()
        # 맥OS에서는 list를 자동적으로 정렬해주지 않으므로 list.sort()
        # 기본적으로 리스트를 오름차순으로 정렬 해줌
        #fname = QFileDialog.getOpenFileName(self)
        #path = QFileDialog.getExistingDirectory(self, 'Open File') + '/'   #경로는 리스트로 출력됨 사용할때는 반드시 뒤에 []에 해당 인덱스를 붙여줘야함
        isDragging = False  # 마우스 드래그 상태 저장
        x0, y0, w, h = -1, -1, -1, -1  # 영역 선택 좌표 저장
        blue, red = (255, 0, 0), (0, 0, 255)  # 색상 값

        if not file_list:
            print("img_load_fail")
            sys.exit()

        i = 1
        while i < len(file_list):
            img_name = path_dir + "/" + file_list[i]
            print(path_dir)
            print(file_list[i])
            print(img_name)
            img = cv2.imread(img_name, cv2.IMREAD_COLOR)
            cv2.imshow('img_data', img)
            key = cv2.waitKey(0)
            if i > len(file_list):
                msg = QMessageBox()
                msg.setWindowTitle('Message')
                msg.setText("No more Images, Press OK")
                break

            if key == 110:  # 'n'을 누르면 다음사진
                print('Next_img:   ', key)

                i += 1
                cv2.imshow("index number" + str(i) + self.ext, img)
                cv2.destroyWindow("index number" + str(i-1)  + self.ext)

            elif key == 98:  # 'b'를 누르면 이전사진
                print('Previous_img:   ', key)
                i -= 1
                cv2.imshow("index number" + str(i) + self.ext, img)
                cv2.destroyWindow("index number" + str(i+1)  + self.ext)

            elif key ==  32:  # 'spacebar'를 누르면 라벨링
                print('Mouse_Event')
                cv2.imshow('%s' %(str(i)), img)
                cv2.setMouseCallback('img_draw', self.onMouse)  # 마우스 이벤트 소환 ---⑧

                self.hide()         #메인윈도우 숨김
                self.second = secondwindow()    #두번째창 생성
                self.second.exec()          #두번째창 닫을때까지 기다림
                # self.show()  # 두번쨰창 닫으면 다시 메인윈도우

                query = self.second.second_text
                selected_object = query
                object_number = None
                production = None

                if selected_object == "information center":     #안내소
                    object_number = "1"
                elif selected_object == "ticket box":           #매표소
                    object_number = "2"
                elif selected_object == "information board":    #안내판
                    object_number = "3"
                elif selected_object == "life saving goods":    #인명구호용품
                    object_number = "4"
                elif selected_object == "defibrillators":       #심장제세동기
                    object_number = "5"
                elif selected_object == "toilet":               #화장실
                    object_number = "6"
                elif selected_object == "tourist attraction":   #관광명소
                    object_number = "7"
                elif selected_object == "building":             #건물
                    object_number = "8"
                elif selected_object == "store":               #상점
                    object_number = "9"

                #json파일에 정보를 넣어준다.
                file_data = OrderedDict()
                file_data["version"] = "1.0.0"
                file_data["filename"] = "%s" %selected_object
                file_data["shapes"] = {'label': '%s' % str(query),
                                       'production_company': "%s" %production,
                                       'points': [clicked_points]}
                file_data["number"] = "%s" %object_number

                print(json.dumps(file_data, ensure_ascii=False, indent="\t"))

            elif key == 109: # 'm'을 누르면 json파일 저장 및 이미지 복사
                with open(self.directory_path + file_list[i] + '.json', 'w', encoding="utf-8") as make_file:
                    json.dump(file_data, make_file, ensure_ascii=False, indent="\t")
                shutil.copy(self.file_name, self.directory_path)
                beep.beep(sound=1)
                cv2.waitKey()
                cv2.destroyWindow('img_draw')

            elif key == 27:  # 'ESC'를 누르면 종료
                print('Exit_image_viewer')
                cv2.destroyAllWindows()
                self.show()             #두번째창 닫으면 다시 첫 번째 창 보여 짐
                break



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