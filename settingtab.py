from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget, QPushButton, QFontDialog, QGridLayout, QColorDialog


class SettingsTab(QWidget):

    def __init__(self, settings):
        super().__init__()
        self.fontButton = QPushButton("字体大小")
        self.fontButton.clicked.connect(lambda: self.changeFont(settings))

        self.fontColorButton = QPushButton("字体颜色")
        self.fontColorButton.clicked.connect(lambda: self.changeColor(settings))

        self.gLayout = QGridLayout()
        self.gLayout.addWidget(self.fontButton)
        self.gLayout.addWidget(self.fontColorButton)
        self.setLayout(self.gLayout)

    def changeFont(self, settings):
        ok, font = QFontDialog().getFont(settings.qFont, self)  # 显示字体选择对话框
        if ok:
            settings.qFont = font

    def changeColor(self, settings):
        color = QColorDialog.getColor(QColor(0, 0, 0, 255), self, options=QColorDialog.ColorDialogOption.ShowAlphaChannel)
        if color.isValid():
            settings.qColor = color
