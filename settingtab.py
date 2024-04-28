from PySide6.QtWidgets import QWidget, QPushButton, QFontDialog, QGridLayout, QColorDialog, QLabel, QSpinBox


class SettingsTab(QWidget):

    def __init__(self, settings):
        super().__init__()
        self.fontButton = QPushButton("字体大小")
        self.fontButton.clicked.connect(lambda: self.changeFont(settings))

        self.fontColorButton = QPushButton("字体颜色")
        self.fontColorButton.clicked.connect(lambda: self.changeColor(settings))

        self.textLineSet = QSpinBox()
        self.lineSizeSet = QSpinBox()

        self.gLayout = QGridLayout(self)
        self.gLayout.addWidget(self.fontButton, 0, 0)
        self.gLayout.addWidget(self.fontColorButton, 0, 2)
        self.gLayout.addWidget(QLabel('文本行数'), 1, 0)
        self.gLayout.addWidget(self.textLineSet, 1, 1)
        self.gLayout.addWidget(QLabel('每行文字数'), 1, 2)
        self.gLayout.addWidget(self.lineSizeSet, 1, 3)

    def changeFont(self, settings):
        ok, font = QFontDialog().getFont(settings.qFont, self)  # 显示字体选择对话框
        if ok:
            settings.qFont = font

    def changeColor(self, settings):
        color = QColorDialog.getColor(settings.qColor, self, options=QColorDialog.ColorDialogOption.ShowAlphaChannel)
        if color.isValid():
            settings.qColor = color
