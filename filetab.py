from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QFileDialog


class FileTab(QWidget):
    def __init__(self):
        super().__init__()
        # 创建打开新文件的按钮
        btn = QPushButton("打开新文件")
        btn.setMaximumSize(90, 30)
        self.open_button = btn
        self.open_button.clicked.connect(self.open_file_dialog)

        # 布局
        h_layout = QHBoxLayout()
        h_layout.addWidget(self.open_button)
        self.setLayout(h_layout)

    def open_file_dialog(self):
        options = QFileDialog.Option()
        fileName, _ = QFileDialog.getOpenFileName(self, "选择", "",

                                                  "Text Files (*.txt)",

                                                  options=options)

        if fileName:
            print(f"选中的文件: {fileName}")

            # 在这里处理文件，例如读取文件内容等

