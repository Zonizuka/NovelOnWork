from PySide6.QtGui import QFont, QMouseEvent
from PySide6.QtWidgets import QTextEdit, QLabel
from PySide6.QtCore import QEvent, QPoint


class TextContent(QLabel):
    def __init__(self, fileName, config):
        super().__init__()
        self.initText(fileName, config)

    def initText(self, fileName, config):
        # 设置字体大小
        font = QFont()
        font.setPointSize(int(config.get('settings', 'fontSize')))
        self.setFont(font)

        # 设置字体颜色

        # 读取文本
        with open(fileName, 'r', encoding='utf-8') as file:
            content = file.read()
            self.setText("测试文字")

    # 重写点击事件
    def mousePressEvent(self, event: QMouseEvent) -> None:
        event.ignore()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        event.ignore()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        event.ignore()

