import os
from pathlib import Path
from PySide2.QtWidgets import QApplication
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PySide2.QtWebChannel import QWebChannel
from PySide2.QtCore import QUrl, Slot, QObject, QUrl
from PyQt5.QtCore import QObject
from PyQt5.QtWebEngineWidgets import QWebEnginePage
import constant

data_dir = Path(os.path.abspath(os.path.dirname(__file__))) / 'data'


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


if __name__ == "__main__":
    # Set up the main application
    app = QApplication([])
    app.setApplicationDisplayName("Greetings from the other side")

    # Use a webengine view
    view = QWebEngineView()
    view.resize(1200, 675)

    # Set up backend communication via web channel
    handler = Handler()
    channel = QWebChannel()
    # Make the handler object available, naming it "backend"
    channel.registerObject("backend", handler)

    # Use a custom page that prints console messages to make debugging easier
    page = WebEnginePage()
    page.setWebChannel(channel)
    view.setPage(page)

    # Finally, load our file in the view
    url = QUrl.fromLocalFile("/2.html")
    view.load(url)
    view.show()

    app.exec_()

# from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
# import os
# class Ui_Dialog(object):
#     def setupUi(self, Dialog):
#         Dialog.setObjectName("Dialog")
#         Dialog.resize(400, 300)
#         # self.widget_youtube.setGeometry(QtCore.QRect(15, 12, 1200, 675))
#         self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
#         self.verticalLayout.setObjectName("verticalLayout")
#         self.centralwidget = QtWidgets.QWidget(Dialog)
#         self.centralwidget.setObjectName("centralwidget")
#         self.webEngineView = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
#         self.webEngineView.load(QtCore.QUrl().fromLocalFile(os.path.split(os.path.abspath(__file__))[0]+r'/2.html'))
#         self.verticalLayout.addWidget(self.webEngineView)
#         self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
#         self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
#         self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
#         self.buttonBox.setObjectName("buttonBox")
#         self.verticalLayout.addWidget(self.buttonBox)
#         self.retranslateUi(Dialog)
#         self.buttonBox.accepted.connect(Dialog.accept)
#         self.buttonBox.rejected.connect(Dialog.reject)
#         QtCore.QMetaObject.connectSlotsByName(Dialog)
#     def retranslateUi(self, Dialog):
#         _translate = QtCore.QCoreApplication.translate
#         Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
#     def javaScriptConsoleMessage(self, message, line, source):
#         """Prints client console message in current output stream."""
#         super(Ui_Dialog, self).javaScriptConsoleMessage(message, line,source)
#
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     Dialog = QtWidgets.QDialog()
#     ui = Ui_Dialog()
#     ui.setupUi(Dialog)
#     Dialog.show()
#     sys.exit(app.exec_())