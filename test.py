"""
The module implements a class that intercepts
signals from the map and sends its
"""
# Third party imports
from PyQt5 import QtCore
from PyQt5.QtWebEngineWidgets import QWebEnginePage


class WebEnginePage(QWebEnginePage):
    """
    The class that implements the connection
    between the events on the map, and the logic
    """

    # Signal when some object has been drawn
    # Param: coordinates - point for marker, or start-end points for area selection
    item_drawn = QtCore.pyqtSignal(tuple)

    # Signal when user zoomed map
    # Param: zoom-value
    zoom_changed = QtCore.pyqtSignal(int)

    def __init__(self, parent):
        """
        Initializing the handler
        :param parent: QWebEngineView
        """
        super().__init__(parent)
        self.parent = parent

    def javaScriptAlert(self, QUrl, p_str):
        """
        When you draw on the map, an alert arises,
        the method intercepts it, and sends its signal (item draw)
        :return: None
        """
        self.item_drawn.emit(self._js_unpack(p_str))

    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        """
        When the user zooms in/out the map,
        the zoom value is written to the console,
        the method intercepts this signal, and emits its (zoom_change)
        :return: None
        """
        if level == 0:
            self.zoom_changed.emit(int(msg))

    @staticmethod
    def _js_unpack(string: str) -> tuple:
        """
        Unpack the signal received from the map
        :param string: JS string to be processed
        :return: Returns the tuple obtained by processing the string
        """
        result = []
        split_str = string.replace("LatLng", "/").split("/")
        for item in split_str:
            item = item[:-1].replace('(', '').replace(')', '') \
                if item[-1] == ',' else item.replace('(', '').replace(')', '')

            if item != 'rectangle' and item != 'marker':
                item = tuple(map(float, item.split(',')))
            result.append(item)
        return tuple(result)