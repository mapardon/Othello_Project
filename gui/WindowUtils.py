from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication, Qt


class WindowUtils(QWidget):
    """Some repetitive operations in UI initialization have been factorized here"""

    def __init__(self, wrap):
        super(WindowUtils, self).__init__()
        self.wrap = wrap

    @staticmethod
    def exiter():
        QCoreApplication.quit()

    @staticmethod
    def init_combobox(elements, centralWidget):
        cb = QComboBox(centralWidget)
        cb.setMinimumWidth(125)
        for el in elements:
            cb.addItem(el)
        if cb.count():
            cb.setCurrentIndex(0)
        return cb

    @staticmethod
    def horizontal_menu_widget_layouter(*wids):
        layout = QHBoxLayout()
        layout.addStretch()
        for w in wids:
            layout.addWidget(w, Qt.AlignLeft)
        layout.addStretch()
        return layout

    @staticmethod
    def groupboxer(title, *layouts):
        groupBox = QGroupBox(title)
        groupBox.setMinimumWidth(300)
        layout_for_gb = QVBoxLayout()
        for l in layouts:
            layout_for_gb.addLayout(l)
        groupBox.setLayout(layout_for_gb)

        layouted = QHBoxLayout()
        layouted.addStretch()
        layouted.addWidget(groupBox, Qt.AlignCenter)
        layouted.addStretch()

        return layouted

    @staticmethod
    def itemizator(cbbox):
        return [cbbox.itemText(i) for i in range(cbbox.count())]

    @staticmethod
    def label_and_input(label_name, centralWidget, lim=False):
        label = QLabel(label_name, centralWidget)
        label.setMinimumWidth(100)
        entree = QLineEdit(centralWidget)
        entree.setMinimumWidth(125)
        if lim:
            entree.setMaxLength(15)
        return label, entree

    @staticmethod
    def easter_eggs_manager(code):
        ret = int()
        if code == "__S4LTY__":
            WindowUtils.informative_popup("luvu 愛", "Je t'aime Salty ^.^" + chr(2764))
        elif code == "__AM3LI__":
            WindowUtils.informative_popup("Cc Mimi ^.^", "Bon courage piti poulet !! ;*")
        else:
            ret = -1
        return ret

    @staticmethod
    def informative_popup(title, msg, btnname=str()):
        sentinel = QMessageBox()
        sentinel.setWindowTitle(title)
        sentinel.setText(msg)
        sentinel.setIcon(QMessageBox.Information)
        sentinel.setStandardButtons(sentinel.Ok)
        unique_button = sentinel.button(QMessageBox.Ok)
        btnname = len(btnname) and btnname or "Ok"
        unique_button.setText(btnname)
        sentinel.exec_()

    @staticmethod
    def interrogative_popup(title, msg, btnnames=("Affirmatif", "Négatif")):
        # btnnames = container 2 els
        sentinel = QMessageBox()
        sentinel.setWindowTitle(title)
        sentinel.setText(msg)
        sentinel.setIcon(QMessageBox.Question)
        sentinel.setStandardButtons(sentinel.Yes | sentinel.No)
        left_button = sentinel.button(QMessageBox.Yes)
        left_button.setText(btnnames[0])
        right_button = sentinel.button(QMessageBox.No)
        right_button.setText(btnnames[1])
        sentinel.exec_()

        if sentinel.clickedButton() == left_button:
            return True
        else:
            return False

    @staticmethod
    def output_str_format(w, t):
        return w[0].upper() + w[1:], t[0].upper() + t[1:]
