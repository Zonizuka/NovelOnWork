from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QFileDialog
from readwindow import ReadWindow


class FileTab(QWidget):
    def __init__(self):
        super().__init__()

        btn = QPushButton("打开新文件")
        btn.setMaximumSize(90, 30)
        self.openButton = btn

        self.readWindow = None
        self.openButton.clicked.connect(self.openFileDialog)

        hLayout = QHBoxLayout(self)
        hLayout.addWidget(self.openButton)

    def openFileDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "选择文本文件", "", "Text Files (*.txt)")
        if fileName:
            if self.readWindow is None:
                self.readWindow = ReadWindow(fileName)
            else:
                self.readWindow.close()
                self.readWindow.deleteLater()
                self.readWindow = ReadWindow(fileName)
            self.readWindow.show()
