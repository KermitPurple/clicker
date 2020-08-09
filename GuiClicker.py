import sys
from gui import Ui_AutoClicker
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

class GuiClicker(Ui_AutoClicker):
    pass

def main():
    app = QApplication(sys.argv)
    win = QMainWindow()
    gui = GuiClicker()
    gui.setupUi(win)
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
