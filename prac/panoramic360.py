import sys
import urllib.request
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic, QtCore, QtGui, QtWidgets

form_Panoramic = uic.loadUiType("panoramic360.ui")[0] #두 번째 창 ui
class panoramic360(QDialog, QWidget, form_Panoramic):
    def __init__(self, imagePath):
        super().__init__()
        self.setupUi(self)
        self.setCursor(QtCore.Qt.CrossCursor)
        self.setFixedSize(1200, 670)  # 창크기 고정
        self.setWindowTitle("SVS 360 Panoramic Viewer")
        # keep a reference of the original image
        self.source = QtGui.QPixmap(imagePath)
        self.pano = QtGui.QPixmap(self.source.width() * 3, self.source.height())
        self.center = self.pano.rect().center()
        # use a QPointF for precision
        self.delta = QtCore.QPointF()
        self.deltaTimer = QtCore.QTimer(interval=25, timeout=self.moveCenter)
        self.sourceRect = QtCore.QRect()
        # create a pixmap with three copies of the source;
        # this could be avoided by smart repainting and translation of the source
        # but since paintEvent automatically clips the painting, it should be
        # faster then computing the new rectangle each paint cycle, at the cost
        # of a few megabytes of memory.
        self.setMaximumSize(self.source.size())
        qp = QtGui.QPainter(self.pano)
        qp.drawPixmap(0, 0, self.source)
        qp.drawPixmap(self.source.width(), 0, self.source)
        qp.drawPixmap(self.source.width() * 2, 0, self.source)
        qp.end()
        self.show()

        self.btn_return_home.clicked.connect(self.return_home)

    def return_home(self):
        self.close()                    #메인윈도우 숨김


    def moveCenter(self):
        if not self.delta:
            return
        self.center += self.delta
        # limit the vertical position
        if self.center.y() < self.sourceRect.height() * .5:
            self.center.setY(self.sourceRect.height() * .5)
        elif self.center.y() > self.source.height() - self.height() * .5:
            self.center.setY(self.source.height() - self.height() * .5)
        # reset the horizontal position if beyond the center of the virtual image
        if self.center.x() < self.source.width() * .5:
            self.center.setX(self.source.width() * 1.5)
        elif self.center.x() > self.source.width() * 2.5:
            self.center.setX(self.source.width() * 1.5)
        self.sourceRect.moveCenter(self.center.toPoint())
        self.update()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mousePos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() != QtCore.Qt.LeftButton:
            return
        delta = event.pos() - self.mousePos
        # use a fraction to get small movements, and ensure we're not too fast
        self.delta.setX(max(-25, min(25, delta.x() * .125)))
        self.delta.setY(max(-25, min(25, delta.y() * .125)))
        if not self.deltaTimer.isActive():
            self.deltaTimer.start()

    def mouseReleaseEvent(self, event):
        self.deltaTimer.stop()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.drawPixmap(self.rect(), self.pano, self.sourceRect)

    # resize and reposition the coordinates whenever the window is resized
    def resizeEvent(self, event):
        self.sourceRect.setSize(self.size())
        self.sourceRect.moveCenter(self.center)
#
# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     w = panoramic360('/Users/leehoseop/Desktop/Photo_1080295507_DJI_83_pano_14026756_0_2022623175722_photo_original.JPG')
#     w.show()
#     sys.exit(app.exec_())