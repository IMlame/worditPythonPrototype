if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import (QApplication)
    from MainWindow import MainWindow

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
