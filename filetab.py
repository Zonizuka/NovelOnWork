from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QFileDialog
from readwindow import ReadWindow


class FileTab(QWidget):
    def __init__(self):
        super().__init__()

        btn = QPushButton("打开新文件")
        btn.setMaximumSize(90, 30)
        self.open_button = btn

        self.readWindow = None
        self.open_button.clicked.connect(self.open_file_dialog)

        hLayout = QHBoxLayout(self)
        hLayout.addWidget(self.open_button)

    def open_file_dialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "选择文本文件", "", "Text Files (*.txt)")
        if fileName:
            self.readWindow = ReadWindow(fileName)
            if self.readWindow:
                self.readWindow.show()
