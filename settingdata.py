import configparser

from PySide6.QtGui import QFont


class SettingData:
    def __init__(self):
        self.filePath = ""
        self.textLine = 2
        self.lineSize = 20
        self.lineSpacing = 3
        self.pageSize = 10
        self.pages = [0]
        self.lastPage = 0
        self.currentPage = 0
        self.font = 'Arial'
        self.size = 12
        self.qFont = self.initFont()

    def readData(self):
        config = configparser.ConfigParser()
        config.read('settings.ini')
        self.filePath = config.get('file', 'filePath')
        self.textLine = int(config.get('settings', 'textLine'))
        self.lineSize = int(config.get('settings', 'lineSize'))
        self.lineSpacing = int(config.get('settings', 'lineSpacing'))
        self.pageSize = int(config.get('settings', 'pageSize'))
        pages = [int(s) for s in config.get('settings', 'pages').split(',')]
        pages.extend([0] * (self.pageSize - len(pages)))
        self.pages = pages
        self.lastPage = int(config.get('settings', 'lastPage'))
        self.currentPage = int(config.get('settings', 'currentPage'))
        self.font = config.get('fontSettings', 'font')
        self.size = int(config.get('fontSettings', 'size'))
        self.qFont = self.initFont()

    def initFont(self):
        font = QFont(self.font, self.size)
        return font


