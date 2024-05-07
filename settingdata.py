import configparser

from PySide6.QtGui import QFont, QColor


#  单例模式
class SettingData:
    def __init__(self):
        self.filePath = ""
        self.textLine = 2
        self.lineSize = 20
        self.lineSpacing = 3
        self.pageSize = 20
        self.pages = [0] * self.pageSize
        self.lastPage = 0
        self.currentPage = 0
        self.font = 'Arial'
        self.size = 12
        self.qFont = QFont(self.font, self.size)
        self.red = 0
        self.green = 0
        self.blue = 0
        self.alpha = 255
        self.qColor = QColor(self.red, self.green, self.blue, self.alpha)

    def readData(self):
        config = configparser.ConfigParser()
        config.read('settings.ini')
        self.filePath = config.get('file', 'filePath')
        self.textLine = int(config.get('settings', 'textLine'))
        self.lineSize = int(config.get('settings', 'lineSize'))
        self.lineSpacing = int(config.get('settings', 'lineSpacing'))
        self.pageSize = int(config.get('settings', 'pageSize'))
        pages = config.get('settings', 'pages').split(',')
        self.pages = [0] * self.pageSize
        for i in range(0, len(pages)):
            self.pages[i] = int(pages[i])
        self.lastPage = int(config.get('settings', 'lastPage'))
        self.currentPage = int(config.get('settings', 'currentPage'))
        self.font = config.get('fontSettings', 'font')
        self.size = int(config.get('fontSettings', 'size'))
        self.qFont = QFont(self.font, self.size)
        self.red = int(config.get('fontSettings', 'red'))
        self.green = int(config.get('fontSettings', 'green'))
        self.blue = int(config.get('fontSettings', 'blue'))
        self.alpha = int(config.get('fontSettings', 'alpha'))
        self.qColor = QColor(self.red, self.green, self.blue, self.alpha)


settingData = SettingData()
