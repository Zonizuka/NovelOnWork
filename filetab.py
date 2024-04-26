from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QFileDialog

from readwindow import ReadWindow


class FileTab(QWidget):
    def __init__(self, settings):
        super().__init__()

        btn = QPushButton("打开新文件")
        btn.setMaximumSize(90, 30)
        self.open_button = btn
        self.open_button.clicked.connect(lambda: self.open_file_dialog(settings))

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.open_button)
        self.setLayout(h_layout)

    def open_file_dialog(self, settings):
        fileName, _ = QFileDialog.getOpenFileName(self, "选择文本文件", "", "Text Files (*.txt)")
        if fileName:
            print(f"选中的文件: {fileName}")
            self.readWindow = ReadWindow(settings, fileName)
            self.readWindow.show()
