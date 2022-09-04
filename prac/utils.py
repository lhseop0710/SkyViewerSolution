import cv2
import numpy as np
from PyQt5.QtWidgets import *
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PySide2.QtCore import QUrl, Slot, QObject, QUrl
import constant

def mouse_handeler(event, x, y, flags, data):
    if event == cv2.EVENT_FLAG_LBUTTON:
        cv2.circle(data['img'], (x,y), 3, (0,0,255), 5, 16)
        cv2.imshow('Image', data['img'])
        data['points'].append([x,y])
            #점 찍은 좌표를 입력 받는 것.

def get_point(img):
    data={}
    data['img'] = img.copy()
    data['points']=[]

    cv2.imshow('Image', img)
    cv2.setMouseCallback("Image", mouse_handeler, data)
    #좌표를 받을 떄 사용
    cv2.waitKey(0)

    #마우스로 찍은 점을 float 형태로 변환
    point = np.array(data['points'], dtype=float)
    return point

class Handler(QObject):
    def __init__(self, *args, **kwargs):
        super(Handler, self).__init__(*args, **kwargs)

    @Slot(str, result=str)
    def sayHello(self, name):
        return f"Hello from the other side, {name}"


class WebEnginePage(QWebEnginePage):
    def __init__(self, *args, **kwargs):
        super(WebEnginePage, self).__init__(*args, **kwargs)

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceId):
        l = message.split(",")
        self.obj = l
        print ('JS: %s line %d: %s' % (sourceId, lineNumber, message))
        print("WebEnginePage Console: %s" %message)

