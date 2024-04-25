from PySide6.QtWidgets import QWidget, QApplication


class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("QWidget { background-color: transparent; }")


if __name__ == '__main__':
    app = QApplication([])
    window = TestWindow()
    window.show()
    app.exec()
