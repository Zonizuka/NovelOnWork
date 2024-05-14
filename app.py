from abc import abstractmethod

from PySide6 import QtGui
from PySide6.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout
from filetab import FileTab
from settingdata import settingData
from settingtab import SettingsTab


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        try:
            settingData.readData()
            print(settingData)
        except Exception as e:
            print(e)

        # 创建选项卡部件
        self.tabWidget = QTabWidget()

        # 创建文件选项卡
        self.fileTab = FileTab()
        # 添加文件选项卡到 QTabWidget
        self.tabWidget.addTab(self.fileTab, "文件")

        # 创建设置选项卡
        self.settingTab = SettingsTab()
        # 添加设置选项卡到 QTabWidget
        self.tabWidget.addTab(self.settingTab, "设置")

        # 创建主布局
        layout = QVBoxLayout(self)
        layout.addWidget(self.tabWidget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

    def initUI(self):

        self.setWindowTitle('工作神器')
        # 设置总体程序大小默认300 * 200
        self.setGeometry(0, 0, 300, 200)
        self.center()

    def center(self):
        # 获取屏幕的中心点
        screen = QtGui.QGuiApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), int((screen.height() - size.height()) / 2))


if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()
