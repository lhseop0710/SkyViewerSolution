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
import re
from secondwindow import secondwindow
import json
from PIL import Image
from PIL.ExifTags import TAGS
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
    exts = ('.jpg', 'png', '.JPG', '.PNG', 'jpeg', 'JPEG')
    background_picture = "/Users/leehoseop/PycharmProjects/SVS_Data_Creator/images/icon.png"
    url = QtCore.QUrl().fromLocalFile(os.path.split(os.path.abspath(__file__))[0] + r'/2copy.html')
    images_path = []
    widget_List = []
    # file_name = []



    def initUI(self):
        self.show()


    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(1600,900)                        #창크기 고정
        self.setWindowTitle("Sky Viewer Solution Data Creator" + " Vesion Beta")
        self.setWindowIcon(QIcon("/Users/leehoseop/PycharmProjects/SVS_Data_Creator/images/icon.png"))
        self.image_Label.setStyleSheet("background-image : url(%s)" %self.background_picture)
        self.image_Label.setScaledContents(True)
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
        self.btn_adjust.clicked.connect(self.adjustimagedata)
        self.btn_Next.clicked.connect(self.upImageFromFile)
        self.btn_Previous.clicked.connect(self.downImageFromFile)
        self.btn_Image_Data_Generator.clicked.connect(self.Image_Labling)
        self.save_btn.clicked.connect(self.save_json_file)
        self.listWidget.itemClicked.connect(self.Clicked_list_item)

    def gps_data(self):
        global item
        filename = str(self.images_path[0]) + "/" + item.text()
        extension = filename.split('.')[-1]
        if (extension == 'jpg') | (extension == 'JPG') | (extension == 'jpeg') | (extension == 'JPEG'):
            try:
                img = Image.open(filename)
                info = img._getexif()
                exif = {}
                for tag, value in info.items():
                    decoded = TAGS.get(tag, tag)
                    exif[decoded] = value
                # from the exif data, extract gps
                exifGPS = exif['GPSInfo']
                latData = exifGPS[2]
                lonData = exifGPS[4]
                # calculae the lat / long
                latDeg = latData[0][0] / float(latData[0][1])
                latMin = latData[1][0] / float(latData[1][1])
                latSec = latData[2][0] / float(latData[2][1])
                lonDeg = lonData[0][0] / float(lonData[0][1])
                lonMin = lonData[1][0] / float(lonData[1][1])
                lonSec = lonData[2][0] / float(lonData[2][1])
                # correct the lat/lon based on N/E/W/S
                Lat = (latDeg + (latMin + latSec / 60.0) / 60.0)
                if exifGPS[1] == 'S': Lat = Lat * -1
                Lon = (lonDeg + (lonMin + lonSec / 60.0) / 60.0)
                if exifGPS[3] == 'W': Lon = Lon * -1
                # print file
                msg = "There is GPS info in this picture located at " + str(Lat) + "," + str(Lon)
                print(msg)
                # kmlheader = '<?xml version="1.0" encoding="UTF-8"?>' + '<kml xmlns="http://www.opengis.net/kml/2.2">'
                # kml = (
                #           '<Placemark><name>%s</name><Point><coordinates>%6f,%6f</coordinates></Point></Placemark></kml>') % (
                #           filename, Lon, Lat)
                # with open(filename + '.kml', "w") as f:
                #     f.write(kmlheader + kml)
                # print
                # 'kml file created'
            except:
                print
                'There is no GPS info in this picture'
                pass


    def File_Dialog(self):
        global images_path

        images_path = QFileDialog.getExistingDirectory(self, 'Open File')
        self.images_path.append(images_path)
        file_list = os.listdir(images_path)
        print(images_path)
        file_list_py = [file for file in file_list if file.endswith(self.exts)]  ## 파일명 끝이 .jpg인 경우

        for file in sorted(file_list_py):
            self.listWidget.addItem(file)
            self.listWidget.setCurrentRow(0)    #default 값으로 인덱싱 넘버 0 번의 아이템을 클릭하도록 함

    def Clear_File_List(self):
        self.listWidget.clear()         #파일리스트 삭제
        self.File_list_itemSelectionChange()
        self.file_path_label.setText("Undifined")
        self.images_path.clear()        #imagesPath 초기화
        self.qPixmapFileVar = QPixmap()
        self.qPixmapFileVar.load(str(self.background_picture))
        self.image_Label.setPixmap(self.qPixmapFileVar)


    def File_list_itemSelectionChange(self):
        global item
        global exifGPS
        global path
        global file_name_item
        global file_path_item
        item = self.listWidget.currentItem()
        path = self.images_path
        file_name_item = item.text()
        file_path_item = str(path[0]) + "/" + item.text()
        if (item == None):
            self.file_name_label.setText("Undifined")
        else:
            self.file_name_label.setText(file_name_item)           #현재 행의 파일 명
            self.file_path_label.setText(file_path_item) #현재 행의 경로와 파일 명

    def adjustimagedata(self) :  #수정한 데이터를 적용하여 라벨에 표시함
        # global item
        global exifGPS
        global resolution
        global latlong
        global file_name_item
        global file_path_item
        # gps 정보 추출
        # filename = str(path[0]) + "/" + item
        # print('this: ' + filename)
        # extension = filename.split('.')[-1]
        img = Image.open(file_path_item)
        info = img._getexif()   #getexif()를 사용하면 GPSInfo가 int타입으로 잘못출력됨 '_getexif()'를 사용
        exif = {}

        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            exif[decoded] = value
    # from the exif data, extract gps
        print(exif)
        print(exif['GPSInfo'])
    # print(filename)
        exifGPS = exif['GPSInfo']
        ImageWidth= exif['ImageWidth']
        ImageLength= exif['ImageLength']
        # ImageWidth = exifIW[]

    #네이버,카카오는 십진수를 주로 사용하고 구글은 전부 사용함
    #십진수 도(DD): 41.40338, 2.17403
    #도, 분, 초(DMS): 41°24'12.2"N 2°10'26.5"E
    #도 및 십진수 분(DMM): 41 24.2028, 2 10.4418
    # calculae the lat / long
    #경도
        latdegrees = float(exifGPS[2][0]) #/  float(exifGPS[2][1])  #도
        latminutes = float(exifGPS[2][1]) #/  float(exifGPS[2][1])   #분
        latseconds = float(exifGPS[2][2]) #/  float(exifGPS[2][1])   #초
    #위도
        londegrees = float(exifGPS[4][0]) #/  float(exifGPS[4][1])   #도
        lonminutes = float(exifGPS[4][1]) #/  float(exifGPS[4][1])   #분
        lonseconds = float(exifGPS[4][2]) #/  float(exifGPS[4][1])   #초
        #십진수로 교정 카카오나 네이버에서 사용하기 쉽도록 변형해준다.
        Lat = (latdegrees + (latminutes + latseconds / 60.0) / 60.0)
        Lon = (londegrees + (lonminutes + lonseconds / 60.0) / 60.0)

        resolution = str(ImageWidth) +','+ str(ImageLength)
        latlong = str(Lat) + "," + str(Lon)


        self.resolution_label.setText(resolution)
        self.lat_label.setText('%s' % Lat)  #십진수(DD)로 변환한 위도
        self.long_label.setText('%s' % Lon) #십진수(DD)로 변환한 경도

        #파노라마 이미지의 좌표값을 라벨에 적용
        clicked_points = WebEnginePage.point
        self.point_x_label.setText(clicked_points[0][0])
        self.point_y_label.setText(clicked_points[0][1])
        self.point_z_label.setText(clicked_points[0][2])

        #이미지가 촬영된 GPS 위도, 경도값을 라벨에 적용

    #클릭한 아이템을 라벨에 보여주도록 함
    def Clicked_list_item(self, item):
        self.qPixmapFileVar = QPixmap()
        self.qPixmapFileVar.load(str(self.images_path[0]) + "/" + str(item.text()))
        self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(1200)
        self.image_Label.setPixmap(self.qPixmapFileVar)

    def upImageFromFile(self) : #up
        row = self.listWidget.currentRow() #현재 행
        item = self.listWidget.item(row) #파일 이름
        value = self.listWidget.count() #리스트내 파일_전체 개수
        if row < value:
            self.listWidget.setCurrentRow(row+1)
            self.qPixmapFileVar = QPixmap()
            self.qPixmapFileVar.load(str(self.images_path[0]) + "/" + str(item.text()))
            self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(1200)
            self.image_Label.setPixmap(self.qPixmapFileVar)
            row -= 1
        if row > value:
            row = self.listWidget.setCurrentRow(0)
            return row
        print(value)
        print(row)

    def downImageFromFile(self) :  #down
        row = self.listWidget.currentRow() #현재 행
        item = self.listWidget.item(row)
        value = self.listWidget.count()
        if row < value:
            self.listWidget.setCurrentRow(row-1)
            self.qPixmapFileVar = QPixmap()
            self.qPixmapFileVar.load(str(self.images_path[0]) + "/" + str(item.text()))
            self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(1200)
            self.image_Label.setPixmap(self.qPixmapFileVar)
            row += 1
        if row > value:
            row = self.listWidget.setCurrentRow(value)
            return row
        print(value)
        print(row)

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
            self.second = secondwindow()    #두번째창 생성
            self.second.exec()          #두번째창 닫을때까지 기다림
            # self.show()  # 두번쨰창 닫으면 다시 메인윈도우

    def findTextCountInText(fname, word):
        cOunt = 0
        with open(fname, 'r') as f:
            for line in f:
                if word in line:
                    cOunt = cOunt + 1
        return cOunt

    def save_json_file(self):
        global images_path
        global item #파일명
        global file_name_item
        global file_path_item

        ext = "_json"
        json_path = images_path+ext
        if not os.path.exists(json_path):
            try:
                os.makedirs(json_path)
            except:
                print("already_exist")


        item = file_name_item
        file_name = item.split('.')[0]
        clicked_points = WebEnginePage.point
        name = self.second.second_text_name
        city = self.second.second_txt_city
        selected_object = self.second.second_text_item
        object_number = self.second.second_text_index
        web_url = self.second.second_text_url
        web_vurl = self.second.second_text_vurl
        production = "skyviewersolution"

        # json파일에 정보를 넣어준다.
        # file_data = OrderedDict()
        file_data = {}
        file_data['Version'] = "1.0.0"
        file_data['Production_company'] = "%s" %production
        file_data['Filename'] = "%s" %item
        file_data['City'] = "%s" %city
        file_data['Latitude,Longitude'] = "%s" %latlong
        file_data['Resolution'] = "%s" %resolution
        file_data['Info_point'] = []
        file_data['Info_point'].append({
            "Number": "1" ,
            "Name": name,
            "Item": selected_object,            #오브젝트
            "Index": object_number,             #인덱싱넘버
            "Url": web_url,                     #웹페이지 주소
            "Vurl":web_vurl,                    #유투브 소스
            "Point_x": clicked_points[0][0],    #x좌표
            "Point_y": clicked_points[0][1],    #y좌표
            "Point_z": clicked_points[0][2]     #z좌표
        })

        Img_json_file = json_path + '/' + file_name + '.json'

        if not os.path.exists(Img_json_file):
            print(json.dumps(file_data, ensure_ascii=False, indent="\t"))  # "\t"
            with open(Img_json_file, 'w', encoding="utf-8") as make_file:
                json.dump(file_data, make_file, ensure_ascii=False, indent="\t")
        else:
            print("already_exist")
            # file_data= {}
            with open(Img_json_file, "r") as json_file:
                file_data = json.load(json_file)

            txt = "Number"
            Number = WindowClass.findTextCountInText(Img_json_file, txt)
            Number += 1

            file_data['Info_point'].append({
                "Number": '%s' %str(Number),
                "Name": name,
                "Item": selected_object,  # 오브젝트
                "Index": object_number,  # 인덱싱넘버
                "Url": web_url,  # 웹페이지 주소
                "Vurl": web_vurl,  # 유투브 소스
                "Point_x": clicked_points[0][0],  # x좌표
                "Point_y": clicked_points[0][1],  # y좌표
                "Point_z": clicked_points[0][2]  # z좌표
            })
            print(json.dumps(file_data, ensure_ascii=False, indent="\t"))  # "\t"

            with open(Img_json_file, 'w') as make_file:
                json.dump(file_data, make_file, indent="\t")



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