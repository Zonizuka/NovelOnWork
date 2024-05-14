import configparser

from PySide6.QtGui import QFont, QColor

config = configparser.ConfigParser()


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
        self.nextShortCut = 'C'
        self.lastShortCut = 'Z'
        self.font = 'Arial'
        self.size = 12
        self.qFont = QFont(self.font, self.size)
        self.red = 0
        self.green = 0
        self.blue = 0
        self.alpha = 255
        self.qColor = QColor(self.red, self.green, self.blue, self.alpha)
        self.outRed = 0
        self.outGreen = 0
        self.outBlue = 0
        self.outAlpha = 0
        self.outColor = QColor(self.outRed, self.outGreen, self.outBlue, self.outAlpha)

    def readData(self):
        config.read('settings.ini', encoding='utf-8')
        self.filePath = config.get('file', 'filePath')
        self.textLine = int(config.get('settings', 'textline'))
        self.lineSize = int(config.get('settings', 'linesize'))
        self.lineSpacing = int(config.get('settings', 'linespacing'))
        self.pageSize = int(config.get('settings', 'pagesize'))
        pages = config.get('settings', 'pages').split(',')
        self.pages = [0] * self.pageSize
        for i in range(0, len(pages)):
            self.pages[i] = int(pages[i])
        self.lastPage = int(config.get('settings', 'lastpage'))
        self.currentPage = int(config.get('settings', 'currentpage'))
        self.nextShortCut = config.get('settings', 'nextshortcut')
        self.lastShortCut = config.get('settings', 'lastshortcut')
        self.font = config.get('fontSettings', 'font')
        self.size = int(config.get('fontSettings', 'size'))
        self.qFont = QFont(self.font, self.size)
        self.red = int(config.get('fontSettings', 'red'))
        self.green = int(config.get('fontSettings', 'green'))
        self.blue = int(config.get('fontSettings', 'blue'))
        self.alpha = int(config.get('fontSettings', 'alpha'))
        self.qColor = QColor(self.red, self.green, self.blue, self.alpha)
        self.outRed = int(config.get('fontSettings', 'outred'))
        self.outGreen = int(config.get('fontSettings', 'outgreen'))
        self.outBlue = int(config.get('fontSettings', 'outblue'))
        self.outAlpha = int(config.get('fontSettings', 'outalpha'))
        self.outColor = QColor(self.outRed, self.outGreen, self.outBlue, self.outAlpha)

    def writeData(self):
        config.set('file', 'filePath', self.filePath)
        config.set('settings', 'textline', str(self.textLine))
        config.set('settings', 'linesize', str(self.lineSize))
        config.set('settings', 'linespacing', str(self.lineSpacing))
        config.set('settings', 'pagesize', str(self.pageSize))
        stringList = [str(i) for i in self.pages]
        newString = ','.join(stringList)
        config.set('settings', 'pages', newString)
        config.set('settings', 'lastpage', str(self.lastPage))
        config.set('settings', 'currentpage', str(self.currentPage))
        config.set('settings', 'nextshortcut', self.nextShortCut)
        config.set('settings', 'lastshortcut', self.lastShortCut)
        config.set('fontSettings', 'font', self.qFont.family())
        config.set('fontSettings', 'size', str(self.qFont.pointSize()))
        config.set('fontSettings', 'red', str(self.qColor.red()))
        config.set('fontSettings', 'green', str(self.qColor.green()))
        config.set('fontSettings', 'blue', str(self.qColor.blue()))
        config.set('fontSettings', 'alpha', str(self.qColor.alpha()))
        config.set('fontSettings', 'outred', str(self.outColor.red()))
        config.set('fontSettings', 'outgreen', str(self.outColor.green()))
        config.set('fontSettings', 'outblue', str(self.outColor.blue()))
        config.set('fontSettings', 'outalpha', str(self.outColor.alpha()))

        with open('settings.ini', 'w', encoding='utf-8') as configfile:
            config.write(configfile)


settingData = SettingData()
