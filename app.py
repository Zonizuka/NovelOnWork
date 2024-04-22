from PySide6 import QtGui
from PySide6.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout
from filetab import FileTab
from settingtab import SettingsTab


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_UI()

        # 创建选项卡部件
        self.tab_widget = QTabWidget()

        # 创建文件选项卡
        self.file_tab = FileTab()
        # 添加文件选项卡到 QTabWidget
        self.tab_widget.addTab(self.file_tab, "文件")

        # 创建设置选项卡
        self.settings_tab = SettingsTab()
        # 添加设置选项卡到 QTabWidget
        self.tab_widget.addTab(self.settings_tab, "设置")

        # 创建主布局
        layout = QVBoxLayout()
        layout.addWidget(self.tab_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 设置窗口的布局
        self.setLayout(layout)

    def init_UI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('工作神器')
        self.setGeometry(0, 0, 300, 200)  # 初始大小和位置，这里仅作为示例，稍后会被覆盖

        # 使窗口在屏幕中央显示
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