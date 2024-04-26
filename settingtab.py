from PySide6.QtWidgets import QWidget, QPushButton, QFontDialog, QTextEdit, QGridLayout


class SettingsTab(QWidget):

    def __init__(self, settings):
        super().__init__()
        self.text_edit = QTextEdit()
        self.fontButton = QPushButton("选择字体")
        self.fontButton.clicked.connect(lambda: self.changeFont(settings))  # 当按钮被点击时，调用changeFont方法

        self.gLayout = QGridLayout()
        self.gLayout.addWidget(self.fontButton)
        self.setLayout(self.gLayout)

    def changeFont(self, settings):
        ok, font = QFontDialog().getFont(settings.qFont)  # 显示字体选择对话框
        if ok:
            settings.qFont = font
