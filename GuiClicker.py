import sys
import threading
from gui import Ui_AutoClicker
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

class GuiClicker(Ui_AutoClicker):
    def __init__(self):
        self.running = True

    def run(self, win):
        while self.running:
            print('h1')
            if not win.isActiveWindow():
                self.running = False

def main():
    app = QApplication(sys.argv)
    win = QMainWindow()
    gui = GuiClicker()
    gui.setupUi(win)
    win.show()
    th = threading.Thread(target = gui.run, args=(win,))
    th.start()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
