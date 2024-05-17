import re

from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLineEdit, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, QPoint, QSize
from PySide6.QtGui import QMouseEvent, QGuiApplication, QPainter, QPen, QColor, QFontMetrics, \
    QKeySequence, QShortcut, QAction, QIcon
from settingdata import settingData


# 支持utf-8、ANSI、gbk编码格式
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

        self.textContent = readText(fileName)
        self.text, _ = self.rollPage(settingData.currentPage)

        self.initUI()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.selectChapter = QAction('选择章节')
        self.closeSelf = QAction('关闭')
        self.search = QAction('搜索')
        self.setAction()
        self.scrollableMenu = None
        self.searchMenu = None

        self.qPen = QPen(settingData.qColor)

        # 初始化鼠标按下的位置
        self.mousePosition = QPoint()
        self.setAttribute(Qt.WidgetAttribute.WA_NativeWindow)

        # 添加快捷键
        self.next = QShortcut(QKeySequence(settingData.nextShortCut), self)
        self.last = QShortcut(QKeySequence(settingData.lastShortCut), self)
        self.next.activated.connect(lambda: self.rollPageActive(settingData.currentPage + 1))
        self.last.activated.connect(lambda: self.rollPageActive(settingData.currentPage - 1))

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setFont(settingData.qFont)
        painter.setPen(self.qPen)
        painter.fillRect(self.rect(), QColor(0, 0, 0, 1))
        textLines = self.text.split('\n')
        metrics = QFontMetrics(settingData.qFont)
        yPosition = metrics.ascent()
        # 遍历文本行列表
        for line in textLines:
            # 在当前yPosition位置绘制文本行
            painter.drawText(QPoint(0, yPosition), line)
            # 更新yPosition位置为下一行文本的基线位置，包括行间距
            yPosition += metrics.height() + settingData.lineSpacing

    def initUI(self):
        # 计算文本高度和宽度
        fontMetrics = QFontMetrics(settingData.qFont)
        textWidth = fontMetrics.horizontalAdvance('中') * settingData.lineSize
        textHeight = (fontMetrics.height() + settingData.lineSpacing) * settingData.textLine - settingData.lineSpacing
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
                if count >= settingData.lineSize:
                    string += '\n'
                    count = 0
                    line += 1
            mark += 1
            if line >= settingData.textLine:
                break
        return string, mark

    # 翻页功能，查找并处理文本
    def rollPage(self, page):
        if page < 0:
            return None, None
        pageOffset = page - settingData.lastPage
        if pageOffset >= 0:
            text, nextMark = self.subText(settingData.pages[page % settingData.pageSize])
            if len(text) == 0:
                return None, None
            settingData.currentPage = page
            settingData.pages[(page + 1) % settingData.pageSize] = nextMark
            settingData.lastPage += 1
            return text, nextMark
        else:
            if -pageOffset < settingData.pageSize:
                settingData.currentPage = page
                text, nextMark = self.subText(settingData.pages[page % settingData.pageSize])
                return text, nextMark
            else:
                return None, None

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

    def setAction(self):
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.addAction(self.selectChapter)
        self.addAction(self.search)
        self.addAction(self.closeSelf)
        self.selectChapter.triggered.connect(self.displayChapter)
        self.search.triggered.connect(self.displaySearch)
        self.closeSelf.triggered.connect(self.close)

    def displayChapter(self):
        self.scrollableMenu = ScrollableMenu(self)
        self.scrollableMenu.show()

    def displaySearch(self):
        self.searchMenu = SearchMenu(self)
        self.searchMenu.show()

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
        text, _ = self.rollPage(page)
        if text:
            self.text = text
            self.update()

    def enterEvent(self, event: QMouseEvent) -> None:
        self.qPen = QPen(settingData.qColor)
        self.update()

    def leaveEvent(self, event: QMouseEvent) -> None:
        self.qPen = QPen(settingData.outColor)
        self.update()

    def closeEvent(self, event):
        settingData.writeData()
        event.accept()

    def getChapter(self):
        chapter = {}
        page = 0
        mark = 0
        temp, mark = self.subText(mark)
        pattern = re.compile(r'(第)([\u4e00-\u9fa5a-zA-Z0-9]{1,7})[章|节].{0,20}(\n|$)')

        while len(temp) > 1:
            lines = temp.splitlines()
            for i in range(len(lines)):
                line = lines[i].strip()
                if re.match(pattern, line):
                    chapter[line] = page
            page += 1
            temp, mark = self.subText(mark)
        return chapter

    def jumpToChapter(self, item, chapter):
        text = ''
        page = chapter[item.text()]
        settingData.currentPage = page
        settingData.lastPage = page
        mark = 0
        for i in range(0, page + 1):
            settingData.pages[i % settingData.pageSize] = mark
            text, mark = self.subText(mark)
        settingData.pages[(page + 1) % settingData.pageSize] = mark
        self.text = text
        self.update()

    def searchContent(self, string, searchMenu):
        count = 0
        line = 0
        page = 0
        result = {}
        for i in range(0, len(self.textContent)):
            char = self.textContent[i]
            if char == '\n':
                try:
                    if self.textContent[i + 1] != '\n':
                        count = 0
                        line += 1
                except IndexError:
                    break
            else:
                count += 1
                if count >= settingData.lineSize:
                    count = 0
                    line += 1
                if char == string[0]:
                    if self.textContent[i: i + len(string)] == string:
                        result[self.textContent[i: i + 20]] = page
            if line >= settingData.textLine:
                page += 1
        searchMenu.displaySearchResult(result, self)


class ScrollableMenu(QWidget):
    def __init__(self, readWindow):
        super().__init__()
        chapter = readWindow.getChapter()
        self.setWindowTitle('选择章节')
        layout = QVBoxLayout(self)

        listWidget = QListWidget()
        for key in chapter.keys():
            listWidget.addItem(QListWidgetItem(key))
        listWidget.itemDoubleClicked.connect(lambda item: readWindow.jumpToChapter(item, chapter))

        layout.addWidget(listWidget)


class SearchMenu(QWidget):
    def __init__(self, readWindow):
        super().__init__()
        self.setWindowTitle('搜索')

        layout = QVBoxLayout(self)
        searchLayout = QHBoxLayout()

        self.searchLine = QLineEdit(self)
        self.searchLine.setPlaceholderText('输入搜索内容...')

        icon = QIcon.fromTheme(QIcon.ThemeIcon.EditFind)
        self.searchButton = QPushButton()
        self.searchButton.setFixedSize(QSize(18, 18))
        self.searchButton.setFlat(True)
        self.searchButton.setIcon(icon)
        self.searchButton.clicked.connect(lambda: readWindow.searchContent(self.searchLine.text(), self))

        self.listWidget = QListWidget()

        searchLayout.addWidget(self.searchLine)
        searchLayout.addWidget(self.searchButton)
        layout.addLayout(searchLayout)
        layout.addWidget(self.listWidget)

    def displaySearchResult(self, result, readWindow):
        for key in result.keys():
            self.listWidget.addItem(QListWidgetItem(key))
        self.listWidget.itemDoubleClicked.connect(lambda item: readWindow.jumpToChapter(item, result))
