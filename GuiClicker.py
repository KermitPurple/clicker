import sys
import threading
import keyboard, mouse
from gui import Ui_AutoClicker
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow

class GuiClicker(Ui_AutoClicker):
    def __init__(self):
        self.running = False

    def setupUi(self, win):
        Ui_AutoClicker.setupUi(self, win)
        self.ToggleButton.clicked.connect(self.toggle_running)

    def toggle_running(self):
        self.running = not self.running
        print(self.running)

    def run(self, win):
        while win.isActiveWindow():
            if self.running:
                if self.LeftClick.isChecked():
                    mouse.click()
                    print("LeftClick")
                elif self.RightClick.isChecked():
                    mouse.right_click()
                else:
                    keyboard.send(self.PressText.text())

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
