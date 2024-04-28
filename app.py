from PySide6 import QtGui
from PySide6.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout
from filetab import FileTab
from settingdata import SettingData
from settingtab import SettingsTab


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.settings = SettingData()
        try:
            self.settings.readData()
        except Exception as e:
            print(e)

        # 创建选项卡部件
        self.tab_widget = QTabWidget()

        # 创建文件选项卡
        self.file_tab = FileTab(self.settings)
        # 添加文件选项卡到 QTabWidget
        self.tab_widget.addTab(self.file_tab, "文件")

        # 创建设置选项卡
        self.settings_tab = SettingsTab(self.settings)
        # 添加设置选项卡到 QTabWidget
        self.tab_widget.addTab(self.settings_tab, "设置")

        # 创建主布局
        layout = QVBoxLayout(self)
        layout.addWidget(self.tab_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 设置窗口的布局

    def initUI(self):

        self.setWindowTitle('工作神器')
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
