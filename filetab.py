from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QFileDialog

from readwindow import ReadWindow


class FileTab(QWidget):
    def __init__(self):
        super().__init__()

        btn = QPushButton("打开新文件")
        btn.setMaximumSize(90, 30)
        self.open_button = btn
        self.open_button.clicked.connect(self.open_file_dialog)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.open_button)
        self.setLayout(h_layout)

    def open_file_dialog(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "选择", "", "Text Files (*.txt)")

        if fileName:
            print(f"选中的文件: {fileName}")
            self.readWindow = ReadWindow(fileName)
            self.readWindow.show()

