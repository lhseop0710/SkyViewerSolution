#!/usr/bin/env python3
import sys
import os
import time
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
    point = [[0,0,0]]
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
    number = 1
    image_directory_path = "/Users/leehoseop/PycharmProjects/pano_dataset/sejong_lake/"
    exts = ('.jpg', 'png', '.JPG', '.PNG', '.jpeg', '.JPEG')
    background_picture = "/Users/leehoseop/PycharmProjects/SVS_Data_Creator/images/icon.jpg"
    url = QtCore.QUrl().fromLocalFile(os.path.split(os.path.abspath(__file__))[0] + r'/index.html')  #html을 넣고 구동시키는 형태
    images_path = []
    widget_List = []
    infospot_num = 0            #inforpot 인덱싱 넘버 부여
    vinfospot_num =0           #video-infospot 인덱싱 넘버 부여
    panolink_num = 1
    viewer_num = 0
    info_list = [""]              #infospot 리스트로 추가적으로 반환받아 보관
    vinfo_desc_list = [""]             #vinfospot 콘테이너를 리스트로 추가적으로 반환받아 보관
    vinfo_list = [""]                  #vinfospot 을 리스트로 추가하기 위함
    image_list=[""]               # 파노링크 이미지 리스트로 추가
    panolink_forward_list = [""]          # 이미지간 연결을 해주기 위해 리스트로 추가
    panolink_backward_list = [""]
    viewer_list = [""]
    image_index = ""
    infospot_index = ""         #infospot 내용 문자열 추가
    vinfospot_index = ""        #vinfospot 내용 문자열 추가
    panolink_index = ""         #링크 내용 문자열 추가
    viewer_index = ""

    def initUI(self):
        self.show()


    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(1600,1000)                        #창크기 고정
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
        self.webview.setGeometry(15, 12, 1200, 700)
        self.webview.load(self.url)
        self.webview_layout.addWidget(self.webview)

        self.btn_loadFromFile.clicked.connect(self.File_Dialog)
        self.get_html_btn.clicked.connect(self.get_html)
        # self.pushbutton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn_Delete_List.clicked.connect(self.Clear_File_List)
        self.listWidget.itemSelectionChanged.connect(self.File_list_itemSelectionChange)
        self.btn_adjust.clicked.connect(self.adjustimagedata)
        self.btn_Next.clicked.connect(self.upImageFromFile)
        self.btn_Previous.clicked.connect(self.downImageFromFile)
        self.btn_Image_Data_Generator.clicked.connect(self.Image_Labling)
        self.save_btn.clicked.connect(self.save_json_file)
        self.listWidget.itemClicked.connect(self.Clicked_list_item)
        self.infospot_add_btn.clicked.connect(self.infospot_add)
        self.video_spot_add_btn.clicked.connect(self.vinfospot_add)
        self.infospot_check_btn.clicked.connect(self.infospot_check)
        self.panolink_check1_btn.clicked.connect(self.panolink1_image_check)
        self.panolink_check2_btn.clicked.connect(self.panolink2_image_check)
        self.panolink_add1_btn.clicked.connect(self.make_front_panolink)
        self.panolink_add2_btn.clicked.connect(self.make_backward_panolink)
        # self.viewer_add_btn.clicked.connect(self.make_viewer)

    def make_front_panolink(self):
        clicked_points = WebEnginePage.point
        global value, relpath, image_list, panolink_forward_list, viewer_list
        num = self.listWidget.currentRow()
        image_list = self.image_list
        panolink_forward_list = self.panolink_forward_list
        viewer_list = self.viewer_list
        num += 1

        panolink_info = "\t\t\t\t\t\t"+"panorama"+str(num)+".link("+"panorama"+str(num+1)+", new THREE.Vector3("+ str(clicked_points[0][0]) + ", " + str(clicked_points[0][1]) + ", " + str(clicked_points[0][2]) + " ), 400 );" + "\n"

        panolink_forward_list.append(str(panolink_info))

    def make_backward_panolink(self):
        clicked_points = WebEnginePage.point
        global value, relpath, image_list, panolink_backward_list, viewer_list
        num = self.listWidget.currentRow()
        image_list = self.image_list
        panolink_backward_list = self.panolink_backward_list
        viewer_list = self.viewer_list
        num += 1

        panolink_info = "\t\t\t\t\t\t"+"panorama"+str(num)+".link("+"panorama"+str(num-1)+", new THREE.Vector3("+ str(clicked_points[0][0]) + ", " + str(clicked_points[0][1]) + ", " + str(clicked_points[0][2]) + " ), 400 );" + "\n"

        panolink_backward_list.append(str(panolink_info))


    # def make_viewer(self):
    #     global value, relpath, image_list, panolink_list, viewer_list, file_path_item
    #     image_list = self.image_list
    #     viewer_list = self.viewer_list
    #     self.viewer_num += 1
    #     num = self.listWidget.currentRow()
    #     relpath = os.path.relpath(file_path_item, "/Users/leehoseop/PycharmProjects/SVS_Data_Creator")
    #
    #     image_info = "\t\t\t\t\t\t"+"panorama"+str(num+1)+"= new PANOLENS.ImagePanorama(""'./" + relpath + "'"");" "\n" + \
    #                  "\t\t\t\t\t\t"+"panorama"+str(num+1)+".addEventListener("'"click"'+ ", function(e) {"+ "\n" + \
    #                  "\t\t\t\t\t\t"+"   if (e.intersects.length > 0) return;"+ "\n" + \
    #                  "\t\t\t\t\t\t"+"   const a = viewer.raycaster.intersectObject(viewer.panorama, true)[0].point;" + "\n" + \
    #                  "\t\t\t\t\t\t"+"   console.log(JSON.stringify(a));"+ "\n" + \
    #                  "\t\t\t\t\t\t"+"});"+ "\n"
    #                  # "\t\t\t\t\t\t"+"panorama" + str(num+1) + "= new PANOLENS.ImagePanorama(""'./" + str(self.panolink_file_label2.text()) + "'"");" + "\n" + \
    #                  # "\t\t\t\t\t\t"+"panorama" + str(num+1) + ".addEventListener("'"click"' + ", function(e) {" + "\n" + \
    #                  # "\t\t\t\t\t\t"+"   if (e.intersects.length > 0) return;" + "\n" + \
    #                  # "\t\t\t\t\t\t"+"   const a = viewer.raycaster.intersectObject(viewer.panorama, true)[0].point;" + "\n" + \
    #                  # "\t\t\t\t\t\t"+"   console.log(JSON.stringify(a));" + "\n" + \
    #                  # "\t\t\t\t\t\t"+"});"
    #
    #
    #     image_list.append(str(image_info))
    #     self.viewer_num_label.setText(str(self.viewer_num))
    #
    #     viewer_info = "\t\t\t\t\t\t"+ "viewer.add( "+"panorama"+str(num+1)+");" + "\n"
    #                   # "\t\t\t\t\t\t"+ "viewer.add( " + "panorama" + str(num+1) + ");"
    #     viewer_list.append(str(viewer_info))


    def panolink1_image_check(self):
        global file_name_item
        global file_path_item
        relpath = os.path.relpath(file_path_item, "/Users/leehoseop/PycharmProjects/SVS_Data_Creator")
        self.panolink_file_label1.setText(relpath)

    def panolink2_image_check(self):
        global file_path_item
        global file_name_item
        relpath = os.path.relpath(file_path_item, "/Users/leehoseop/PycharmProjects/SVS_Data_Creator")
        self.panolink_file_label2.setText(relpath)


    def infospot_add(self):
        global infospot_index
        global info_list
        global infospot_information
        self.infospot_num += 1
        clicked_points = WebEnginePage.point
        info_list = self.info_list
        num = self.listWidget.currentRow()

        html_info = "\t\t\t\t\t\t" + "infospot" + str(self.infospot_num) + " = new PANOLENS.Infospot();""\n" + \
                    "\t\t\t\t\t\t" + "infospot" + str(self.infospot_num) + ".position.set( " + str(clicked_points[0][0]) + ", " + str(clicked_points[0][1]) + ", " + str(clicked_points[0][2]) + " );""\n" + \
                    "\t\t\t\t\t\t" + "infospot" + str(self.infospot_num) + ".addHoverText('"+ str(infospot_information)+"');" + "\n" + \
                    "\t\t\t\t\t\t" + "infospot" + str(self.infospot_num) + ".addEventListener( 'click', function(){this.focus();} );" + "\n" + \
                    "\t\t\t\t\t\t" + "panorama"+str(num+1)+".add( infospot" + str(self.infospot_num) + " );"


        info_list.append(str(html_info))
        self.infospot_num_label.setText(str(self.infospot_num))

    def vinfospot_add(self):
        global vinfospot_index
        global vinfo_list
        global vinfo_desc_list
        global vinfospot_url , vinfospot_title, vinfospot_information, web_vurl
        vinfo_list = self.vinfo_list
        vinfo_desc_list = self.vinfo_desc_list
        clicked_points = WebEnginePage.point
        vinfospot_url = self.second.second_text_vurl
        vinfospot_title = self.second.second_text_name
        vinfospot_information = self.second.second_text_vinfo
        self.vinfospot_num += 1
        num = self.listWidget.currentRow()


        html_desc =  "\n"+"\t\t\t\t\t" + "<div id="+'"desc-container'+str(self.vinfospot_num)+'"' + " style="+'"display:none"'+">"+"\n"+\
                     "\t\t\t\t\t" + " <iframe src =" + '"' +str(vinfospot_url) +'"' + "></iframe>"+"\n"+\
                     "\t\t\t\t\t" + ' <div class="title">'+ '"' + str(vinfospot_title) + '"' +"</div>"+"\n"+\
                     "\t\t\t\t\t" + ' <div class="text">' +'"'+str(vinfospot_information)+'"'+"</div>"+"\n"+\
                     "\t\t\t\t\t" + "</div>"+"\n"

        html_vinfo = "\n"+"\t\t\t\t\t\t" + "vinfospot" + str(self.vinfospot_num) + " = new PANOLENS.Infospot(300, PANOLENS.DataImage.Info);""\n" + \
                     "\t\t\t\t\t\t" + "vinfospot" + str(self.vinfospot_num) + ".position.set( " + str(clicked_points[0][0]) + ", " + str(clicked_points[0][1]) + ", " + str(clicked_points[0][2]) + " );""\n" + \
                     "\t\t\t\t\t\t" + "vinfospot" + str(self.vinfospot_num) + ".addHoverElement(document.getElementById('" + "desc-container"+str(self.vinfospot_num) + "'), 200);" + "\n" + \
                     "\t\t\t\t\t\t" + "panorama"+str(num+1)+".add( vinfospot" + str(self.vinfospot_num) + " );" + "\n"

        #"\t\t\t\t\t\t" + "vinfospot" + str(self.vinfospot_num) + ".addEventListener( 'click', function(){this.focus();} );" + "\n" + \
        vinfo_list.append(str(html_vinfo))
        vinfo_desc_list.append(str(html_desc))


        self.vinfospot_num_label.setText(str(self.vinfospot_num))

    def infospot_check(self):
        global infospot_information

        # for item in info_list:
        #     print (item)

        # 인포스팟 정보 땡겨오기
        information_text = self.information_textEdit.toPlainText()
        self.information_label.setText(information_text)
        infospot_information = self.information_label.text()
        self.point_x_label.setText(str(WebEnginePage.point[0][0]))
        self.point_y_label.setText(str(WebEnginePage.point[0][1]))
        self.point_z_label.setText(str(WebEnginePage.point[0][2]))

    def vinfospot_check(self):
        global vinfospot_url, vinfospot_title, vinfospot_information

        vinformation_text_title = self.vinformation_textEdit.toPlainText()
        self.vinformation_label.setText(vinformation_text_title)
        vinfospot_title = self.vinformation_label.text()
        self.point_x_label.setText(str(WebEnginePage.point[0][0]))
        self.point_y_label.setText(str(WebEnginePage.point[0][1]))
        self.point_z_label.setText(str(WebEnginePage.point[0][2]))

    def get_html(self):
        self.infospot_num = 0
        self.vinfospot_num = 0
        self.panolink_num = 0
        self.infospot_num_label.setText(str(self.infospot_num))
        self.vinfospot_num_label.setText(str(self.vinfospot_num))
        print("make html")
        global images_path
        global file_path_item
        global info_list, vinfo_list, vinfo_desc_list, relpath, image_list, panolink_forward_list, panolink_backward_list


        relpath = os.path.relpath(file_path_item, "/Users/leehoseop/PycharmProjects/SVS_Data_Creator")
        ext = "_html"
        html_path = images_path + ext
        if not os.path.exists(html_path):
            try:
                os.makedirs(html_path)
            except:
                print("already_exist")

        # Html파일에 정보를 넣어준다.

        html_text1 = """
            <!DOCTYPE html>
            <html>
                <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="initial-scale=1, maximum-scale=1, user-scalable=no, width=device-width, shrink-to-fit=no">
                    <title>Panolens.js panorama image panorama</title>
                    <link href="css/stayle.css" rel="stylesheet" type="text/css">
                </head>
                <body>
                    <div class="credit"><a href="https://github.com/pchen66/panolens.js">Panolens.js</a> SkyViewerSolution.Corporation. Image from <a href="https://github.com/lhseop0710">Hoseop Lee</a></div>
        """
        html_scripts = """
                    <script src="three.min.js"></script>
                    <script src="panolens.min.js"></script>
                    <script>
                        var panorama1;
                        var infospot1, infospot2, viewer;
        """
        html_Number = "\t\t\t\t" + "var Num_index = 0;""\n"


        html_img = "\n"\
                   "\t\t\t\t\t\t" +  "panorama1 = new PANOLENS.ImagePanorama(""'./" + relpath + "'"");" "\n"


        html_text2 = """
                        viewer = new PANOLENS.Viewer({
                            container: document.body,        // A DOM Element container
                            controlBar: true,             // Vsibility of bottom control bar
                            controlButtons: [],            // Buttons array in the control bar. Default to ['fullscreen', 'setting', 'video']
                            autoHideControlBar: false,        // Auto hide control bar
                            autoHideInfospot: false,            // Auto hide infospots
                            horizontalView: false,            // Allow only horizontal camera control
                            cameraFov: 60,                // Camera field of view in degree
                            reverseDragging: false,            // Reverse orbit control direction
                            enableReticle: false,            // Enable reticle for mouseless interaction
                            dwellTime: 1500,            // Dwell time for reticle selection in millisecond
                            autoReticleSelect: true,        // Auto select a clickable target after dwellTime
                            viewIndicator: false,            // Adds an angle view indicator in upper left corner
                            indicatorSize: 30,            // Size of View Indicator
                            output: 'console'            // Whether and where to output infospot position. Could be 'console' or 'overlay'
                          });
                        
        """
        html_ends = """
                    </script>
                </body>
            </html>
        """
        html_file_path = html_path + '/' + 'html_file.html'
        html_text = html_text1  + html_scripts + html_Number + html_img + html_text2 + html_ends

        ######################
        if not os.path.exists(html_file_path):
            with open( html_file_path, 'w', encoding="utf-8") as html_file:
                html_file.write(html_text)
        else:
            print("already_exist")

            #####연습######
            infospots = '\n'.join(info_list)
            video_infospots = '\n'.join(vinfo_list)
            video_desc = '\n'.join(vinfo_desc_list)
            panoforwardlink = '\n'.join(panolink_forward_list)
            panobackwardlink = '\n'.join(panolink_backward_list)
            images = '\n'.join(image_list)
            viewer = '\n'.join(viewer_list)


            html_text = html_text1 + video_desc + html_scripts + html_Number + images + html_text2 + infospots +video_infospots + panoforwardlink + panobackwardlink + viewer + html_ends


            with open('html_file.html', 'w') as html_file:
                html_file.write(html_text)
                ##################

        # html_text = html_text1 + html_img + html_text2
        #
        # with open('html_file.html', 'w') as html_file:
        #     html_file.write(html_text)

        #html_info = "\t\t\t" + "infospot"+Number+"= new PANOLENS.Infospot( PANOLENS.DataImage.Info);""\n"+"infospot"+Number+".position.set("+str(clicked_points[0][0]) + "," + str(clicked_points[0][1])+ "," + str(clicked_points[0][2])+" );""\n"+"infospot"+Number+".addHoverText( 'Infospot');""\n""infospot"+Number+".addEventListener( 'click', onFocus );"


        self.url = QtCore.QUrl().fromLocalFile(
            os.path.split(os.path.abspath(__file__))[0] + r'/html_file.html')  # html을 넣고 구동시키는 형태
        self.webview.load(self.url)



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
        global value, relpath, image_list, panolink_list, viewer_list, file_path_item


        images_path = QFileDialog.getExistingDirectory(self, 'Open File')
        self.images_path.append(images_path)
        file_list = os.listdir(images_path)
        file_list.sort()
        print(images_path)
        file_list_py = [file for file in file_list if file.endswith(self.exts)]  ## 파일명 끝이 .jpg인 경우
        image_list = self.image_list
        viewer_list = self.viewer_list
        num = 0
        print(file_list_py)


        for file in sorted(file_list_py):
            self.listWidget.addItem(file)
            image_add = images_path+"/"+file
            relpath = os.path.relpath(image_add, "/Users/leehoseop/PycharmProjects/SVS_Data_Creator")
            self.viewer_num += 1
            num += 1

            image_info = "\t\t\t\t\t\t" + "panorama" + str(num) + "= new PANOLENS.ImagePanorama(""'./" + relpath + "'"");" "\n" + \
                         "\t\t\t\t\t\t" + "panorama" + str(num) + ".addEventListener("'"click"' + ", function(e) {" + "\n" + \
                         "\t\t\t\t\t\t" + "   if (e.intersects.length > 0) return;" + "\n" + \
                         "\t\t\t\t\t\t" + "   const a = viewer.raycaster.intersectObject(viewer.panorama, true)[0].point;" + "\n" + \
                         "\t\t\t\t\t\t" + "   console.log(JSON.stringify(a));" + "\n" + \
                         "\t\t\t\t\t\t" + "});" + "\n"

            image_list.append(str(image_info))
            self.viewer_num_label.setText(str(self.viewer_num))

            viewer_info = "\t\t\t\t\t\t" + "viewer.add( " + "panorama" + str(num) + ");" + "\n"
            viewer_list.append(str(viewer_info))

            self.listWidget.setCurrentRow(0)    #default 값으로 인덱싱 넘버 0 번의 아이템을 클릭하도록 함
            self.number += 1
            ###

        print(self.image_list)
        #전체 아이템 개수
        value = self.listWidget.count()
        # setting text to the label
        self.item_num_label.setText(str(value))



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
        global value

        item = self.listWidget.currentItem()
        path = self.images_path
        file_name_item = item.text()
        file_path_item = str(path[0]) + "/" + item.text()

        if (item == None):
            self.file_name_label.setText("Undifined")
        else:
            self.file_name_label.setText(file_name_item)           #현재 행의 파일 명
            self.file_path_label.setText(file_path_item)           #현재 행의 경로와 파일 명

    def adjustimagedata(self) :  #수정한 데이터를 적용하여 라벨에 표시함
        # global item
        global exifGPS
        global resolution
        global latlong
        global file_name_item
        global file_path_item
        global clicked_point
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
        global name

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


if __name__ == "__main__" :

    app = QApplication(sys.argv)
    myWindow = WindowClass()
    # Make the handler object available, naming it "backend"
    myWindow.show()
    app.exec_()