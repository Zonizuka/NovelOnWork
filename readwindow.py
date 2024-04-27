from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QMouseEvent, QGuiApplication, QPainter, QPen, QColor, QFontMetrics, \
    QKeySequence, QShortcut


# 只支持utf-8和ANSI编码格式
def readText(fileName):
    # 读取文本
    try:
        with open(fileName, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except UnicodeDecodeError:
        with open(fileName, 'r', encoding='ANSI') as file:
            content = file.read()
            return content


class ReadWindow(QWidget):
    def __init__(self, settings, fileName):
        super().__init__()

        self.settings = settings

        self.textContent = readText(fileName)
        self.text = self.rollPage(self.settings.currentPage)

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
        painter.setFont(self.settings.qFont)
        painter.setPen(QPen(self.settings.qColor))
        painter.fillRect(self.rect(), QColor(0, 0, 0, 1))
        textLines = self.text.split('\n')
        metrics = QFontMetrics(self.settings.font)
        yPosition = metrics.ascent()
        # 遍历文本行列表
        for line in textLines:
            # 在当前yPosition位置绘制文本行
            painter.drawText(QPoint(0, yPosition), line)
            # 更新yPosition位置为下一行文本的基线位置，包括行间距
            yPosition += metrics.height() + self.settings.lineSpacing

    def initUI(self):
        # 计算文本高度和宽度
        fontMetrics = QFontMetrics(self.settings.font)
        textWidth = fontMetrics.horizontalAdvance('中') * self.settings.lineSize
        textHeight = (fontMetrics.height() + self.settings.lineSpacing) * self.settings.textLine - self.settings.lineSpacing
        # 获取主屏幕
        screen = QGuiApplication.primaryScreen()
        # 获取屏幕的尺寸
        size = screen.size()
        screenWidth = size.width()
        screenHeight = size.height()

        x = screenWidth - 500
        y = screenHeight - 200
        self.setGeometry(x, y, textWidth, textHeight)

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
                if count >= self.settings.lineSize:
                    string += '\n'
                    count = 0
                    line += 1
            mark += 1
            if line >= self.settings.textLine:
                break
        return string, mark

    # 翻页功能，查找并处理文本
    def rollPage(self, page):
        if page < 0:
            return
        pageOffset = page - self.settings.lastPage
        if pageOffset >= 0:
            text, nextMark = self.subText(self.settings.pages[page % self.settings.pageSize])
            if len(text) == 0:
                return
            self.settings.currentPage = page
            self.settings.pages[(page + 1) % self.settings.pageSize] = nextMark
            self.settings.lastPage += 1
            return text
        else:
            if -pageOffset < self.settings.pageSize:
                self.settings.currentPage = page
                text, _ = self.subText(self.settings.pages[page % self.settings.pageSize])
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
        text = self.rollPage(self.settings.currentPage + 1)
        if text:
            self.text = text
            self.update()

    def last_shortcut_activated(self):
        text = self.rollPage(self.settings.currentPage - 1)
        if text:
            self.text = text
            self.update()
