from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import Qt
import cv2
import json
from collections import OrderedDict

form_secondwindow = uic.loadUiType("secondwindow.ui")[0] #두 번째 창 ui
class secondwindow(QDialog, QWidget, form_secondwindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(380,770)                        #창크기 고정
        self.initUI()
        self.show() #두번째창 실행

        self.Add_btn.clicked.connect(self.Add_Object)
        self.Delete_btn.clicked.connect(self.Delete_Object)
        self.Clear_btn.clicked.connect(self.Clear_Object)
        self.Object_list.itemSelectionChanged.connect(self.Object_list_itemSelectionChange)
        self.Adjust_btn.clicked.connect(self.adjust_labeling_information)
        # self.close_btn.clicked.connect(self.close)
        # self.home_btn.clicked.connect(self.home)

    def initUI(self):
        self.setWindowTitle("SVS_DATA_CREATOR" + " / Version Beta")
        self.setWindowFlag(Qt.WindowStaysOnTopHint)


    def Add_Object(self):
        query = self.Object_name_textEdit.toPlainText()
        self.Object_name_textEdit.setText("")
        self.Object_list.addItem(query)

    def Delete_Object(self):
        rn = self.Object_list.currentRow()
        self.Object_list.takeItem(rn)

    def Clear_Object(self):
        self.Object_list.clear()
        self.Object_list_itemSelectionChange()

    def Object_list_itemSelectionChange(self):
        item = self.Object_list.currentItem()
        value = self.Object_list.currentRow()
        if (item == None):
            self.item_label.setText("[selection]")
            self.index_lable.setText("[selection]")
            self.Delete_btn.setEnabled(False)
        else:
            self.item_label.setText(item.text())
            self.index_label.setText(str(value))
            self.Delete_btn.setEnabled(True)

    def adjust_labeling_information(self):
        #클래스와 인덱싱 넘버를 적용
        self.second_text_item = self.item_label.text()
        self.second_text_index = self.index_label.text()
        #url 주소를 적용
        url = self.url_txt_edit.toPlainText()
        self.url_label.setText(url)
        self.second_text_url = self.url_label.text()
        #vurl 주소를 적용
        vurl = self.vurl_txt_edit.toPlainText()
        self.vurl_label.setText(vurl)
        self.second_text_vurl = self.vurl_label.text()
        #이름을 적용 (건물, 상호, 공공기관 등)
        name = self.name_txt_edit.toPlainText()
        self.name_label.setText(name)
        self.second_text_name = self.name_label.text()
        #도시,지방 이름을 적용(특별시,광역시 시 단위로 작성)
        city = self.city_txt_edit.toPlainText()
        self.city_label.setText(city)
        self.second_txt_city = self.city_label.text()



    def close(self):
        self.close()  # 메인윈도우 숨김

    # def home(self):
    #     self.close()  # 메인윈도우 숨김
    #     self.main = form_class()  # 두번째창 생성
    #     self.main.exec()  # 두번째창 닫을때까지 기다림
    #     self.hide()

