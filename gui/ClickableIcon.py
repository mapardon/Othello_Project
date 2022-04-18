from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ClickableIcon(QAbstractButton):
    def __init__(self, icon, parent=None):
        super(ClickableIcon, self).__init__(parent)
        self.pixmap = QPixmap(icon)
        self.setMinimumSize(60, 60)
        self.setMaximumSize(100, 100)

    def editPixmap(self, icon):
        self.pixmap = QPixmap(icon)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()
