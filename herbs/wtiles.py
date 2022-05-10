import os
import sys
import numpy as np
import pyqtgraph as pg
import pyqtgraph.functions as fn
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class LayerSettingDialog(QDialog):
    def __init__(self, window_name, min_val, max_val, val):
        super().__init__()

        self.setWindowTitle(window_name)

        self.val = val

        self.val_slider = QSlider(Qt.Horizontal)
        self.val_slider.setValue(val)
        self.val_slider.setMinimum(min_val)
        self.val_slider.setMaximum(max_val)
        self.val_slider.setSingleStep(1)
        self.val_slider.sliderMoved.connect(self.val_spinbox_changed)

        self.val_spinbox = QSpinBox()
        self.val_spinbox.setValue(val)
        self.val_spinbox.setMaximum(max_val)
        self.val_spinbox.setMinimum(min_val)
        self.val_spinbox.setSingleStep(1)
        self.val_spinbox.valueChanged.connect(self.value_changed)

        # ok button, used to close window
        ok_btn = QDialogButtonBox(QDialogButtonBox.Ok)
        ok_btn.accepted.connect(self.accept)

        # add widget to layout
        layout = QHBoxLayout()
        layout.addWidget(self.val_slider)
        layout.addWidget(self.val_spinbox)
        layout.addSpacing(10)
        layout.addWidget(ok_btn)
        self.setLayout(layout)

    def accept(self) -> None:
        self.close()

    def val_spinbox_changed(self):
        val = self.val_slider.value()
        self.val = val
        self.val_spinbox.setValue(val)

    def value_changed(self):
        val = self.val_spinbox.value()
        self.val = val
        self.val_slider.setValue(val)


class QDoubleButton2(QPushButton):
    doubleClicked = pyqtSignal()
    clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        QPushButton.__init__(self, *args, **kwargs)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.clicked.emit)
        super().clicked.connect(self.checkDoubleClick)

        self.setFixedHeight(60)

    @pyqtSlot()
    def checkDoubleClick(self):
        if self.timer.isActive():
            self.doubleClicked.emit()
            self.timer.stop()
        else:
            self.timer.start(60)


class QDoubleButton(QPushButton):
    right_clicked = pyqtSignal()
    left_clicked = pyqtSignal()
    double_clicked = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(QDoubleButton, self).__init__(*args, **kwargs)

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(150)
        self.timer.timeout.connect(self.timeout)

        self.is_double = False
        self.is_left_click = True

        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.MouseButtonPress:
            if not self.timer.isActive():
                self.timer.start()

            self.is_left_click = False
            if event.button() == Qt.LeftButton:
                self.is_left_click = True

            return True

        elif event.type() == QEvent.MouseButtonDblClick:
            self.is_double = True
            return True

        return False

    def timeout(self):
        if self.is_double:
            self.double_clicked.emit()
        else:
            if self.is_left_click:
                self.left_clicked.emit()
            else:
                self.right_clicked.emit()

        self.is_double = False


class QLabelClickable(QLabel):
    # doubleClicked = pyqtSignal(object)
    clicked = pyqtSignal(object)

    def __init__(self, parent=None):
        super(QLabelClickable, self).__init__(parent)

    def mousePressEvent(self, event):
        self.ultimo = 'Click'

    def mouseReleaseEvent(self, event):
        if self.ultimo == 'Click':
            QTimer.singleShot(QApplication.instance().doubleClickInterval(),
                              self.performSingleClickAction)
        else:
            self.ultimo = 'doubleClick'
            self.clicked.emit(self.ultimo)

    def mouseDoubleClickEvent(self, event):
        self.ultimo = 'doubleClick'

    def performSingleClickAction(self):
        if self.ultimo == 'Click':
            self.clicked.emit(self.ultimo)
            self.update()


class QFrameClickable(QFrame):
    clicked = pyqtSignal(object)

    def __init__(self, parent=None):
        super(QFrameClickable, self).__init__(parent)

    # def mousePressEvent(self, QMouseEvent):
    #     if QMouseEvent.button() == Qt.LeftButton:
    #         self.clicked.emit()
    #     elif QMouseEvent.button() == Qt.RightButton:
    #         self.clicked.emit()
    #     self.update()

    def mousePressEvent(self, event):
        self.ultimo = 'Click'

    def mouseReleaseEvent(self, event):
        if self.ultimo == 'Click':
            QTimer.singleShot(QApplication.instance().doubleClickInterval(),
                              self.performSingleClickAction)
        else:
            self.ultimo = 'doubleClick'
            self.clicked.emit(self.ultimo)

    def mouseDoubleClickEvent(self, event):
        self.ultimo = 'doubleClick'

    def performSingleClickAction(self):
        if self.ultimo == 'Click':
            self.clicked.emit(self.ultimo)
            self.update()


class LineEditEntered(QLineEdit):
    sig_return_pressed = pyqtSignal()

    def __init__(self):
        QLineEdit.__init__(self)

    def keyPressEvent(self, event):
        super(LineEditEntered, self).keyPressEvent(event)

        if event.key() == Qt.Key_Return:
            self.sig_return_pressed.emit()
        elif event.key() == Qt.Key_Enter:
            self.sig_return_pressed.emit()
