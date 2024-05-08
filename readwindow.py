from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QMouseEvent, QGuiApplication, QPainter, QPen, QColor, QFontMetrics, \
    QKeySequence, QShortcut, QAction
from settingdata import settingData


# 只支持utf-8和ANSI编码格式
def readText(fileName):
    # 读取文本
    if settingData.filePath != fileName:
        settingData.currentPage = 0
        settingData.lastPage = 0
        settingData.pages = [0] * settingData.pageSize
    settingData.filePath = fileName

    encodings = ['utf-8', 'ANSI', 'gbk']
    # 尝试每种编码格式
    for encoding in encodings:
        try:
            with open(fileName, 'r', encoding=encoding) as file:
                text = file.read()
                return text
        except UnicodeDecodeError:
            pass
            # 如果所有编码都失败，抛出异常
    raise IOError(f"Could not decode the file {fileName} with any of the encodings: {encodings}")


class ReadWindow(QWidget):
    def __init__(self, fileName):
        super().__init__()

        self.settings = settingData
        self.textContent = readText(fileName)
        self.text = self.rollPage(self.settings.currentPage)
        self.initUI()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.closeSelf = QAction("关闭")
        self.addAction(self.closeSelf)
        self.closeSelf.triggered.connect(self.close)

        # 初始化鼠标按下的位置
        self.mousePosition = QPoint()
        self.setAttribute(Qt.WidgetAttribute.WA_NativeWindow)

        # 添加快捷键
        self.next = QShortcut(QKeySequence(settingData.nextShortCut), self)
        self.last = QShortcut(QKeySequence(settingData.lastShortCut), self)
        self.next.activated.connect(lambda: self.rollPageActive(self.settings.currentPage + 1))
        self.last.activated.connect(lambda: self.rollPageActive(self.settings.currentPage - 1))

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setFont(self.settings.qFont)
        painter.setPen(QPen(self.settings.qColor))
        painter.fillRect(self.rect(), QColor(0, 0, 0, 1))
        textLines = self.text.split('\n')
        metrics = QFontMetrics(self.settings.qFont)
        yPosition = metrics.ascent()
        # 遍历文本行列表
        for line in textLines:
            # 在当前yPosition位置绘制文本行
            painter.drawText(QPoint(0, yPosition), line)
            # 更新yPosition位置为下一行文本的基线位置，包括行间距
            yPosition += metrics.height() + self.settings.lineSpacing

    def initUI(self):
        # 计算文本高度和宽度
        fontMetrics = QFontMetrics(self.settings.qFont)
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
            self.mousePosition = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        # 如果鼠标左键被按下，移动窗口
        if event.buttons() & Qt.MouseButton.LeftButton:
            delta = event.pos() - self.mousePosition
            self.move(self.x() + delta.x(), self.y() + delta.y())

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        # 鼠标释放时重置拖动位置
        self.mousePosition = QPoint()

    def rollPageActive(self, page):
        text = self.rollPage(page)
        if text:
            self.text = text
            self.update()
