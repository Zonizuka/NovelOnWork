import configparser

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QMouseEvent, QGuiApplication, QFont, QPainter, QPen, QColor, QFontMetrics, \
    QKeySequence, QShortcut

config = configparser.ConfigParser()
config.read('settings.ini')


def readText(fileName):
    # 读取文本
    with open(fileName, 'r', encoding='utf-8') as file:
        content = file.read()
        return content


class ReadWindow(QWidget):
    def __init__(self, fileName):
        super().__init__()

        self.font = QFont(config.get('settings', 'fontStyle'), int(config.get('settings', 'fontSize')))
        self.color = QColor(0, 0, 0)

        self.textLine = int(config.get('settings', 'textLine'))
        self.lineSize = int(config.get('settings', 'lineSize'))
        self.textSize = self.textLine * self.lineSize

        # 页数
        self.pageSize, self.pages, self.lastPage, self.currentPage = self.initPage()

        # 初始化文本
        self.textContent = readText(fileName)
        self.text = self.rollPage(self.pages[self.currentPage])

        self.initUI()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # 初始化鼠标按下的位置
        self.drag_position = QPoint()
        self.setAttribute(Qt.WidgetAttribute.WA_NativeWindow)

        # 添加快捷键
        self.next = QShortcut(QKeySequence("Ctrl+C"), self)
        self.last = QShortcut(QKeySequence("Ctrl+X"), self)
        self.next.activated.connect(self.next_shortcut_activated)
        self.last.activated.connect(self.last_shortcut_activated)

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setFont(self.font)

        painter.setPen(QPen(self.color))

        painter.fillRect(self.rect(), QColor(0, 0, 0, 1))

        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignLeft, self.text)

    def initUI(self):
        # 计算文本高度和宽度
        fontMetrics = QFontMetrics(self.font)
        textWidth = fontMetrics.horizontalAdvance('中') * 20
        textHeight = (fontMetrics.height() + fontMetrics.leading()) * self.textLine

        # 获取主屏幕
        screen = QGuiApplication.primaryScreen()
        # 获取屏幕的尺寸
        size = screen.size()
        screenWidth = size.width()
        screenHeight = size.height()

        x = screenWidth - 500
        y = screenHeight - 200
        self.setGeometry(x, y, textWidth, textHeight)

    def initPage(self):
        pageSize = int(config.get('settings', 'pageSize'))
        pages = [int(s) for s in config.get('settings', 'pages').split(',')]
        pages.extend([0] * (pageSize - len(pages)))
        lastPage = int(config.get('settings', 'lastPage'))
        currentPage = int(config.get('settings', 'currentPage'))
        return pageSize, pages, lastPage, currentPage

    # 根据mark来移动标记的指针，正向
    def subText(self, mark):
        count = 0
        line = 0
        string = ""
        for i in range(mark, len(self.textContent)):
            char = self.textContent[i]
            # 将多个换行符作为一个换行符进行拼接
            if char == '\n':
                try:
                    if self.textContent[i + 1] != '\n':
                        # 如果下一个字符不是换行符，拼接
                        string += char
                        count = 0
                        line += 1
                # 可能到最后一个字符
                except IndexError:
                    string += char
                    break
            else:
                string += char
                count += 1
                if count >= self.lineSize:
                    string += '\n'
                    count = 0
                    line += 1
            mark += 1
            if line >= self.textLine:
                break
        return string, mark

    # 翻页功能，查找并处理文本
    def rollPage(self, page):
        # 先判断想要获取的页码是否大于lastPage
        if page < 0:
            return
        pageOffset = page - self.lastPage
        if pageOffset >= 0:
            self.currentPage = page
            text, mark = self.subText(self.pages[page % self.pageSize])
            self.pages[(page + 1) % self.pageSize] = mark
            self.lastPage += 1
            return text
        else:
            if -pageOffset < self.pageSize:
                self.currentPage = page
                text, _ = self.subText(self.pages[page % self.pageSize])
                return text
            else:
                return

    def nativeEvent(self, eventType, message):
        # 处理Windows系统的WM_NCHITTEST消息，以允许拖拽
        if eventType == "windows_generic_msg":
            msg = message
            if msg.window() == self.winId() and msg.message() == 0x84:  # WM_NCHITTEST
                x = msg.lParam() & 0xFFFF
                y = msg.lParam() >> 16
                if self.rect().contains(QPoint(x, y)):
                    # 返回HTCAPTION，让系统知道点击的是标题栏区域
                    return True, 1  # HTCAPTION
        return super().nativeEvent(eventType, message)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        # 如果按下的是鼠标左键，记录按下时的位置
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        # 如果鼠标左键被按下，移动窗口
        if event.buttons() & Qt.MouseButton.LeftButton:
            delta = event.pos() - self.drag_position
            self.move(self.x() + delta.x(), self.y() + delta.y())

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        # 鼠标释放时重置拖动位置
        self.drag_position = QPoint()

    def next_shortcut_activated(self):
        text = self.rollPage(self.currentPage + 1)
        if text:
            self.text = text
            self.update()

    def last_shortcut_activated(self):
        text = self.rollPage(self.currentPage - 1)
        if text:
            self.text = text
            self.update()
