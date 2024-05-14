from PySide6.QtWidgets import QWidget, QPushButton, QFontDialog, QGridLayout, QColorDialog, QLabel, QSpinBox, \
    QKeySequenceEdit, QVBoxLayout, QHBoxLayout, QLineEdit
from settingdata import settingData
from PySide6.QtCore import Qt


def setTextAndComp(text, comp):
    textLayout = QHBoxLayout()
    textLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
    textLayout.addWidget(QLabel(text))
    textLayout.addWidget(comp)
    return textLayout


class SettingsTab(QWidget):

    def __init__(self):
        super().__init__()
        self.fontButton = QPushButton("字体大小")
        self.fontButton.clicked.connect(self.changeFont)

        self.fontColorButton = QPushButton("字体颜色")
        self.fontColorButton.clicked.connect(self.changeColor)

        self.outButton = QPushButton("鼠标移出")
        self.outButton.clicked.connect(self.changeOutColor)

        self.textLineSet = QSpinBox()
        self.lineSizeSet = QSpinBox()
        self.lineSpacingSet = QSpinBox()

        self.textLineSet.setValue(settingData.textLine)
        self.lineSizeSet.setValue(settingData.lineSize)
        self.lineSpacingSet.setValue(settingData.lineSpacing)

        self.textLineSet.setMinimum(1)
        self.textLineSet.setMinimumWidth(60)
        self.lineSizeSet.setMinimum(1)
        self.lineSizeSet.setMinimumWidth(60)
        self.lineSpacingSet.setMinimum(0)
        self.lineSpacingSet.setMinimumWidth(60)

        self.textLineSet.valueChanged.connect(self.changeTextLine)
        self.lineSizeSet.valueChanged.connect(self.changeLineSize)
        self.lineSpacingSet.valueChanged.connect(self.changeLineSpacing)

        self.mainLayout = QVBoxLayout(self)
        self.fontLayout = QHBoxLayout()
        self.fontLayout.addWidget(self.fontButton)
        self.fontLayout.addWidget(self.fontColorButton)
        self.fontLayout.addWidget(self.outButton)

        self.textLayout = QHBoxLayout()
        self.textLine = setTextAndComp('文本行数', self.textLineSet)
        self.lineSize = setTextAndComp('行文字数', self.lineSizeSet)
        self.textSpacing = setTextAndComp('行间距   ', self.lineSpacingSet)
        self.textLayout.addLayout(self.textLine)
        self.textLayout.addLayout(self.lineSize)
        # self.textLayout.addLayout(self.textSpacing)

        self.nextShortCut = QLineEdit(settingData.nextShortCut)
        self.lastShortCut = QLineEdit(settingData.lastShortCut)
        self.shortCutLayout = QHBoxLayout()
        self.next = setTextAndComp('下一页', self.nextShortCut)
        self.last = setTextAndComp('上一页', self.lastShortCut)
        self.nextShortCut.textChanged.connect(self.changeNext)
        self.lastShortCut.textChanged.connect(self.changeLast)
        self.shortCutLayout.addLayout(self.next)
        self.shortCutLayout.addLayout(self.last)

        self.mainLayout.addLayout(self.fontLayout)
        self.mainLayout.addLayout(self.textLayout)
        # self.mainLayout.addLayout(self.textLine)
        # self.mainLayout.addLayout(self.lineSize)
        self.mainLayout.addLayout(self.textSpacing)
        self.mainLayout.addLayout(self.shortCutLayout)

    def changeFont(self):
        ok, font = QFontDialog().getFont(settingData.qFont, self)  # 显示字体选择对话框
        if ok:
            settingData.qFont = font

    def changeColor(self):
        color = QColorDialog.getColor(settingData.qColor, self, options=QColorDialog.ColorDialogOption.ShowAlphaChannel)
        if color.isValid():
            settingData.qColor = color

    def changeOutColor(self):
        color = QColorDialog.getColor(settingData.outColor, self, options=QColorDialog.ColorDialogOption.ShowAlphaChannel)
        if color.isValid():
            settingData.outColor = color

    def changeTextLine(self, value):
        settingData.textLine = value

    def changeLineSize(self, value):
        settingData.lineSize = value

    def changeLineSpacing(self, value):
        settingData.lineSpacing = value

    def changeNext(self, text):
        settingData.nextShortCut = text

    def changeLast(self, text):
        settingData.lastShortCut = text
