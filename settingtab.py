from PySide6.QtWidgets import QWidget, QPushButton, QFontDialog, QGridLayout, QColorDialog, QLabel, QSpinBox
from settingdata import settingData


class SettingsTab(QWidget):

    def __init__(self):
        super().__init__()
        self.fontButton = QPushButton("字体大小")
        self.fontButton.clicked.connect(self.changeFont)

        self.fontColorButton = QPushButton("字体颜色")
        self.fontColorButton.clicked.connect(self.changeColor)

        self.textLineSet = QSpinBox()
        self.lineSizeSet = QSpinBox()

        self.gLayout = QGridLayout(self)
        self.gLayout.addWidget(self.fontButton, 0, 0)
        self.gLayout.addWidget(self.fontColorButton, 0, 2)
        self.gLayout.addWidget(QLabel('文本行数'), 1, 0)
        self.gLayout.addWidget(self.textLineSet, 1, 1)
        self.gLayout.addWidget(QLabel('每行文字数'), 1, 2)
        self.gLayout.addWidget(self.lineSizeSet, 1, 3)

    def changeFont(self):
        ok, font = QFontDialog().getFont(settingData.qFont, self)  # 显示字体选择对话框
        if ok:
            settingData.qFont = font

    def changeColor(self):
        color = QColorDialog.getColor(settingData.qColor, self, options=QColorDialog.ColorDialogOption.ShowAlphaChannel)
        if color.isValid():
            settingData.qColor = color
