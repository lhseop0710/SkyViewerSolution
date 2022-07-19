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
        self.initUI()
        self.show() #두번째창 실행

        self.Add_btn.clicked.connect(self.Add_Object)
        self.Delete_btn.clicked.connect(self.Delete_Object)
        self.Clear_btn.clicked.connect(self.Clear_Object)
        self.Object_list.itemSelectionChanged.connect(self.Object_list_itemSelectionChange)
        self.Save_btn.clicked.connect(self.save_labeling_information)
        # self.close_btn.clicked.connect(self.close)
        self.home_btn.clicked.connect(self.home)

    def initUI(self):
        self.setWindowTitle("VUASRL_IMAGE_DATA_CREATOR" + " / Version 1.0.0")
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
        if (item == None):
            self.item_label.setText("[selection]")
            self.Delete_btn.setEnabled(False)
        else:
            self.item_label.setText(item.text())
            self.Delete_btn.setEnabled(True)

    def save_labeling_information(self):
        self.second_text = self.item_label.text()
        self.close()

    # def close(self):
    #     self.close()

    def home(self):
        self.close()  # 메인윈도우 숨김
        self.main = SVS_Viewer()  # 두번째창 생성
        self.second.exec()  # 두번째창 닫을때까지 기다림
        self.hide()
        cv2.destroyAllWindows()

